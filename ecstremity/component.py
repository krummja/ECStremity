from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity
    from engine import Engine


class Component:
    """All Components inherit from this class.

    To create a new Component, inherit from this base class and define the
    Component's properties as instance variables in the subclass's constructor.

    Note that the `name` attribute is the accessor for the component, whether
    as an instance or uninitialized class. These should be in all-caps for
    consistency.
    """

    ecs: Engine
    entity: Optional[Entity] = None
    _is_destroyed: bool = False

    @property
    def name(self) -> str:
        return self._name.upper()

    @name.setter
    def name(self, value: str) -> None:
        self._name = value.upper()

    @property
    def is_destroyed(self) -> bool:
        """Returns True if this component has been destroyed."""
        return self._is_destroyed

    @property
    def is_attached(self) -> bool:
        """Returns True if this component is attached to an entity."""
        return bool(self.entity)

    def clone(self) -> Component:
        """TODO"""

    def destroy(self) -> None:
        """Remove and destroy this component."""
        self.remove(destroy=True)

    def on_attached(self):
        """Override this method to add behavior when this component is added
        to an entity.
        """
        pass

    def on_event(self):
        """Override this method to add behavior when this component receives
        a signal from an `EntityEvent`.
        """
        pass

    def on_destroyed(self):
        """Override this method to add behavior when this component is
        destroyed.
        """
        pass

    def on_detached(self):
        """Override this method to add behavior when this component is removed
        from an entity.
        """
        pass

    def remove(self, destroy: bool = True) -> Optional[Component]:
        """Remove this component. If `destroy = True` then this behaves the
        same as `destroy()`.
        """
        if self.is_attached:
            self.entity[self.name.upper()] = None
            self.entity = None
            return self
        if destroy:
            self._on_destroyed()

    def _on_attached(self, entity: Entity):
        self.entity = entity
        self.on_attached()

    def _on_event(self, evt):
        """TODO"""
        pass

    def _on_destroyed(self):
        self._is_destroyed = True
        self.on_destroyed()

    def _on_detached(self):
        if self.is_attached:
            self.on_detached()
            self.entity = None
