from __future__ import annotations
from typing import *
from dataclasses import dataclass

if TYPE_CHECKING:
    from .entity import Entity


@dataclass
class EventData:
    """Extensible base class to normalize EntityEvent interface."""
    instigator: Entity = None
    target: Union[Tuple[int, int], Entity] = None
    interactions: List[Dict[str, str]] = None
    cost: float = None


class EntityEvent:

    def __init__(self, name: str, data: EventData = None):
        self.name = name
        self.data = data

        self._prevented: bool = False
        self._handled: bool = False
        self._routed: bool = False

    @property
    def prevented(self) -> bool:
        """`prevented` property"""
        return self._prevented

    @property
    def handled(self) -> bool:
        """`handled` property"""
        return self._handled

    @property
    def routed(self) -> bool:
        return self._routed

    def handle(self) -> None:
        """Callback for `_handled` and `_prevented` attributes."""
        self._handled = True
        self._prevented = True

    def prevent(self) -> None:
        """Callback for `_prevented` attribute."""
        self._prevented = True

    def route(self, target: Entity):
        self._routed = True
        name = self.name
        if self.name[:4] == 'fwd_':
            name = self.name[4:]
        else:
            print(f"Expected event prefixed with `fwd_`, got {name} instead.")

        if not self.data.target:
            raise ValueError("Routed events require a target entity!")
        else:
            return target.fire_event(name, self.data)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, EntityEvent):
            return self.name == other.name
