from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from ecstremity.entity import Entity
    from ecstremity.prefab_component import PrefabComponent


class Prefab:

    def __init__(self, name: str):
        self.name = name
        self.inherit: List[PrefabComponent] = []
        self.components: List[PrefabComponent] = []

    def add_component(self, prefab_component) -> None:
        self.components.append(prefab_component)

    def apply_to_entity(self, entity: Entity, prefab_props: Dict[str, Any] = None) -> Entity:
        if not prefab_props:
            prefab_props = {}
        for component in self.components:
            component.apply_to_entity(entity, prefab_props)
        return entity
