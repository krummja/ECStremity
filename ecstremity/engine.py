from __future__ import annotations
from typing import *
import numpy as np

from ecstremity.component import Position, Renderable

if TYPE_CHECKING:
    from ecstremity.component import Component


class AccessorFactory:

    def __init__(self, engine: Engine) -> None:
        self.engine = engine


class ComponentRegistry:

    def __init__(self, engine: Engine, *, component_list: List[Component]):
        self.engine = engine
        self.registry = self._compose_registry_dtype(component_list)
        self.pool = {c.name: c.__class__ for c in component_list}

    @staticmethod
    def _compose_registry_dtype(component_list):
        components_dt = []
        for component in component_list:
            components_dt.append((component.name, component.ctype))
        components_dt = np.dtype(components_dt)
        return np.recarray((len(component_list,)), dtype=components_dt)


class Engine:

    def __init__(self):
        self.components = ComponentRegistry(self, component_list = [Position(), Renderable()])
        self.prefabs = None


if __name__ == '__main__':
    ecs = Engine()
    print(ecs.components.registry['RENDERABLE'])
    pos = ecs.components.pool['POSITION'](0, 1, 2)
    print(pos.xy)
    print(pos.z)
