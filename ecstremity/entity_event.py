from __future__ import annotations
from typing import *
from types import SimpleNamespace
from dataclasses import dataclass

if TYPE_CHECKING:
    from ecstremity.entity import Entity


class EventData(SimpleNamespace):

    _record: List[str] = []

    def __init__(self, /, **kwargs: Dict[str, Any]) -> None:
        super().__init__(**kwargs)
        self._record = [k for k in kwargs.keys()]

    def __setattr__(self, key, value):
        self.update_record(key)
        super().__dict__.update({key: value})

    def update_record(self, key):
        if key not in self._record:
            self._record.append(key)

    def get_record(self):
        namespace = super().__dict__
        return {k: namespace[k] for k in self._record}


class EntityEvent:

    def __init__(self, name: str, data: Dict[str, Any] = None):
        """An event to be broadcast to all of an Entity's components.

        All events must be given a name so that they can be accessed inside
        a Component's listener methods. For example, if an event is fired as
        `Entity.fire_event("get_data")`, then some Component on that Entity
        must have a corresponding method `on_get_data`.

        Event data is optional, and is simply passed in as a dict. The event
        data may be accessed inside of a listener by grabbing the `data`
        attribute of the Event:

            class SomeComponent(Component):
                def some_behavior(self) -> None:
                    self.entity.fire_event("get_data", {
                        "foo": 10,
                        "bar": False,
                    })

            class OtherComponent(Component):
                def on_get_data(self, evt: EntityEvent) -> None:
                    if evt.data.foo >= 5:
                        # do something
                    if evt.data.bar:
                        # do another thing
                    evt.handle()
        """
        self.name = name
        self._data = EventData(**data)

        self._prevented: bool = False
        self._handled: bool = False
        self._routed: bool = False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, EntityEvent):
            return self.name == other.name

    def __str__(self) -> str:
        return str(self.name)

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
