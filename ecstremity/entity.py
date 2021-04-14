from __future__ import annotations
from typing import *
from collections import OrderedDict
from ecstremity.bit_util import *

if TYPE_CHECKING:
    from ecstremity.component import Component
    from ecstremity.world import World


def attach_component(entity: Entity, component: Component) -> None:
    entity.components[component.name] = component


def attach_component_keyed(entity: Entity, component: Component) -> None:
    if component.name not in entity.components.keys():
        entity.components[component.name] = {}


def attach_component_array(entity, component):
    pass


def remove_component(entity, component):
    pass


def remove_component_keyed(entity, component):
    pass


def remove_component_array(entity, component):
    pass


class Entity:

    def __init__(self, world: World, uid: str):
        self.world = world
        self.uid = uid
        self.components = OrderedDict()
        self.is_destroyed = False
        self._cbits = 0
        self._qeligible = True

    @property
    def cbits(self):
        return self._cbits

    def candidacy(self):
        if self._qeligible:
            self.world.candidate(self)

    def add(self, component_class: Component, properties: Dict[str, Any]) -> None:
        component = component_class(**properties)
        # TODO Add additional attachment types
        attach_component(self, component)

        self._cbits = add_bit(self._cbits, component.cbit)
        component.on_attached()
        self.candidacy()

    def has(self, component: Component):
        return has_bit(self._cbits, component.cbit)

    def remove(self, component):
        pass

    def destroy(self):
        pass

    def fire_event(self, name, data):
        pass
