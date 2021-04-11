from __future__ import annotations
from typing import *

from collections import defaultdict

if TYPE_CHECKING:
    from engine import Engine, EngineAdapter


class Registry(defaultdict):

    def __init__(self, ecs: Union[Engine, EngineAdapter]) -> None:
        self.ecs: Union[Engine, EngineAdapter] = ecs
