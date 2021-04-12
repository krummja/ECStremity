from ecstremity.engine import Engine
from ecstremity.component import Component

import math


class Position(Component):
    name = "POSITION"

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x = x
        self.y = y


class Obstacle(Component):
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
    return engine


def add_remove_test(engine):
    entity = engine.create_entity()
    entity.add('POSITION', {'x': 0.0, 'y': 0.0})
    entity.remove('POSITION')


def query_test(engine):
    for _ in range(64*64):
        entity = engine.create_entity()
        entity.add('POSITION', {'x': 0.0, 'y': 0.0})
        entity.add('OBSTACLE', {})

    engine.create_query(all_of=['POSITION'])
    engine.create_query(all_of=['OBSTACLE'])
    engine.create_query(all_of = ['OBSTACLE'])
    engine.create_query(all_of = ['OBSTACLE'])
    engine.create_query(all_of = ['OBSTACLE'])
    engine.create_query(all_of = ['OBSTACLE'])
    engine.create_query(all_of = ['OBSTACLE'])
    engine.create_query(all_of = ['OBSTACLE'])
    # for entity in query.result:
    #     entity['POSITION'].x += 1.0
    #     entity['POSITION'].y += 1.0


if __name__ == '__main__':
    import timeit

    t = timeit.Timer(
        stmt="""
query_test(engine)
iterations += 1
print("iteration:     " + str(iterations))
        """,
        setup="""
from __main__ import setup_ecs, add_remove_test, query_test
engine = setup_ecs()
iterations = 0
        """)

    repeats = 1
    result = t.timeit(number=repeats)
    print("total time:    " + str(math.trunc(result * 1000)) + "ms")
    print("per iteration: " + str(math.trunc((result / repeats) * 1000)) + "ms")
