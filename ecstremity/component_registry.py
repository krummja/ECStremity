from __future__ import annotations
from typing import *
from collections import OrderedDict

if TYPE_CHECKING:
    from ecstremity.component import Component


class ComponentRegistry:
    _cbit: int = 0
    _map = OrderedDict()

    def register(self, component: Component):
        component.cbit = self._cbit
        self._cbit += 1
        self._map[component.name] = component

    def get(self, key):
        return self._map[key]
