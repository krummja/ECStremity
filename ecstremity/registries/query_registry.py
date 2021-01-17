from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING

from .registry import Registry

from ecstremity.query import Query

if TYPE_CHECKING:
    from ecstremity.entity import Entity


class QueryRegistry(Registry):

    _queries = []

    def create(
            self,
            any_of: Optional[List[str]] = None,
            all_of: Optional[List[str]] = None,
            none_of: Optional[List[str]] = None
        ) -> Query:
        query = Query(self.ecs, any_of=any_of, all_of=all_of, none_of=none_of)
        self._queries.append(query)
        return query

    def on_component_added(self, entity: Entity) -> None:
        for query in self._queries:
            query._on_component_added(entity)

    def on_component_removed(self, entity: Entity) -> None:
        for query in self._queries:
            query._on_component_removed(entity)

    def on_entity_created(self, entity: Entity) -> None:
        for query in self._queries:
            query._on_entity_created(entity)

    def on_entity_destroyed(self, entity: Entity) -> None:
        for query in self._queries:
            query._on_entity_destroyed(entity)
