from __future__ import annotations
from typing import TYPE_CHECKING

from collections import  defaultdict

if TYPE_CHECKING:
    from engine import Engine


class Registry(defaultdict):

    def __init__(self, ecs: Engine) -> None:
        self.ecs = ecs
