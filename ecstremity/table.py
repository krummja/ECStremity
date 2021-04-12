from __future__ import annotations

from abc import abstractmethod
from typing import *
from collections.abc import MutableMapping, Sequence

INDEX_SEPARATOR = '__to__'


def slice_is_not_empty(s):
    return s.start != s.stop


class TableRow(Sequence):

    def __init__(self, *values) -> None:
        if isinstance(values[0], Generator):
            self.values = tuple(values[0])
        elif isinstance(values[0], tuple):
            self.values = values[0]
        else:
            self.values = tuple(values)

    def __add__(self, other):
        other = tuple(other)
        assert len(other) == len(self.values), "Must add item of same length"
        return TableRow(this + that for this, that in zip(self.values, other))

    def __sub__(self, other):
        other = tuple(other)
        assert len(other) == len(self.values), "Must add item of same length"
        return TableRow(this - that for this, that in zip(self.values, other))

    def __eq__(self, other):
        return self.values == other

    def __ne__(self, other):
        return self.values != other

    def __repr__(self):
        return f"TableRow: {(self.values,)}"

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return iter(self.values)

    def copy(self):
        return TableRow(*self.values)

    def __getitem__(self, index):
        return self.values[index]


class Table:

    def __init__(
            self,
            column_names: List[str],
            class_ids: Tuple[Tuple[int, ...]]
    ) -> None:
        self.__col_names = tuple(column_names)
        self.__row_length = len(column_names)
        self.__row_format = ''.join((" | {:>%s}" % (len(name) for name in column_names)))
        self._staged_adds = {}
        self.known_class_ids = tuple(class_ids)
        self.class_ids = []
        self.uids = []
        self.starts = []
        self.sizes = []

    @property
    def column_names(self):
        return self.__col_names

    def entity_class_from_tuple(self, sizes_tuple):
        """Takes a component tuple like (5,5,0,2,2,2) and returns
        a normalized tuple that is a class id, like (1,1,0,1,1,1)
        """
        assert len(sizes_tuple) == self.__row_length, "too many values"
        return tuple(0 if x == 0 else x / x for x in sizes_tuple)

    def stage_add(self, uid, value_tuple):
        assert uid not in self.uids, "uid must be unique"
        assert uid not in {t[0] for lst in self._staged_adds.values() for t in lst}, "cannot restage a staged uid"
        entity_class = self.entity_class_from_tuple(value_tuple)
        self._staged_adds.setdefault(entity_class, []).append((uid, value_tuple))

    def stage_delete(self, uid):
        self.uids[self.uids.index(uid)] = None

    def make_starts_table(self):
        start = TableRow(*(0,) * self.__row_length)
        table = [start]
        for row in self.sizes:
            start = row + start
            table.append(start)
        return table

    def section_slices(self) -> Dict[Tuple[int, ...], slice]:
        import cardinality
        expressed_ids: Iterator[Tuple[int, ...]] = filter(lambda x: x in self.class_ids, self.known_class_ids)
        starts: Iterator[int] = map(self.class_ids.index, expressed_ids)
        assert all(starts[x] < starts[x + 1] for x in range(cardinality.count(starts) - 1)), \
            "id_column must be in same order as known ids"
        stops = starts[1:] + [None]
        return {class_id: slice(start, stop, 1) for class_id, start, stop in zip(expressed_ids, starts, stops)}

    def uid_slices(self, uid) -> Dict[str, slice]:
        assert uid in self.uids, "uid must already be allocated"
        index: int = self.uids.index(uid)
        starts = self.starts[index]
        sizes = self.sizes[index]
        return {attr: slice(start, start + size) for
                attr, start, size in zip(self.column_names, starts, sizes) if size}

    def rows_from_class_ids(self, class_ids) -> Tuple[TableRow, List[int]]:
        result: List[int, ...] = []
        starts: TableRow = TableRow(*(0,) * self.__row_length)
        started: bool = self.class_ids[0] in class_ids
        all_ids: Iterator[Tuple[int, int]] = iter(self.class_ids)
        for class_id, size_row in zip(all_ids, self.sizes):
            if started:
                if class_id in class_ids:
                    result.append(size_row)
                else:
                    break
            else:
                if class_id in class_ids:
                    result.append(size_row)
                    started = True
                else:
                    starts += size_row
        assert not any(_id in class_ids for _id in all_ids), "given set of class_ids must be contiguous"
        return starts, result

    def mask_slices(self, col_names, indices):
        names = self.__col_names

        def to_indices(string, col_names=names, sep=INDEX_SEPARATOR) -> Tuple[int, int]:
            p1, p2 = string.split(sep)
            assert (p1 in col_names), f"{p1} must be a column_name"
            assert (p2 in col_names), f"{p2} must be a column_name"
            return col_names.index(p1), col_names.index(p2)

        mask_tuple = tuple(1 if n in col_names else 0 for n in names)

        def in_mask(item_tuple, mask=mask_tuple) -> Generator[Any, Any, None]:
            return (x for x, m in zip(item_tuple, mask) if m)

        matched_ids = {class_id for class_id in self.known_class_ids if all(in_mask(class_id))}
        idxs = tuple(map(to_indices, indices))
        sizes = TableRow(*(0,) * self.__row_length)
        idx_result = tuple([] for _ in range(len(idxs)))

        starts, rows = self.rows_from_class_ids(matched_ids)
        for i, row in enumerate(rows):
            sizes += row
            for lst, (s, t) in zip(idx_result, idxs):
                assert row[s] == 1, "must broadcast from size == 1"
                lst.extend([i] * row[t])

        selectors = {n: slice(st, st + si) for n, st, si in zip(names, starts, sizes) if n in col_names}
        indices = {n: lst for n, lst in zip(indices, idx_result)}
        return selectors, indices

    def compress(self):
        sizes = self.sizes
        uids = self.uids
        new_class_ids = []
        new_uids = []
        new_sizes = []

        def empty_row():
            return TableRow(*(0,) * self.__row_length)

        # start at 0 for everything
        sources = []
        targets = []
        free_start = empty_row()
        current_start = empty_row()
        total_alloc = empty_row()
        # TODO could this be reduce?
        ends = TableRow(sum(column) for column in zip(*sizes)) or empty_row()
        new_ends = ends.copy()

        # TODO section_slices should return [(class_id, section_slice),...]
        section_dict = self.section_slices()
        for class_id in self.known_class_ids:

            allocations = empty_row()
            deallocations = empty_row()
            section_slice = section_dict.get(class_id, slice(0, 0, 1))

            for uid, size_tuple in zip(uids[section_slice], sizes[section_slice]):
                assert all((start >= free_start for start, free_start in zip(current_start, free_start))), \
                    "next start must be larger than current free start"
                if uid is None:
                    current_start += size_tuple
                    deallocations += size_tuple
                else:
                    new_class_ids.append(class_id)
                    new_uids.append(uid)
                    new_sizes.append(size_tuple)
                    if current_start != free_start:
                        sources.append(tuple(
                            slice(start, start + size, 1) for start, size in zip(current_start, size_tuple)))
                        targets.append(tuple(
                            slice(start, start + size, 1) for start, size in zip(free_start, size_tuple)))
                    free_start += size_tuple
                    current_start += size_tuple

            for added_uid, size_tuple in self._staged_adds.get(class_id, ()):
                size = TableRow(size_tuple)
                allocations += size

                new_class_ids.append(class_id)
                new_uids.append(added_uid)
                new_sizes.append(size)

            free_start += allocations
            new_ends += allocations
            new_ends -= deallocations

            if current_start != free_start:
                source = tuple(slice(start, end, 1) for start, end in zip(
                    current_start, ends))
                target = tuple(slice(start, end, 1) for start, end in zip(
                    free_start, new_ends))
                sources.append(source)
                targets.append(target)

            current_start = free_start.copy()  # TODO part of last debugging
            ends = new_ends.copy()
            total_alloc += allocations

        self.class_ids = new_class_ids
        self.uids = new_uids
        self.sizes = new_sizes
        self.starts = self.make_starts_table()
        self._staged_adds = {}

        ret = []
        for new_capacity, col_sources, col_targets in zip(
                new_ends, zip(*sources), zip(*targets)):
            col_sources = tuple((s for s in col_sources if slice_is_not_empty(s)))
            col_targets = tuple((t for t in col_targets if slice_is_not_empty(t)))
            assert len(col_sources) == len(col_targets)
            ret.append((new_capacity, col_sources, col_targets))

        return ret

    def slices_from_uid(self, uid):
        idx = self.uids.index(uid)
        starts = self.starts[idx]
        sizes = self.sizes[idx]
        return (slice(start, start + size, 1) for start, size in zip(starts, sizes))

    def show_sizes(self):
        formatter = self.__row_format.format
        ret_str = " uid"
        ret_str += formatter(*self.__col_names)
        ret_str += "\n"
        for uid, size_tuple in zip(self.uids, self.sizes):
            ret_str += "{:>5}".format(uid)
            ret_str += formatter(*size_tuple.values)
            ret_str += "\n"
        return ret_str

    def show_starts(self):
        formatter = self.__row_format.format
        ret_str = " uid"
        ret_str += formatter(*self.__col_names)
        ret_str += "\n"
        for uid, size_tuple in zip(self.uids, self.starts):
            ret_str += "{:>5}".format(uid)
            ret_str += formatter(*size_tuple.values)
            ret_str += "\n"
        return ret_str

    def __str__(self):
        return "<Table: " + ' '.join(self.__col_names) + ">"
