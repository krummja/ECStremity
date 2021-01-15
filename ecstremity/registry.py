from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine


class Registry:

    def __init__(self, ecs: Engine) -> None:
        self.ecs = ecs
