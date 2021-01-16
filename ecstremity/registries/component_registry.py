from __future__ import annotations
from typing import Any, Dict, TYPE_CHECKING, Optional, Union

from ecstremity import Component
from .registry import Registry


class ComponentRegistry(Registry):
    """Component registry."""

    def register(self, component: Component):
        self[component.name] = component

    def create(
            self,
            component: Union[str, Component],
            properties: Dict[str, Any]
        ) -> Optional[Component]:
        """Create a new instance of a Component registered definition.

        Pass in the class symbol or name of a Component along with a dictionary
        of initialization parameters. If component is registered and properties
        is well-formed, returns a Component instance.
        """
        if not isinstance(component, str):
            if issubclass(component, Component):
                component = component.name
        definition = self[component]
        return definition(**properties)

    def __getitem__(self, component: Union[str, Component]) -> Component:
        if not isinstance(component, str):
            component = component.name
        return super().__getitem__(component.upper())
