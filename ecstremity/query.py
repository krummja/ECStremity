from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ecstremity.engine import Engine
    from ecstremity.entity import Entity


class Query:
    """Base Query class."""

    def __init__(
            self,
            ecs: Engine,
            any_of: Optional[List[str]] = None,
            all_of: Optional[List[str]] = None,
            none_of: Optional[List[str]] = None
        ) -> None:
        self._ecs = ecs
        self.query_filter = {
            'any_of': any_of if any_of is not None else [],
            'all_of': all_of if all_of is not None else [],
            'none_of': none_of if none_of is not None else []
            }
        self._on_entity_added_cbs = []
        self._on_entity_removed_cbs = []
        self._cache = []

    @property
    def cache(self):
        return self._cache

    def is_match(self, entity: Entity):
        if len(self.query_filter['any_of']) >= 1:
            has_any = any([entity.has(c) for c in self.query_filter['any_of']])
        else:
            has_any = True

        has_all = all([entity.has(c) for c in self.query_filter['all_of']])

        if len(self.query_filter['none_of']) >= 1:
            has_none = not all([entity.has(c) for c in self.query_filter['none_of']])
        else:
            has_none = True
        return has_any and has_all and has_none

    def on_entity_added(self, cb):
        self._on_entity_added_cbs.append(cb)

    def on_entity_removed(self, cb):
        self._on_entity_removed_cbs.append(cb)

    def has(self, entity: Entity) -> bool:
        if entity in self._cache:
            return True
        return False

    def candidate(self, entity: Entity):
        is_tracking = self.has(entity)

        if self.is_match(entity):
            if not is_tracking:
                self._cache.append(entity)
                for cb in self._on_entity_added_cbs:
                    cb(entity)
            return True

        if is_tracking:
            self._cache.remove(entity)
            for cb in self._on_entity_removed_cbs:
                cb(entity)

        return False

    def _on_entity_created(self, entity: Entity):
        self.candidate(entity)

    def _on_component_added(self, entity: Entity):
        self.candidate(entity)

    def _on_component_removed(self, entity: Entity):
        self.candidate(entity)

    def _on_entity_destroyed(self, entity: Entity):
        if self.has(entity):
            self._cache.remove(entity)
            for cb in self._on_entity_removed_cbs:
                cb(entity)

    def bust_cache(self):
        self._cache.clear()
        for entity in self._ecs.entities.items():
            self.candidate(entity)
        return self._cache
