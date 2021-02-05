from __future__ import annotations
from typing import Any, Dict, Optional, TYPE_CHECKING
import json

from .registry import Registry

if TYPE_CHECKING:
    from entity import Entity


class PrefabRegistry(Registry):

    def register(self, definition) -> None:
        self[definition['name']] = {
            "inherit": definition['inherit'],
            "components": [component for component in definition['components']]
            }

    def inherit(self, prefab_name: str) -> Dict[str, Any]:
        pass

    def apply_to_entity(
            self,
            entity: Entity,
            name: str,
            properties: Optional[Dict[str, Any]] = None
        ) -> Entity:
        try:
            if properties is None:
                properties = {}

            definition = self[name]

            for component in definition['components']:
                try:
                    component['properties'].update(properties[component['type']])
                except KeyError:
                    pass
                entity.add(component['type'],
                           component['properties'])
            return entity
        except KeyError:
            pass
