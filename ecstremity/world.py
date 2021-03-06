from __future__ import annotations
from typing import *

import json
import lzma
import pickle
import pickletools
import math

from uuid import uuid1
from collections import OrderedDict, deque

from ecstremity.entity import Entity
from ecstremity.query import Query
from ecstremity.component import Component

from uuid import UUID
if TYPE_CHECKING:
    from ecstremity.engine import Engine


def deque_filter(lst, condition, replace=None):
    lst = deque(lst)
    for _ in range(len(lst)):
        item = lst.popleft()
        if condition(item):
            if replace:
                item = replace(item)
            lst.append(item)
    return lst


class World:

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        self._id = 0
        self._queries = []
        self._entities = OrderedDict()

    @property
    def entities(self):
        return self._entities.values()

    @staticmethod
    def create_uid():
        return uuid1()

    def get_entity(self, uid: str):
        return self._entities[uid]

    def get_entities(self):
        return self._entities.values()

    def create_entity(self, uid: str = None):
        if not uid:
            uid = self.create_uid()
        entity = Entity(self, uid)
        self._entities[uid] = entity
        return entity

    def destroy_entity(self, uid: str):
        entity = self._entities[uid]
        if entity:
            entity.destroy()

    def destroy_entities(self):
        """Destroy all entities in the world."""
        to_destroy = []
        for entity in self._entities:
            to_destroy.append(self.get_entity(entity))
        for entity in to_destroy:
            entity.destroy()

    def destroy(self):
        """Muahahaha!"""
        self.destroy_entities()
        self._id = 0
        self._queries = []
        self._entities = OrderedDict()

    def create_query(self, any_of=None, all_of=None, none_of=None):
        if any_of and isinstance(any_of[0], str):
            any_of = deque_filter(any_of,
                                  (lambda i: isinstance(i, str)),
                                  (lambda i: self.engine.components[i.upper()]))
        if all_of and isinstance(all_of[0], str):
            all_of = deque_filter(all_of,
                                  (lambda i: isinstance(i, str)),
                                  (lambda i: self.engine.components[i.upper()]))
        if none_of and isinstance(none_of[0], str):
            none_of = deque_filter(none_of,
                                   (lambda i: isinstance(i, str)),
                                   (lambda i: self.engine.components[i.upper()]))

        query = Query(self, any_of, all_of, none_of)
        self._queries.append(query)
        return query

    def candidate(self, entity):
        for query in self._queries:
            query.candidate(entity)

    def destroyed(self, uid: str):
        try:
            self._entities.pop(uid)
        except KeyError:
            pass

    def create_prefab(self, name: str, properties: Dict[str, Any] = None, uid: str = None):
        if not properties:
            properties = {}
        return self.engine.prefabs.create(self, name, properties, uid)

    def serialize(self, entities: OrderedDict[Entity] = None):
        json = []
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
            self._deserialize_entity(entity_data)

    def _create_or_get_by_uid(self, uid: str):
        try:
            return self.get_entity(uid)
        except KeyError:
            return self.create_entity(uid)

    def _deserialize_entity(self, data):
        uid: str = data["uid"]
        components: Dict[str, bytes] = data["components"]

        entity = self._create_or_get_by_uid(uid)
        entity._qeligible = False

        for comp_id, comp_props in components.items():
            entity.add(comp_id, {k: v for k, v in comp_props.items()})

        entity._qeligible = True
        entity.candidacy()
