from __future__ import annotations
from typing import Dict, Optional, ValuesView

from ecstremity.registry import Registry
from ecstremity.entity import Entity


class EntityRegistry(Registry):
    _entities: Dict[str, Entity] = {}

    @property
    def all(self) -> ValuesView[Entity]:
        return self._entities.values()

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
        self._entities[uid].destroy()

    def get(self, uid: str) -> Entity:
        """Search for an entity by UID."""
        return self._entities[uid]

    def on_entity_destroyed(self, entity: Entity) -> None:
        """Callback for entity self-destruct."""
        del self._entities[entity.uid]

    def register(self, entity: Entity) -> Entity:
        """Register an Entity with the EntityRegistry."""
        self._entities[entity.uid] = entity
        return entity

    def cleanup_refs(self):
        pass

    def add_ref(self):
        pass

    def remove_ref(self):
        pass

    def serialize(self, entities):
        pass

    def deserialize(self, data):
        pass

    def deserialize_entity(self, data):
        pass
