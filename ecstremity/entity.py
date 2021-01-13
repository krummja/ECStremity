from __future__ import annotations
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from component import Component
    from engine import Engine, Component


class Entity:

    def __init__(self, ecs: Engine, uid: Optional[str] = None) -> None:
        self.ecs = ecs
        self.uid = uid if uid is not None else self.ecs.generate_uid()
        self.components: Dict[str, Component] = {}
        self._is_destroyed: bool = False

    def destroy(self):
        self._is_destroyed = True
        for component in self.components:
            component.destroy()
        self.ecs.on_entity_destroyed(self)

    def add(self, component: Component, properties: Dict[str, Any]) -> bool:
        pass

    def attach(self, component: Component) -> bool:
        pass

    def owns(self, component: Component) -> bool:
        pass

    def remove(self, component_type: str) -> Optional[Component]:
        pass

    def fire_event(self, name: str, data):
        pass
