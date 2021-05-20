from typing import Dict, Any
from deepmerge import always_merger

from ecstremity.entity import Entity
from ecstremity.component import Component


class PrefabComponent:
    """Interface class to handle the application of prefabs to an entity."""

    def __init__(self, klass: Component, properties: Dict[str, Any] = None, overwrite: bool = True):
        self.klass = klass
        self.properties = properties if properties else {}
        self.overwrite = overwrite

    def apply_to_entity(self, entity: Entity, initial_props: Dict[str, Any] = None):
        if not initial_props:
            initial_props = {}

        if not self.klass.allow_multiple and entity.has(self.klass.comp_id):
            if not self.overwrite:
                return
            component = entity[self.klass.comp_id]
            entity.remove(component)

        props = always_merger.merge(self.properties, initial_props)
        entity.add(self.klass, props)
