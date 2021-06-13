from __future__ import annotations
from typing import *
from ecstremity.prefab import Prefab
from ecstremity.prefab_component import PrefabComponent

if TYPE_CHECKING:
    from ecstremity.world import World
    from ecstremity.entity import Entity
    from ecstremity.engine import Engine


class PrefabRegistry:

    def __init__(self, engine: Engine):
        self.engine = engine
        self._prefabs: Dict[str, Prefab] = {}

    def register(self, data: Dict[str, Any]) -> None:
        prefab = self.deserialize(data)
        self._prefabs[prefab.name] = prefab

    def deserialize(self, data: Dict[str, Any]) -> Prefab:
        registered = self.get(data['name'])
        if registered:
            return registered

        prefab = Prefab(data['name'])

        inherit: List[str] = []
        if isinstance(data.get('inherit'), list):
            inherit = data.get('inherit')
        elif isinstance(data.get('inherit'), str):
            inherit = [data.get('inherit')]

        prefab.inherit = [self.get(parent) for parent in inherit]
        comps = data.get('components', [])

        for component_data in comps:
            if isinstance(component_data, str):
                comp_id = component_data
                klass = self.engine.components[comp_id]
                if klass:
                    prefab.add_component(PrefabComponent(klass))
                    continue

            if isinstance(component_data, dict):
                comp_id = component_data['type']
                klass = self.engine.components[comp_id]
                if klass:
                    prefab.add_component(PrefabComponent(
                        klass,
                        component_data.get('properties', {}),
                        component_data.get('overwrite', True)
                    ))
                    continue

            print(f"Unrecognized component reference {component_data} in prefab {data['name']}")

        return prefab

    def create(
            self,
            world: World,
            name: str,
            properties: Optional[Dict[str, Any]] = None,
            uid: Optional[str] = None
        ) -> Optional[Entity]:
        if not properties:
            properties = {}

        prefab: Optional[Prefab] = self.get(name)
        if not prefab:
            print(f"Could not instantiate {name} since it is not registered")
            return None

        entity = world.create_entity(uid if uid else None)
        entity._qeligible = False
        prefab.apply_to_entity(entity, properties)
        entity._qeligible = True
        entity.candidacy()

        return entity

    def clear(self):
        self._prefabs.clear()

    def get(self, name: str) -> Optional[Prefab]:
        return self._prefabs.get(name)


class PrefabLoader:

    pass
