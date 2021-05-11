from __future__ import annotations
from typing import *
from types import SimpleNamespace
from dataclasses import dataclass

if TYPE_CHECKING:
    from ecstremity.entity import Entity


# @dataclass
# class EventData:
#     """Extensible base class to normalize EntityEvent interface."""
#     instigator: Entity = None
#     target: Union[Tuple[int, int], Entity, Iterable[Entity]] = None
#     interactions: List[Dict[str, str]] = None
#     goal: Component = None
#     callback: Callable[[Any], Any] = None
#     cost: float = None


class EventData(SimpleNamespace):

    _record: List[str] = []

    def __init__(self, /, **kwargs: Dict[str, Any]) -> None:
        super().__init__(**kwargs)
        self._record = [k for k in kwargs.keys()]

    def update_record(self, key):
        if key not in self._record:
            self._record.append(key)

    def get_record(self):
        namespace = super().__dict__
        return {k: namespace[k] for k in self._record}

    def __setattr__(self, key, value):
        self.update_record(key)
        super().__dict__.update({key: value})


class EntityEvent:

    def __init__(self, name: str, data: Dict[str, Any] = None):
        self.name = name
        # self._data = SimpleNamespace(**data)
        self._data = EventData(**data)

        self._prevented: bool = False
        self._handled: bool = False
        self._routed: bool = False

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value: Dict[str, Any]):
        self._data = EventData(**value)

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

    def route(self, new_event: str, target: Entity):
        self._routed = True
        if not self.data.target:
            raise ValueError("Routed events require a target entity!")
        else:
            return target.fire_event(new_event, self.data)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, EntityEvent):
            return self.name == other.name
