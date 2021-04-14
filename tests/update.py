from ecstremity.component import Component
from ecstremity.world import World
from ecstremity.engine import Engine
from ecstremity.query import Query


class Position(Component):

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @property
    def xy(self):
        return self.x, self.y


class Renderable(Component):

    def __init__(self, char: str, fg: int, bg: int) -> None:
        self.char = char
        self.fg = fg
        self.bg = bg


if __name__ == '__main__':
    engine = Engine()
    engine.register_component(Position)
    engine.register_component(Renderable)

    world = engine.create_world()

    entity = world.create_entity()
    for entity in world.entities:
        print(entity.uid)
    entity.add(Position, {'x': 10, 'y': 10})
    entity.add(Renderable, {'char': '@', 'fg': 0xFFFF00FF, 'bg': 0xFF151515})

    system = world.create_query(all_of=[ Position, Renderable ])
