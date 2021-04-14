from __future__ import annotations
from typing import *
from collections import OrderedDict
from ecstremity.bit_util import *
from ecstremity.entity_event import EntityEvent

from ecstremity.component import Component

if TYPE_CHECKING:
    from ecstremity.world import World


def attach_component(entity: Entity, component: Component) -> None:
    entity.components[component.name] = component
    component.entity = entity


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

    def add(self, component: Union[Component, str], properties: Dict[str, Any]) -> None:
        if isinstance(component, str):
            component = self.world.engine.components[component.upper()]
        component = component(**properties)
        attach_component(self, component)

        self._cbits = add_bit(self._cbits, component.cbit)
        component.on_attached()
        self.candidacy()

    def has(self, component: Union[Component, str]) -> bool:
        if isinstance(component, str):
            component = self.world.engine.components[component.upper()]
        return has_bit(self._cbits, component.cbit)

    def remove(self, component):
        pass

    def destroy(self):
        pass

    def fire_event(self, name: str, data: Optional[EntityEvent]) -> EntityEvent:
        evt = EntityEvent(name, data)
        for component in self.components.values():
            component._on_event(evt)
            if evt.prevented:
                return evt
        return evt

    def __getitem__(self, component: Union[Component, str]):
        if isinstance(component, Component):
            component = component.name
        return self.components[component.upper()]

    def __repr__(self):
        component_list = ", ".join(self.components.keys())
        return f"Entity [{self.uid}] with [{component_list}]"
