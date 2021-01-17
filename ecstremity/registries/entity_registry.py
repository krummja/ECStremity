from __future__ import annotations
from typing import Dict, Optional, ValuesView

from ecstremity.entity import Entity
from .registry import Registry


class EntityRegistry(Registry):

    @property
    def get_all(self) -> ValuesView[Entity]:
        return self.values()

    def create(self, uid: Optional[str] = None) -> Entity:
        """Create a new Entity and register it with the EntityRegistry."""
        entity = Entity(self.ecs, uid)
        self.register(entity)
        return entity

    def create_or_get_by_id(self, uid: str) -> Entity:
        """Look up an Entity by UID. If the Entity does not exist, it will be
        created.
        """
        entity = self.get(uid)
        if entity:
            return entity
        return self.create(uid)

    def destroy(self, uid: str) -> None:
        """Trigger an entity to self-destruct (including all attached
        Components).
        """
        self[uid].destroy()

    def on_entity_destroyed(self, entity: Entity) -> None:
        """Callback for entity self-destruct."""
        print(f"Destroying {entity}")
        del self[entity.uid]

    def register(self, entity: Entity) -> Entity:
        """Register an Entity with the EntityRegistry."""
        self[entity.uid] = entity
        return entity

    def serialize(self, entities):
        """TODO"""
        pass

    def deserialize(self, data):
        """TODO"""
        pass

    def deserialize_entity(self, data):
        """TODO"""
        pass
