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
        setattr(clsobj, "comp_id", str(clsname).upper())
        return clsobj


class Component(metaclass=ComponentMeta):
    """Base Component class. Do not instance this class directly, but rather
    inherit from it to make your own custom Components.

    A new Component should always supply an __init__ method. Parameters to
    __init__ must bound to the instance (i.e. parameter 'a' must have 'self.a'
    inside __init__). These variables will be stored in the Component's
    state to be utilized during serialization. Instance variables prefixed
    with "_" are excluded, so prefix any instance variables not declared as
    parameters to __init__ in this way.

        class Position(Component):

            def __init__(self, x: int, y: int) -> None:
                self.x = x
                self.y = y
                self._pathing: bool = False

            @property
            def pathing(self) -> bool:
                return self._pathing

            @pathing.setter
            def pathing(self, value: bool) -> None:
                self._pathing = value

    In the Position example, the parameters `x` and `y` will be used to
    construct the Component from a prefab definition. Because the instance
    variable `_pathing` is not a declared parameter, it is declared with a
    prefixed '_', and is accessed via a getter/setter on the class instead.
    """

    allow_multiple: bool = False
    _cbit: int = 0
    _client: Optional[Any] = None
    _entity: Optional[Entity] = None
    _world: World

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
