from __future__ import annotations
from typing import *

import json
import lzma
import pickle
import pickletools
import math

from uuid import uuid1
from collections import OrderedDict, deque, ValuesView

from ecstremity.entity import Entity
from ecstremity.query import Query
from ecstremity.component import Component

from uuid import UUID

if TYPE_CHECKING:
    from ecstremity.query import QueryType
    from ecstremity.engine import Engine


def deque_filter(
        lst: Deque[Any],
        condition: Callable[..., bool],
        replace: Optional[Callable[[Any], Component]] = None
    ) -> QueryType:
    lst = deque(lst)
    for _ in range(len(lst)):
        item = lst.popleft()
        if condition(item):
            if replace:
                item = replace(item)
            lst.append(item)
    return list(lst)


class World:

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        self._id = 0
        self._queries: List[Query] = []
        self._entities: OrderedDict[str, Entity] = OrderedDict()

    @property
    def entities(self) -> ValuesView[Entity]:
        return self._entities.values()

    @staticmethod
    def create_uid() -> str:
        return str(uuid1())

    def get_entity(self, uid: str) -> Optional[Entity]:
        return self._entities.get(uid)

    def create_entity(self, uid: Optional[str] = None) -> Entity:
        if not uid:
            uid = self.create_uid()
        assert uid is not None
        entity = Entity(self, uid)
        self._entities[uid] = entity
        return entity

    def destroy_entity(self, uid: str) -> None:
        entity = self._entities[uid]
        if entity:
            entity.destroy()

    def destroy_entities(self) -> None:
        """Destroy all entities in the world."""
        to_destroy: List[Entity] = []
        entities: ValuesView[Entity] = self._entities.values()
        for entity in entities:
            _entity: Optional[Entity] = self.get_entity(entity.uid)
            if _entity is not None:
                to_destroy.append(_entity)
        for entity in to_destroy:
            entity.destroy()

    def destroy(self) -> None:
        """Muahahaha!"""
        self.destroy_entities()
        self._id = 0
        self._queries = []
        self._entities = OrderedDict()

    def create_query(
            self,
            any_of: Optional[Deque[str]] = None,
            all_of: Optional[Deque[str]] = None,
            none_of: Optional[Deque[str]] = None,
        ) -> Query:

        # ANY OF
        if any_of and isinstance(any_of[0], str):
            _any_of: QueryType = deque_filter(
                any_of,
                (lambda i: isinstance(i, str)),
                (lambda i: self.engine.components[i.upper()]))
        else:
            _any_of = []

        # ALL OF
        if all_of and isinstance(all_of[0], str):
            _all_of: QueryType = deque_filter(
                all_of,
                (lambda i: isinstance(i, str)),
                (lambda i: self.engine.components[i.upper()]))
        else:
            _all_of = []

        # NONE OF
        if none_of and isinstance(none_of[0], str):
            _none_of: QueryType = deque_filter(
                none_of,
                (lambda i: isinstance(i, str)),
                (lambda i: self.engine.components[i.upper()]))
        else:
            _none_of = []

        query = Query(self, _any_of, _all_of, _none_of)  # type: ignore
        self._queries.append(query)
        return query

    def candidate(self, entity: Entity) -> None:
        for query in self._queries:
            query.candidate(entity)

    def destroyed(self, uid: str) -> None:
        try:
            self._entities.pop(uid)
        except KeyError:
            pass

    def create_prefab(self, name: str, properties: Optional[Dict[str, Any]] = None, uid: Optional[str] = None):
        if not properties:
            properties = {}
        return self.engine.prefabs.create(self, name, properties, uid)

    def serialize(self, entities: Optional[OrderedDict[str, Entity]] = None) -> Dict[str, Any]:
        json:  List[Dict[str, Union[str, Dict[str, Any]]]] = []  # FIXME: Create a type for this lmao wow
        entities = entities if entities else self._entities
        for entity in entities.values():
            json.append(entity.serialize())
        return {
            "entities": json
        }

    def deserialize(self, data) -> None:
        for entity_data in data["entities"]:
            self._create_or_get_by_uid(entity_data["uid"])

        for entity_data in data["entities"]:
            self.deserialize_entity(entity_data)

    def _create_or_get_by_uid(self, uid: str) -> Entity:
        entity: Optional[Entity] = self.get_entity(uid)
        if entity is not None:
            return entity
        else:
            return self.create_entity(uid)

    def deserialize_entity(self, data: Dict[str, Any]) -> None:
        uid: str = data["uid"]
        components: Dict[str, bytes] = data["components"]
        entity = self._create_or_get_by_uid(uid)
        entity._qeligible = False
        for comp_id, comp_props in components.items():
            entity.add(comp_id, {k: v for k, v in comp_props.items() if k[0] != "_"})
        entity._qeligible = True
        entity.candidacy()
