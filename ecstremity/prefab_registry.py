from __future__ import annotations
from typing import *
from collections import OrderedDict
from ecstremity.component import Component

if TYPE_CHECKING:
    from .world import World
    from .entity import Entity
    from .engine import Engine


class PrefabComponent:
    """Interface class to handle the application of prefabs to an entity."""

    def __init__(self, cls: Component, properties: Dict[str, Any] = None, overwrite: bool = True):
        self.cls = cls
        self.properties = properties if properties else {}
        self.overwrite = overwrite

    def apply_to_entity(self, entity: Entity, initial_props: Dict[str, Any] = None):
        if not initial_props:
            initial_props = {}
        if not self.cls.allow_multiple and entity.has(self.cls.comp_id):
            if not self.overwrite:
                return
            component = entity[self.cls.comp_id]
            entity.remove(component)
        self.properties.update(initial_props)
        entity.add(self.cls, self.properties)


class Prefab:

    def __init__(
            self,
            name: str,
            inherit: List[Prefab] = None,
            components: List[PrefabComponent] = None
        ) -> None:
        self.name = name
        self.inherit = inherit if inherit else []
        self.components = components if components else []

    def add_component(self, component: PrefabComponent):
        self.components.append(component)

    def apply_to_entity(self, entity: Entity, prefab_props: Dict[int, Any] = None) -> Entity:
        if not prefab_props:
            prefab_props = {}
        prefab_props = {k.upper(): v for k, v in prefab_props.items()}

        for parent in self.inherit:
            parent.apply_to_entity(entity, prefab_props)

        arr_comps = {}

        for prefab_component in self.components:
            comp_cls = prefab_component.cls
            name = comp_cls.comp_id
            initial_comp_props = {}

            if comp_cls.allow_multiple:

                if not arr_comps.get(name):
                    arr_comps[name] = 0

                if name in prefab_props.keys():
                    try:
                        initial_comp_props = prefab_props[name][arr_comps[name]]
                    except KeyError:
                        pass

                arr_comps[name] += 1

            else:
                try:
                    initial_comp_props = prefab_props[name]
                except KeyError:
                    pass

            prefab_component.apply_to_entity(entity, initial_comp_props)
        return entity


class PrefabRegistry:

    def __init__(self, engine: Engine):
        self.engine = engine
        self._prefabs = {}

    def register(self, data: Dict[str, Any]):
        prefab = self.deserialize(data)
        self._prefabs[prefab.name] = prefab

    def deserialize(self, data: Dict[str, Any]):
        registered = self.get(data['name'])
        if registered:
            return registered
        prefab = Prefab(data['name'])
        inherit: List[str]

        if isinstance(data.get('inherit'), list):
            inherit = data['inherit']
        elif isinstance(data.get('inherit'), str):
            inherit = [data['inherit']]
        else:
            inherit = []

        def map_inheritance(parent):
            ref = self.get(parent)
            if not ref:
                print(f"Prefab {data['name']} cannot inherit from Prefab {parent} because it is not registered yet")
                return parent
            return ref

        prefab.inherit = map(map_inheritance, inherit)
        comps = data.get('components', [])

        for component_data in comps:

            if isinstance(component_data, str):
                name = component_data.upper()
                cls = self.engine.components[name]
                if cls:
                    prefab.add_component(PrefabComponent(cls))

            if isinstance(component_data, dict):
                name = component_data['type']
                cls = self.engine.components[name]
                if cls:
                    prefab.add_component(PrefabComponent(
                        cls, component_data.get('properties', {}), component_data.get('overwrite', True)
                    ))

            else:
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

    def get(self, name):
        return self._prefabs.get(name)
