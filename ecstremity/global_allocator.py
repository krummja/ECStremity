from __future__ import annotations
from typing import *

from ecstremity.table import Table
from ecstremity.components import Component


class GlobalAllocator:

    def __init__(
            self,
            components: List[Component],
            allocation_scheme: Tuple[Tuple[int, int]]
        ) -> None:
        self.component_registry = {component.name: component for component in components}
        self._memoized = {}  # for selectors_from_component_names

        names: Tuple[str] = tuple(component.name for component in components)
        self.names: Tuple[str] = names
        self._allocation_table = Table(names, tuple(allocation_scheme))

        self._cached_adds = []
        self._next_uid = 0
        self.__accessor_factory = None
        self.__accessors = []

    def accessor_from_uid(self, uid):
        pass

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
        pass

    def delete(self, uid):
        pass

    def _defrag(self):
        pass

    def is_valid_query(self):
        pass

    def selectors_from_component_query(self):
        pass
