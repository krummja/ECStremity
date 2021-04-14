from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from ecstremity.world import World
    from ecstremity.entity import Entity


class ComponentMeta(type):

    def __new__(mcs, clsname, bases, clsobj):
        clsobj = super().__new__(mcs, clsname, bases, clsobj)
        clsobj.name = str(clsname).upper()
        return clsobj


class Component(metaclass=ComponentMeta):
    _allow_multiple: bool = False
    _world: World
    _cbit: int
    _entity: Entity = None
    _client = None

    @property
    def allow_multiple(self) -> bool:
        return self._allow_multiple

    @property
    def world(self) -> World:
        return self._entity.world

    @property
    def cbit(self) -> int:
        return self._cbit

    @cbit.setter
    def cbit(self, value) -> None:
        self._cbit = value

    @property
    def entity(self) -> Entity:
        return self._entity

    @entity.setter
    def entity(self, value: Entity) -> None:
        self._entity = value

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value

    def destroy(self):
        pass

    def _on_event(self, evt: EntityEvent) -> Any:
        self.on_event(evt)
        try:
            handler = getattr(self, f"on_{evt.name}")
            return handler(evt)
        except Exception:
            return None

    def _on_attached(self):
        pass

    def _on_destroyed(self):
        pass

    def on_attached(self):
        pass

    def on_destroyed(self):
        pass

    def on_event(self, evt):
        pass
