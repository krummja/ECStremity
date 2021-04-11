from __future__ import annotations
from typing import Any, Dict, Optional, TYPE_CHECKING
import json

from .registry import Registry

if TYPE_CHECKING:
    from entity import Entity
    from ecstremity.prefab import Prefab


class PrefabRegistry(Registry):

    def register(self, definition) -> None:
        self[definition['name'].upper()] = {
            "inherit": definition['inherit'],
            "components": [component for component in definition['components']]
            }

    def apply_to_entity(
            self,
            entity: Entity,
            name: str,
            properties: Optional[Dict[str, Any]] = None
        ) -> Entity:
        try:
            if properties is None:
                properties = {}

            definition = self[name.upper()]

            for component in definition['components']:
                try:
                    component['properties'].update(properties[component['type']])
                except KeyError:
                    pass

                entity.add(component['type'],
                           component['properties'])

            return entity

        except KeyError:
            raise Exception(f"Failed to apply prefab {name} to entity "
                            f"with properties {properties}")

    # def create(self, prefab_name):
    #     try:
    #         prefab = self.get(prefab_name.upper())
    #     except KeyError:
    #         print(f"Could not instantiate prefab for {prefab_name} "
    #               f"since it is unregistered.")
    #         return
    #
    #     entity = self.ecs.create_entity()
    #     self.apply_to_entity(entity, prefab['type'], prefab['properties'])
    #     return entity
