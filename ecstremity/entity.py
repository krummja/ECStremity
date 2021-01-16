from __future__ import annotations
from typing import Any, Dict, Optional, TYPE_CHECKING, Union, List

from collections import  defaultdict

from ecstremity.component import Component

if TYPE_CHECKING:
    from engine import Engine


class Entity(defaultdict):

    def __init__(self, ecs: Engine, uid: Optional[str] = None) -> None:
        self.ecs = ecs
        self.uid = uid if uid is not None else self.ecs.generate_uid()
        self._is_destroyed: bool = False

    @property
    def is_destroyed(self) -> bool:
        return self._is_destroyed

    @property
    def components(self):
        return self.items()

    def add(self, component: Union[str, Component], properties: Dict[str, Any]) -> bool:
        if isinstance(component, str):
            component = self.ecs.components[component.upper()]
        component = self.ecs.create_component(component, properties)
        return self._attach(component)

    def _attach(self, component: Component) -> bool:
        self[component.name] = component
        component._on_attached(self)
        return True

    def destroy(self):
        self._is_destroyed = True
        for component in self.values():
            component.destroy()
        self.ecs.entities.on_entity_destroyed(self)

    def get(self, component: Union[str, Component]):
        """Get a Component currently attached to this Entity.

        Components can be accessed by passing in either the string name of the
        Component, or the class symbol directly. If the Entity has multiple of
        the Component, access a particular one by supplying a `key` parameter,
        or leave it unfilled to return all of the specified Component.
        """

    def has(self, component: Union[str, Component]):
        """Check if a Component is currently attached to this Entity."""
        try:
            if isinstance(component, str):
                components = self[component.upper()]
            else:
                components = self[component.name]
            if components:
                return True
        except KeyError:
            return False

    def owns(self, component: Component) -> bool:
        """Check if target Component has this Entity as an owner."""
        return component.entity == self

    def remove(self, component: Union[str, Component]) -> Optional[Component]:
        if isinstance(component, str):
            return self[component.upper()].remove()
        return self[component].remove()


    def serialize(self):
        pass

    def fire_event(self, name: str, data):
        pass
