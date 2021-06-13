from __future__ import annotations
from typing import TYPE_CHECKING, Union

import os
import importlib
from collections import OrderedDict

from ecstremity.component import Component, ComponentMeta

if TYPE_CHECKING:
    from ecstremity.engine import Engine


class ComponentRegistry:

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        self._cbit: int = 0
        self._map: OrderedDict[str, Component] = OrderedDict()

    def register(self, component: Component) -> None:
        """Register a Component for later construction."""
        component.cbit = self._cbit
        component.client = self.engine.client
        self._cbit += 1
        self._map[component.comp_id] = component

    def __getitem__(self, key: Union[Component, str]) -> Component:
        if isinstance(key, Component):
            return self._map[key.comp_id]
        else:
            return self._map[key.upper()]


class ComponentLoader:

    def __init__(self, path: str) -> None:
        self.path = path
        self.tree = os.listdir(f"{path}")
