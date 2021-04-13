from __future__ import annotations
from typing import *
from ecstremity.component import Position


class ComponentRegistry:
    _cbit = 0
    _map = {}

    def register(self, component):
        setattr(component, "ckey", component.name)
        setattr(component, "cbit", self._cbit)
        self._cbit += 1
        assert component.ckey, "Component has no ckey"
        self._map[component.ckey] = component


class Engine:

    def __init__(self):
        self.components = ComponentRegistry()
        self.prefabs = None


if __name__ == '__main__':
    ecs = Engine()
