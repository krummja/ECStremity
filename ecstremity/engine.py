from __future__ import annotations
from typing import *

from ecstremity.component_registry import ComponentRegistry
from ecstremity.prefab_registry import PrefabRegistry
from ecstremity.world import World

if TYPE_CHECKING:
    from ecstremity.component import Component


class Engine:

    def __init__(self, client=None):
        self.client = client
        self.components = ComponentRegistry(self)
        self.prefabs = PrefabRegistry(self)

    def register_component(self, component: Component):
        self.components.register(component)

    def register_prefab(self, prefab):
        self.prefabs.register(prefab.name, prefab)

    def create_world(self) -> World:
        return World(self)

    @staticmethod
    def destroy_world(world: World):
        world.destroy()
