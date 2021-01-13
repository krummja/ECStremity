from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity
    from engine import Engine


class Component:
    """All Components inherit from this class."""
    name: str
    ecs: Engine
    entity: Entity

    allow_multiple: bool = False
    _is_destroyed: bool = False

    @property
    def is_destroyed(self) -> bool:
        return self._is_destroyed

    @property
    def is_attached(self) -> bool:
        return bool(self.entity)

    def remove(self, destroy: bool = True) -> None:
        if self._is_attached:
            pass
        if destroy:
            self._on_destroyed()

    def destroy(self) -> None:
        self.remove(destroy=True)

    def on_attached(self):
        pass

    def on_detached(self):
        pass

    def on_destroyed(self):
        pass

    def _on_attached(self, entity: Entity):
        self.entity = entity
        self.on_attached()

    def _on_detached(self):
        if self.is_attached:
            self.on_detached()
            self.entity = None

    def _on_destroyed(self):
        self._is_destroyed = True
        self.on_destroyed()
