from __future__ import annotations
from typing import *
from ecstremity.bit_util import *
from functools import reduce

from ecstremity.component import Component

if TYPE_CHECKING:
    from ecstremity.entity import Entity
    from ecstremity.component import Component
    from ecstremity.world import World


def from_name(world: World, component_name: str) -> Component:
    return world.engine.components[component_name]


QueryType = Optional[List[Component]]


class Query:
    _cache: List[Entity] = []

    def __init__(
            self,
            world: World,
            any_of: QueryType = None,
            all_of: QueryType = None,
            none_of: QueryType = None
    ) -> None:
        self._cache = []
        self.world = world
        self.any_of = any_of if any_of is not None else []
        self.all_of = all_of if all_of is not None else []
        self.none_of = none_of if none_of is not None else []

        self._any = reduce(lambda a, b: add_bit(a, b.cbit), self.any_of, 0)
        self._all = reduce(lambda a, b: add_bit(a, b.cbit), self.all_of, 0)
        self._none = reduce(lambda a, b: add_bit(a, b.cbit), self.none_of, 0)

        self.refresh()

    def idx(self, entity: Entity) -> int:
        try:
            return self._cache.index(entity)
        except ValueError:
            return -1

    def matches(self, entity: Entity) -> bool:
        bits = entity.cbits
        any_of = self._any == 0 or bit_intersection(bits, self._any) > 0
        all_of = bit_intersection(bits, self._all) == self._all
        none_of = bit_intersection(bits, self._none) == 0
        return any_of & all_of & none_of

    def candidate(self, entity: Entity) -> bool:
        idx = self.idx(entity)
        is_tracking = idx >= 0

        if self.matches(entity):
            if not is_tracking:
                self._cache.append(entity)
            return True

        if is_tracking:
            del self._cache[idx]
        return False

    def refresh(self) -> None:
        self._cache = []
        for entity in self.world.entities:
            self.candidate(entity)

    @property
    def result(self) -> List[Entity]:
        return self._cache
