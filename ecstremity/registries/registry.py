from __future__ import annotations
from typing import *
from collections import defaultdict

if TYPE_CHECKING:
    from ecstremity.engine import Engine, EngineAdapter


class Registry(defaultdict):

    def __init__(self, ecs: Union[Engine, EngineAdapter], **kwargs) -> None:
        super().__init__(**kwargs)
        self.ecs: Union[Engine, EngineAdapter] = ecs
