from __future__ import annotations
from typing import *

import pickle
import pickletools
import lzma

if TYPE_CHECKING:
    from ecstremity.world import World
    from ecstremity.entity import Entity
    from ecstremity.entity_event import EntityEvent


class ComponentMeta(type):

    def __new__(mcs, clsname, bases, clsobj):
        clsobj = super().__new__(mcs, clsname, bases, clsobj)
        clsobj.comp_id = str(clsname).upper()
        return clsobj

    def __getnewargs__(self):
        return self.comp_id


class Component(metaclass=ComponentMeta):
    allow_multiple: bool = False
    _cbit: int = 0
    _client = None
    _entity: Entity = None
    _world: World

    @property
    def cbit(self) -> int:
        return self._cbit

    @cbit.setter
    def cbit(self, value: int) -> None:
        self._cbit = value

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value

    @property
    def entity(self) -> Entity:
        return self._entity

    @entity.setter
    def entity(self, value: Entity) -> None:
        self._entity = value

    @property
    def world(self) -> World:
        return self._entity.world

    def destroy(self) -> None:
        self.entity.destroy()

    def on_attached(self, entity: Entity) -> None:
        pass

    def on_destroyed(self) -> None:
        pass

    def on_event(self, evt: EntityEvent) -> EntityEvent:
        pass

    def _on_attached(self, entity: Entity) -> None:
        self.entity = entity
        self.on_attached(entity)

    def _on_destroyed(self) -> None:
        self.on_destroyed()
        self.entity = None

    def _on_event(self, evt: EntityEvent) -> Any:
        self.on_event(evt)
        try:
            handler = getattr(self, f"on_{evt.name}")
            return handler(evt)
        except Exception:
            return None
