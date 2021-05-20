from __future__ import annotations
from typing import *
from collections import OrderedDict
from ecstremity.component import Component, ComponentMeta


class ComponentRegistry:

    def __init__(self, engine):
        self.engine = engine
        self._cbit: int = 0
        self._map = OrderedDict()

    def register(self, component: ComponentMeta):
        component.cbit = self._cbit
        component.client = self.engine.client
        self._cbit += 1
        self._map[component.comp_id] = component

    def __getitem__(self, key: Union[ComponentMeta, str]):
        if isinstance(key, ComponentMeta):
            key = key.comp_id
        return self._map[key.upper()]
