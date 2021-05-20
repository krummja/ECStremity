from __future__ import annotations
from typing import *
from ecstremity.prefab import Prefab
from ecstremity.prefab_component import PrefabComponent

if TYPE_CHECKING:
    from .world import World
    from .entity import Entity
    from .engine import Engine


class PrefabRegistry:

    def __init__(self, engine: Engine):
        self.engine = engine
        self._prefabs = {}

    def register(self, data: Dict[str, Any]):
        prefab = self.deserialize(data)
        self._prefabs[prefab.name] = prefab

    def deserialize(self, data):
        registered = self.get(data['name'])
        if registered:
            return registered

        prefab = Prefab(data['name'])

        inherit = []
        if isinstance(data.get('inherit'), list):
            inherit = data['inherit']
        elif isinstance(data.get('inherit'), str):
            inherit = [data.get['inherit']]

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

    def create(self, world: World, name: str, properties: Dict[str, Any] = None, uid: str = None) -> Optional[Entity]:
        if not properties:
            properties = {}

        prefab: Prefab = self.get(name)
        if not prefab:
            print(f"Could not instantiate {name} since it is not registered")
            return

        entity = world.create_entity(uid if uid else None)
        entity._qeligible = False
        prefab.apply_to_entity(entity, properties)
        entity._qeligible = True
        entity.candidacy()

        return entity

    def clear(self):
        self._prefabs.clear()

    def get(self, name):
        return self._prefabs.get(name)
