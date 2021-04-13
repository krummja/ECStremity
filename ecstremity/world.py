from __future__ import annotations
from typing import *
from collections import OrderedDict

if TYPE_CHECKING:
    from ecstremity.engine import Engine


class World:

    def __init__(self, engine: Engine):
        self.engine = engine
        self._id = 0
        self._queries = []
        self._entities = OrderedDict([])

    def create_uid(self):
        pass

    def get_entity(self, uid):
        return self._entities.get(uid)

    def get_entities(self):
        return self._entities.values()

    def create_entity(self):
        pass

    def destroy_entity(self):
        pass

    def destroy_entities(self):
        pass

    def create_query(self):
        pass

    def create_prefab(self):
        pass

    def _candidate(self, entity):
        pass

    def _destroyed(self, uid):
        pass
