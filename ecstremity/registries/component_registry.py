from __future__ import annotations
from typing import Any, Dict, TYPE_CHECKING, Optional

from registries.registry import Registry

if TYPE_CHECKING:
    from component import Component


class ComponentRegistry(Registry):
    _definitions: Dict[str, Component] = {}

    def register(self, component: Component):
        self._definitions[component.name] = component

    def create(
            self,
            component_name: str,
            properties: Dict[str, Any]
        ) -> Optional[Component]:
        try:
            definition: Component = self._definitions[component_name]
            return definition(**properties)
        except:
            raise KeyError(f"No component {component_name} registered!")

    def get(self, component_type: str) -> Component:
        try:
            return self._definitions[component_type]
        except:
            raise KeyError(f"No component {component_type} registered!")


