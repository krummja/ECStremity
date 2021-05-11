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


def make_signature(names):
    return Signature(
        [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names]
    )


class ComponentMeta(type):

    def __new__(mcs, clsname, bases, clsobj):
        clsobj = super().__new__(mcs, clsname, bases, clsobj)
        clsobj.comp_id = str(clsname).upper()
        return clsobj

    def __call__(cls, *args, **kwargs):
        names = []
        names.extend(args)
        if kwargs:
            names.extend([name for name in kwargs.keys()])

        setattr(cls, "__signature__", make_signature(names))
        bound = cls.__signature__.bind(*args, **kwargs)
        setattr(cls, "__init_props__", [(n, v) for n, v in bound.arguments.items()])
        return super().__call__(*args, **kwargs)


class Component(metaclass=ComponentMeta):
    allow_multiple: bool = False
    _cbit: int = 0
    _client = None
    _entity: Entity = None
    _world: World

    @property
    def init_props(self):
        return self.__init_props__

    def __getnewargs__(self):
        return self.comp_id

    def __getstate__(self):
        component_state = {}
        for name, _ in self.init_props:
            component_state[name] = getattr(self, name)
        return component_state

    def __setstate__(self, state):
        for k, v in state.items():
            setattr(self, k, v)

    def __str__(self):
        return str(self.comp_id) + ": " + str(self.__getstate__())

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
        except AttributeError:
            return None
        except Exception:
            traceback.print_exc(file=sys.stderr)
