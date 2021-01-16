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
    monster = ecs.create_entity()
    monster.add("Position", {'x': 10, 'y': 5})
    print(monster.items())

    component = monster.remove('Position')
    print(vars(component))


if __name__ == '__main__':
    main()
