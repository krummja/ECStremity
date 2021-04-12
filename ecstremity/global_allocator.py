from __future__ import annotations
from typing import *

import numpy as np
from ecstremity.table import Table, INDEX_SEPARATOR
from ecstremity.components import BaseComponent as Component


def verify_component_schema(allocation_schema) -> bool:
    started = [False] * len(allocation_schema[0])
    ended = [False] * len(allocation_schema[0])
    for row in allocation_schema:
        for i, val in enumerate(row):
            if val:
                if not started[i]:
                    print("--------------")
                    print(started)
                    print(ended)
                    print("--------------")
                    started[i] = True
                else:
                    if ended[i]:
                        print("--------------")
                        print(started)
                        print(ended)
                        print("--------------")
                        return False
            elif started[i]:
                print("--------------")
                print(started)
                print(ended)
                print("--------------")
                ended[i] = True
    return True


class GlobalAllocator:

    def __init__(
            self,
            components: List[Component],
            allocation_scheme
        ) -> None:
        self.component_registry = {component.name: component for component in components}
        self._memoized = {}  # for selectors_from_component_names

        names: List[str] = [component.name for component in components]
        self.names: List[str] = names
        self._allocation_table = Table(names, tuple(allocation_scheme))

        self._cached_adds = []
        self._next_uid = 0
        self.__accessor_factory = None
        self.__accessors = []

    def accessor_from_uid(self, uid):
        accessor = self.__accessor_factory(uid)
        self.__accessors.append(accessor)
        return accessor

    @property
    def allocation_table(self):
        return self._allocation_table

    @property
    def next_uid(self):
        self._next_uid += 1
        return self._next_uid

    @property
    def uids(self):
        return tuple(self._allocation_table.uids)

    def add(self, values_dict, uid=None):
        component_dict = self.component_registry

        def convert_to_component_array(component: Component, value):
            """Converts value to a NumPy array with appropriate shape for component."""
            value = np.array(value, dtype=component.datatype)
            shape = value.shape or (1,)
            dim = component.dim
            assert shape == dim or (len(shape) > 1 and shape[1:] == dim), \
                f"Component '{component.name}' expected shape {component.dim} but got {value.shape}"
            return value

        result = {'uid': uid or self.next_uid}
        for name, value in values_dict.items():
            result[name] = convert_to_component_array(component_dict[name], value)
        assert result['uid'] not in {d['uid'] for d in self._cached_adds}, "Cannot add a uid twice."
        self._cached_adds.append(result)
        return result['uid']

    def delete(self, uid):
        self._allocation_table.stage_delete(uid)

    def _defrag(self):
        if (not self._cached_adds) and (None not in self._allocation_table.uids):
            return

        def safe_len(item):
            if item is None:
                return 0
            shape = item.shape

            if len(shape) > 1:
                return shape[0]
            else:
                return 1

        for add in self._cached_adds:
            uid = add['uid']
            add = tuple(safe_len(add.get(name, None)) for name in self._allocation_table.column_names)
            self._allocation_table.stage_add(uid, add)

        for name, (new_size, sources, targets) in zip(
                self._allocation_table.column_names,
                self._allocation_table.compress()):
            component = self.component_registry[name]
            component.assert_capacity(new_size)
            for source, target in zip(sources, targets):
                component[target] = component[source]

        for add in self._cached_adds:
            uid = add['uid']
            for name, this_slice in zip(
                    self._allocation_table.column_names,
                    self._allocation_table.slices_from_uid(uid)):
                if name in add:
                    self.component_registry[name][this_slice] = add[name]

        self._cached_adds = []
        self._memoized = {}
        for accessor in self.__accessors:
            accessor.dirty = True

    def is_valid_query(self, query, separator=INDEX_SEPARATOR):
        for x in query:
            if (separator not in x) and (x not in self.names):
                print(f"{x} in query is not valid.")
                return False
            return True

    def selectors_from_component_query(self, query, separator=INDEX_SEPARATOR):
        assert isinstance(query, tuple), "argument must be hashable"
        assert self.is_valid_query(query), "col_names must be valid component names and index names."
        if query not in self._memoized:
            indices = tuple(filter(lambda x: separator in x, query))
            col_names = tuple(filter(lambda x: x not in indices, query))
            selectors, indices = self._allocation_table.mask_slices(col_names, indices)
            result = {n: self.component_registry[n][s] for n, s in selectors.items()}
            result.update({n: np.array(l) for n, l in indices.items()})
            self._memoized[query] = result
        else:
            result = self._memoized[query]
        return dict(result)
