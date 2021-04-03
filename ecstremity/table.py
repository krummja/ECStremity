from __future__ import annotations
from typing import *


class Table:

    def __init__(
            self,
            column_names: Tuple[str],
            class_ids: Tuple[Tuple[int, int]]
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
        pass

    def stage_add(self, uid, value_tuple):
        pass

    def stage_delete(self, uid):
        pass

    def make_starts_table(self):
        pass

    def section_slices(self):
        pass

    def uid_slices(self, uid):
        pass

    def rows_from_class_ids(self, class_ids):
        pass

    def mask_slices(self, col_names, indices):
        pass

    def compress(self):
        pass

    def slices_from_uid(self, uid):
        pass

    def show_sizes(self):
        pass

    def show_starts(self):
        pass

    def __str__(self):
        return "<Table: " + ' '.join(self.__col_names) + ">"
