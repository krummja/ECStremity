from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from ecstremity.world import World


class ComponentMeta(type):

    def __new__(mcs, clsname, bases, clsobj):
        clsobj = super().__new__(mcs, clsname, bases, clsobj)
        clsobj.name = str(clsname).upper()
        return clsobj


class Component(metaclass=ComponentMeta):
    _allow_multiple: bool = False
    _world: World
    _cbit: int

    @property
    def allow_multiple(self) -> bool:
        return self._allow_multiple

    @property
    def world(self) -> World:
        return self._world

    @world.setter
    def world(self, value: World) -> None:
        self._world = value

    @property
    def cbit(self) -> int:
        return self._cbit

    @cbit.setter
    def cbit(self, value) -> None:
        self._cbit = value

    def destroy(self):
        pass

    def _on_event(self):
        pass

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
