from __future__ import annotations
from typing import *
from collections import OrderedDict
import pickle
import pickletools
import lzma
import json

from ecstremity.bit_util import *
from ecstremity.entity_event import EntityEvent

from ecstremity.component import Component

if TYPE_CHECKING:
    from ecstremity.entity_event import EventData
    from ecstremity.world import World


def attach_component(entity: Entity, component) -> None:
    entity.components[component.name] = component


def remove_component(entity, component_name: str):
    component = entity.components[component_name.upper()]
    del entity.components[component_name.upper()]
    entity.cbits = subtract_bit(entity.cbits, component.cbit)
    entity.candidacy()


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

    @cbits.setter
    def cbits(self, value):
        self._cbits = value

    def candidacy(self):
        """Check this entity against the existing queries in the active world."""
        if self._qeligible:
            self.world.candidate(self)

    def add(self, component: Union[Component, str], properties: Dict[str, Any]) -> None:
        """Create and add a registered component to the entity initialized with
        the specified properties.
        A component instance can be supplied instead.
        """
        if isinstance(component, str):
            component = self.world.engine.components[component.upper()]
        component = component(**properties)
        attach_component(self, component)

        self._cbits = add_bit(self._cbits, component.cbit)
        component._on_attached(self)
        self.candidacy()

    def has(self, component: Union[Component, str]) -> bool:
        """Check if a particular component is currently attached to this Entity."""
        if isinstance(component, str):
            component = self.world.engine.components[component.upper()]
        return has_bit(self._cbits, component.cbit)

    def owns(self, component: Union[Component, str]) -> bool:
        """Check if target component has this entity as an owner."""
        if isinstance(component, str):
            component = self.world.engine.components[component.upper()]
        return component.entity == self

    def remove(self, component):
        """Remove a component from the entity."""
        if isinstance(component, str):
            remove_component(self, component)
        else:
            remove_component(self, component.name)

    def destroy(self):
        """Destroy this entity and all attached components."""
        to_destroy = []
        for name, component in self.components.items():
            to_destroy.append(component)

        for component in to_destroy:
            self.remove(component)
            component._on_destroyed()

        self.world.destroyed(self.uid)
        self.components.clear()
        self.is_destroyed = True

    def fire_event(self, name: str, data: Optional[EventData]) -> EntityEvent:
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
