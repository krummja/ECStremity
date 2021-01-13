from __future__ import annotations
from typing import Any, Dict, Optional, ValuesView, TYPE_CHECKING
from uuid import uuid1

from registries.component_registry import ComponentRegistry
from registries.entity_registry import EntityRegistry

if TYPE_CHECKING:
    from component import Component
    from ecs.entity import Entity


class Engine:

    def __init__(self) -> None:
        self.components = ComponentRegistry(self)
        self.entities = EntityRegistry(self)

    def generate_uid(self) -> str:
        """Generate a new unique identifier for an `Entity`."""
        return uuid1().hex

    def create_entity(self, uid: str) -> Entity:
        """Use the `EntityRegistry` to create a new `Entity` with the specified `uid`."""
        return self.entities.create(uid)

    def get_entity(self, uid: str) -> Entity:
        """Use a `uid` to return an `Entity` from the `EntityRegistry`."""
        return self.entities.get(uid)

    def delete_entity(self, uid: str) -> None:
        self.entities.destroy(uid)

    def register_component(self, component: Component) -> None:
        """Register the specified `component` with the `ComponentRegistry`. Registering
        a component allows for creation of new copies using `create_component`."""
        self.components.register(component)

    def create_component(self, component_type, properties) -> Component:
        """Use the `ComponentRegistry` to create a new `Component` with the provided
        `properties` as initial values. The specified `component_type` must already be
        registered with the `ComponentRegistry`.
        """
        return self.components.create(component_type, properties)

    def create_query(self, filters):
        pass
