from __future__ import annotations
from typing import *

from ecstremity.component_registry import ComponentRegistry
from ecstremity.world import World


class Engine:

    def __init__(self, client=None):
        self.client = client
        self.components = ComponentRegistry(self)

    def register_component(self, component):
        self.components.register(component)

    def create_world(self):
        return World(self)

    def destroy_world(self):
        pass
