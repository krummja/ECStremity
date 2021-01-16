from __future__ import annotations
from typing import Any, Dict, Optional, TYPE_CHECKING, Union, List

from collections import  defaultdict

from ecstremity import Component

if TYPE_CHECKING:
    from ecstremity import Engine


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
            component = self.ecs.components[component]
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

    def has(self, component: Union[str, Component]):
        """Check if a Component is currently attached to this Entity."""
        try:
            if isinstance(component, str):
                components = self[component]
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
            return self[component].remove()
        return self[component].remove()

    def serialize(self):
        pass

    def __getitem__(self, component: Union[str, Component]) -> Component:
        if not isinstance(component, str):
            component = component.name
        return super().__getitem__(component.upper())
