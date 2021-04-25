from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from ecstremity.entity import Entity
    from ecstremity.world import World
    from ecstremity.prefab_component import PrefabComponent
    from ecstremity.engine import Engine


class PrefabRegistry:

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        self._prefabs = {}

    def register(self, prefab_definition: Dict[str, Any]) -> None:
        # self._prefabs[name] = obj
        self._prefabs.update(prefab_definition)

    def remove(self, name: str) -> None:
        del self._prefabs[name]

    def deserialize(self, data: Dict[str, Any]):
        registered = self._prefabs.get(data['name'])
        if registered:
            return registered
        prefab = PrefabComponent()

    def create(self, world: World, name: str, properties: Dict[str, Any] = None) -> Optional[Entity]:
        if not properties:
            properties = {}

        prefab = self.get(name)
        if not prefab:
            print(f"Could not instantiate prefab {name} since it is not registered")
            return

        entity = world.create_entity()
        entity._qeligible = False
        prefab.apply_to_entity(entity, properties)
        entity._qeligible = True
        entity.candidacy()
        return entity

    def get(self, prefab_name: str):
        return self._prefabs[prefab_name]
