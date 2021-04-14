from ecstremity.engine import Engine
from ecstremity.component import Component

import math
from collections import OrderedDict


class Position(Component):
    name = "POSITION"

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x = x
        self.y = y


class Obstacle(Component):
    _allow_multiple = True
    name = "OBSTACLE"


class Foo(Component):
    """"""

class Bar(Component):
    """"""

class Baz(Component):
    """"""


def setup_ecs():
    engine = Engine()
    engine.register_component(Position)
    engine.register_component(Obstacle)
    engine.register_component(Foo)
    engine.register_component(Bar)
    engine.register_component(Baz)
    world = engine.create_world()
    return engine, world


def add_remove_test(world):
    entity = world.create_entity()
    entity.add('POSITION', {'x': 0.0, 'y': 0.0})
    entity.remove('POSITION')


def query_test(world):
    world._queries = []
    world._entities = OrderedDict()
    for _ in range(64*64):
        entity = world.create_entity()
        entity.add('POSITION', {'x': 0.0, 'y': 0.0})
        entity.add('OBSTACLE', {})

    world.create_query(all_of=['POSITION'])
    world.create_query(all_of=['OBSTACLE'])
    world.create_query(all_of = ['OBSTACLE'])
    world.create_query(all_of = ['OBSTACLE'])
    world.create_query(all_of = ['OBSTACLE'])
    world.create_query(all_of = ['OBSTACLE'])
    world.create_query(all_of = ['OBSTACLE'])
    world.create_query(all_of = ['OBSTACLE'])


def add_test(world):
    entity = world.create_entity()
    entity.add(Position, {'x': 0, 'y': 0})
    entity.add(Obstacle, {})
    entity.add(Obstacle, {})
    entity.add(Obstacle, {})
    entity.add(Obstacle, {})
    entity.add(Obstacle, {})
    entity.add(Obstacle, {})
    entity.add(Obstacle, {})
    entity.add(Obstacle, {})
    entity.add(Obstacle, {})
    entity.add(Obstacle, {})
    entity.add(Obstacle, {})


if __name__ == '__main__':
    import timeit

    t = timeit.Timer(
        stmt="""
query_test(world)
        """,
        setup="""
from __main__ import setup_ecs, add_remove_test, query_test, add_test
engine, world = setup_ecs()
        """)

    repeats = 2
    result = t.timeit(number=repeats)
    print("total time:    " + str(math.trunc(result * 1000)) + "ms")
    print("per iteration: " + str(math.trunc((result / repeats) * 1000)) + "ms")
