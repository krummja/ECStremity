from __future__ import annotations
from typing import Any, Dict, TYPE_CHECKING, Optional, Union

from ecstremity.registry import Registry
from ecstremity.component import Component


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
        if type(component) != str:
            if issubclass(component, Component):
                component = component.name
        definition = self[component.upper()]
        return definition(**properties)

    # def get(self, component: Union[str, Component]) -> Component:
    #     """Grab a Component definition from those registered."""
    #     try:
    #         if type(component) != str:
    #             component = component.name
    #         return self[component.upper()]
    #     except:
    #         raise KeyError(f"No component {component} registered!")
