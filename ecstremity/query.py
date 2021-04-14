from __future__ import annotations
from typing import *
from ecstremity.bit_util import *
from functools import reduce

if TYPE_CHECKING:
    from ecstremity.world import World


class Query:
    _cache = []

    def __init__(
            self,
            world: World,
            any_of: Optional[List[str]] = None,
            all_of: Optional[List[str]] = None,
            none_of: Optional[List[str]] = None
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

    def idx(self, entity):
        try:
            return self._cache.index(entity)
        except ValueError:
            return -1

    def matches(self, entity):
        bits = entity.cbits
        any_of = self._any == 0 or bit_intersection(bits, self._any) > 0
        all_of = bit_intersection(bits, self._all) == self._all
        none_of = bit_intersection(bits, self._none) == self._none
        return any_of & all_of & none_of

    def candidate(self, entity):
        idx = self.idx(entity)
        is_tracking = idx >= 0

        if self.matches(entity):
            if not is_tracking:
                self._cache.append(entity)
            return True

        if is_tracking:
            self._cache[idx] = 1
        return False

    def refresh(self):
        self._cache = []
        for entity in self.world.entities:
            self.candidate(entity)

    def result(self):
        return self._cache
