from __future__ import annotations

from ecstremity import Engine, Component

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

    position = monster['Position']
    print(monster.owns(position))

    position = monster.remove('Position')
    print(monster.owns(position))

if __name__ == '__main__':
    main()
