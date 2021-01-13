from __future__ import annotations
from typing import Dict, TYPE_CHECKING, ValuesView

from registries.registry import Registry

if TYPE_CHECKING:
    from entity import Entity
    from engine import Engine


class EntityRegistry(Registry):
    _entities: Dict[str, Entity] = {}

    @property
    def all(self) -> ValuesView[Entity]:
        return self._entities.values()

    def register(self, entity: Entity) -> Entity:
        self._entities[entity.uid] = entity
        return entity

    def create(self, uid: str) -> Entity:
        entity = Entity(uid, self.ecs)
        self.register(entity)
        return entity

    def destroy(self, uid: str) -> None:
        self._entities[uid].destroy()

    def get(self, uid: str) -> Entity:
        return self._entities[uid]

    def on_entity_destroyed(self, entity: Entity) -> None:
        del self._entities[entity.uid]
