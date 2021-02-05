from __future__ import annotations
import dataclasses
from typing import Any, Dict, List, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from entity import Entity
    from component import Component


@dataclass
class Prefab:
    inherit: List[Prefab] = []
    components: List[Component] = []

    @classmethod
    def add_component(cls, component: Component) -> None:
        cls.components.append(component)

    @classmethod
    def apply_to_entity(cls, entity: Entity, properties: Dict[str, Any]) -> Entity:
        for parent in cls.inherit:
            parent.apply_to_entity(entity, properties)

        component_properties = {}

        # For each component defined for the Prefab...
        for component in cls.components:

            # Get the class symbol for that component.
            component_class = component.__class__
            component_properties = properties[component_class.__name__]

        return entity
