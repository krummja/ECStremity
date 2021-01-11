from __future__ import annotations


class Engine:

    @property
    def uid_generator(self):
        pass

    def generate_id(self) -> str:
        pass

    def create_entity(self, uid):
        pass

    def create_prefab(self, name_or_class, initial_props = None):
        pass

    def destroy_entity(self, entity):
        pass

    def register_prefab(self, data):
        pass

    def register_component(self, component):
        pass

    def get_entity(self, uid: str):
        pass

    def serialize(self, entities):
        pass

    def deserialize(self, data):
        pass
