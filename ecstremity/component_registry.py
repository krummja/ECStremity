from __future__ import annotations
from typing import *
from collections import OrderedDict
from ecstremity.component import Component


class ComponentRegistry:

    def __init__(self, engine):
        self.engine = engine
        self._cbit: int = 0
        self._map = OrderedDict()

    def register(self, component: Component):
        component.cbit = self._cbit
        component.client = self.engine.client
        self._cbit += 1
        self._map[component.name] = component

    def __getitem__(self, key: Union[Component, str]):
        if isinstance(key, Component):
            key = key.name
        return self._map[key.upper()]
