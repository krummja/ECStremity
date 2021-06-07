from __future__ import annotations
from typing import *

import pickle
import pickletools
import lzma
import traceback
import sys
from inspect import Signature, Parameter

if TYPE_CHECKING:
    from ecstremity.world import World
    from ecstremity.entity import Entity
    from ecstremity.entity_event import EntityEvent


class ComponentMeta(type):

    def __new__(mcs, clsname: str, bases: Tuple[type, ...], clsobj: Any) -> Any:
        clsobj = super().__new__(mcs, clsname, bases, clsobj)
        setattr(clsobj, "__component_id__", None)
        clsobj.__component_id__ = str(clsname).upper()
        return clsobj


class Component(metaclass=ComponentMeta):

    allow_multiple: bool = False
    _cbit: int = 0
    _client: Optional[Any] = None
    _entity: Optional[Entity] = None
    _world: World

    __component_id__: str

    def __getstate__(self) -> Dict[str, Any]:
        state = {k: v for k, v in self.__dict__.items() if k[0] != "_"}
        return state

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self.__dict__ = state

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Component):
            return self._cbit == other._cbit
        return False

    def __str__(self) -> str:
        return str(self.comp_id) + ": " + str(self.__getstate__())

    @property
    def comp_id(self) -> str:
        return self.__component_id__

    @property
    def cbit(self) -> int:
        return self._cbit

    @cbit.setter
    def cbit(self, value: int) -> None:
        self._cbit = value

    @property
    def client(self) -> Optional[Any]:
        return self._client

    @client.setter
    def client(self, value: Any) -> None:
        self._client = value

    @property
    def entity(self) -> Optional[Entity]:
        return self._entity

    @entity.setter
    def entity(self, value: Entity) -> None:
        self._entity = value

    @property
    def world(self) -> Optional[World]:
        if self._entity is not None:
            return self._entity.world
        return None

    def destroy(self) -> None:
        if self.entity is not None:
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
        except AttributeError:
            return None
        except Exception:
            traceback.print_exc(file=sys.stderr)

    def serialize(self) -> Dict[str, Any]:
        return {self.comp_id: self.__getstate__()}
