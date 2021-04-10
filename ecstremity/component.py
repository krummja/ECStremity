from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from entity import Entity, EntityEvent
    from engine import Engine, GAME, EngineAdapter


class NonremovableError(Exception):
    pass


class componentmeta(type):

    def __new__(mcs, clsname, bases, clsdict):
        clsobj = super().__new__(mcs, clsname, bases, clsdict)
        clsobj.name = str(clsname).upper()
        return clsobj


class Component(metaclass=componentmeta):
    """All Components inherit from this class.

    To create a new Component, inherit from this base class and define the
    Component's properties as instance variables in the subclass's constructor.

    Note that the `name` attribute is the accessor for the component, whether
    as an instance or uninitialized class. These should be in all-caps for
    consistency.
    """

    ecs: Union[Engine, EngineAdapter]
    client: GAME
    init_props: Dict[str, Any]
    entity: Optional[Entity] = None
    _name: str = ''
    _is_destroyed: bool = False
    _removable: bool = True

    @property
    def name(self):
        return self._name

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

    def on_event(self, evt):
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
        if self._removable:
            if self.is_attached:
                self.entity[self.name.upper()] = None
                self.ecs.components.on_component_removed(self.entity)
                self.entity = None
            if destroy:
                self._on_destroyed()
        else:
            raise NonremovableError("This component cannot safely be removed!")

        return self

    def _on_attached(self, entity: Entity):
        self.entity = entity
        self.on_attached()

    def _on_event(self, evt: EntityEvent) -> None:
        self.on_event(evt)
        try:
            handler = getattr(self, f"on_{evt.name}")
            return handler(evt)
        except Exception:
            return None

    def _on_destroyed(self):
        self._is_destroyed = True
        self.on_destroyed()

    def _on_detached(self):
        if self.is_attached:
            self.on_detached()
            self.entity = None
