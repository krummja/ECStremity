from __future__ import annotations
from typing import *
from dataclasses import dataclass

if TYPE_CHECKING:
    from entity import Entity
    from component import Component


InitialProps = Dict[str, Any]
Definition = Union[Component, InitialProps]


@dataclass
class Prefab:
    inherit: List[Prefab]
    components: List[Dict[str, Definition]]

    @classmethod
    def add_component(cls, component: Component, init_props: InitialProps = None) -> None:
        if not init_props:
            init_props = {}
        cls.components.append({
            'definition': component,
            'init_props': init_props
            })

    @classmethod
    def apply_to_entity(cls, entity: Entity, properties: Dict[str, Any] = None) -> Entity:
        if not properties:
            properties = {}
        for parent in cls.inherit:
            parent.apply_to_entity(entity, properties)

        # For each component defined for the Prefab...
        for component in cls.components:
            entity.add(component['definition'], component['init_props'])

        return entity
