from __future__ import annotations
import pickle
from typing import *

if TYPE_CHECKING:
    pass


from ecstremity import *


class Position(Component):

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @property
    def xy(self):
        return self.x, self.y


class FakeComponentA(Component):
    """Fake component"""


class FakeComponentB(Component):
    """Fake component"""


if __name__ == '__main__':
    ecs = Engine()
    ecs.register_component(Position)
    ecs.register_component(FakeComponentA)
    ecs.register_component(FakeComponentB)

    world = ecs.create_world()

    e1 = world.create_entity()
    ecs.prefabs.register({
        "name": "Base",
        "components": [
            {
                "type": "Position",
                "properties": {
                    "x": 20,
                    "y": 20,
                }
            }
        ]
    })

    ecs.prefabs.register({
        "name": "Derived",
        "inherit": ["Base"],
        "components": [
            {
                "type": "FakeComponentA"
            },
            {
                "type": "FakeComponentB"
            }
        ]
    })

    e3 = world.create_prefab("Derived")

    serial_world = world.serialize()
    serial_world["entities"][1]["components"]["POSITION"]["_foo"] = "bar"

    ecs_2 = Engine()
    ecs_2.register_component(Position)
    ecs_2.register_component(FakeComponentA)
    ecs_2.register_component(FakeComponentB)

    world_2 = ecs_2.create_world()
    world_2.deserialize(serial_world)

    e2 = world_2.get_entity(e3.uid)
    print(e2['Position'].xy)
