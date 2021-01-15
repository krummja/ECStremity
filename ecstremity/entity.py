from __future__ import annotations
from typing import Any, Dict, Optional, TYPE_CHECKING, Union, List

from ecstremity.component import Component

if TYPE_CHECKING:
    from engine import Engine


class Entity:

    def __init__(self, ecs: Engine, uid: Optional[str] = None) -> None:
        self.ecs = ecs
        self.uid = uid if uid is not None else self.ecs.generate_uid()
        self.components: Dict[str, Component] = {}
        self._is_destroyed: bool = False

    @property
    def is_destroyed(self) -> bool:
        return self._is_destroyed

    def add(
            self,
            component: Union[str, Component],
            properties: Dict[str, Any]
        ) -> bool:
        if type(component) != str:
            if isinstance(component, Component):
                if component.is_attached:
                    print(f"{component.name} cannot be added! It is already attached "
                        f"to an entity!")
                    return False
                return self._attach(component)

            if issubclass(component, Component):
                component = component.name.upper()
        component = self.ecs.create_component(component, properties)
        if not component:
            print(f"{component.name} cannot be added! It is not registered.")
            return False
        return self._attach(component)

    def _attach(self, component: Component) -> bool:
        """Use a Component type (the string name of the Component) or the class
        symbol to attach a Component to this Entity."""

        if not component.allow_multiple:
            if self.has(component):
                print(f"{component.name} cannot be added! Component disallows"
                      f"multiple instances being attached.")
                return False
            self.components[component.name] = component
            component._on_attached(self)
            return True

        if not component._key:
            try:
                self.components[component.name].append(component)
            except KeyError:
                self.components[component.name] = [component]
            component._on_attached(self)
            return True

        if not self.components[component.name]:
            self.components[component.name] = {}
        self.components[component.name][component.key] = component
        component._on_attached(self)
        return True

    def destroy(self):
        self._is_destroyed = True
        for component in self.components:
            component.destroy()
        self.ecs.on_entity_destroyed(self)

    def get(self, component: Union[str, Component], key: Optional[str] = None):
        """Get a Component currently attached to this Entity.

        Components can be accessed by passing in either the string name of the
        Component, or the class symbol directly. If the Entity has multiple of
        the Component, access a particular one by supplying a `key` parameter,
        or leave it unfilled to return all of the specified Component.
        """
        try:
            if type(component) == str:
                components = self.components[component.upper()]
            else:
                components = self.components[component.name]

            if components and key:
                return components[key]

            return components

        except:
            KeyError(f"Entity has no component {component}!")

    def has(self, component: Union[str, Component], key: Optional[str] = None):
        """Check if a Component is currently attached to this Entity."""
        try:
            if type(component) == str:
                components = self.components[component.upper()]
            else:
                components = self.components[component.name]

            if components and key:
                if components[key]:
                    return True

            if components:
                return True

        except KeyError:
            return False

    def owns(self, component: Component) -> bool:
        """Check if target Component has this Entity as an owner."""
        return component.entity == self

    def remove(
            self,
            component: Union[str, Component],
            key: Optional[str] = None
        ) -> Optional[Component]:
        is_component = isinstance(component, Component)
        key = component.key if is_component else key

        definition = self.ecs.components.get(component)
        accessor = definition.name

        if definition.allow_multiple:
            if not definition.key:
                try:
                    all = self.components[accessor]
                except:
                    raise KeyError(f"Cannot remove {definition.name} not on this entity!")

    def serialize(self):
        pass

    def fire_event(self, name: str, data):
        pass
