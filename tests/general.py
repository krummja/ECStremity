from __future__ import annotations

from ecstremity.engine import Engine
from ecstremity.component import Component
from ecstremity.entity import Entity


class Position(Component):
    name = "POSITION"
    allow_multiple = True
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y


def main():
    ecs = Engine()
    ecs.register_component(Position)
    ecs.create_component("POSITION", {'x': 10, 'y': 10})

    monster = ecs.create_entity()
    monster.add("Position", {'x': 10, 'y': 5})
    monster.add("Position", {'x': 5, 'y': 10})
    print(monster.has("Position"))  # returns True
    print(monster.get("Position"))  # returns Position instance on monster

    position = monster.get("Position")
    print(monster.owns(position))  # True

if __name__ == '__main__':
    main()
