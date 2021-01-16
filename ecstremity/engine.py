from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from uuid import uuid1

from ecstremity.registries import ComponentRegistry, EntityRegistry

if TYPE_CHECKING:
    from ecstremity import Component, Entity


class Engine:

    def __init__(self) -> None:
        self.components = ComponentRegistry(self)
        self.entities = EntityRegistry(self)

    def generate_uid(self) -> str:
        """Generate a new unique identifier for an `Entity`."""
        return uuid1().hex

    def get_entity(self, uid: str) -> Entity:
        """Use a `uid` to return an `Entity` from the `EntityRegistry`."""
        return self.entities.get(uid)

    def create_component(self, component, properties) -> Component:
        return self.components.create(component, properties)

    def create_entity(self, uid: Optional[str] = None) -> Entity:
        """Use the `EntityRegistry` to create a new `Entity` with the
        specified `uid`.
        """
        return self.entities.create(uid)

    def create_prefab(self, name_or_class, initial_props=None):
        pass

    def create_query(self, filters):
        pass

    def destroy_entity(self, uid: str) -> None:
        self.entities.destroy(uid)

    def register_component(self, component: Component) -> None:
        self.components.register(component)

    def register_prefab(self, prefab):
        pass

    def serialize(self, entities):
        pass

    def deserialize(self, data):
        pass
