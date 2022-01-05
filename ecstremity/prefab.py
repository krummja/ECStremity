from __future__ import annotations
from typing import List, Dict, Any

from ecstremity.entity import Entity
from ecstremity.prefab_component import PrefabComponent


class Prefab:

    def __init__(
            self,
            name: str,
            inherit: List[Prefab] = None,
            components: List[PrefabComponent] = None
        ) -> None:
        self.name = name
        self.inherit = inherit if inherit else []
        self.components = components if components else []

    def __str__(self):
        return f"{self.name} {[component.cls for component in self.components]}"

    def add_component(self, component: PrefabComponent):
        self.components.append(component)

    def apply_to_entity(self, entity: Entity, prefab_props: Dict[int, Any] = None) -> Entity:
        if not prefab_props:
            prefab_props = {}
        prefab_props = {k.upper(): v for k, v in prefab_props.items() if k[0] != "_"}

        for parent in self.inherit:
            parent.apply_to_entity(entity, prefab_props)

        arr_comps = {}

        for component in self.components:
            klass = component.klass
            comp_id = klass.comp_id

            initial_comp_props = {}

            if klass.allow_multiple:

                if not arr_comps.get(comp_id):
                    arr_comps[comp_id] = 0

                if prefab_props.get(comp_id):
                    if prefab_props[comp_id].get(arr_comps[comp_id]):
                        initial_comp_props = prefab_props[comp_id][arr_comps[comp_id]]

                arr_comps[comp_id] += 1

            else:
                initial_comp_props = prefab_props.get(comp_id)

            component.apply_to_entity(entity, initial_comp_props)
        return entity
