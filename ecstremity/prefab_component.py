from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from ecstremity.entity import Entity
    from ecstremity.component import Component


class PrefabComponent:

    def __init__(
            self,
            component_class: Component,
            properties: Optional[Dict[str, Any]] = None,
            overwrite: bool = True
        ) -> None:
        self.component_class = component_class
        self.properties = {} if not properties else properties
        self.overwrite = overwrite

    def apply_to_entity(
            self,
            entity: Entity,
            initial_props: Optional[Dict[str, Any]] = None
        ):
        if not initial_props:
            initial_props = {}
        if not self.component_class.allow_multiple & entity.has(self.component_class):
            if not self.overwrite:
                return
            component = entity[self.component_class.name]
            entity.remove(component)

        self.properties.update(initial_props)
        props: Dict[str, Any] = self.properties
        entity.add(self.component_class, props)
