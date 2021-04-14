from __future__ import annotations

import unittest
import timeit
from ecstremity import *


class Position(Component):
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y


class Renderable(Component):
    def __init__(self, char: str, fg: int, bg: int) -> None:
        self.char = char
        self.fg = fg
        self.bg = bg


class MockSystem:
    def __init__(self, ecs):
        self.world = ecs.world
        self._query = self.world.create_query(
            all_of  = [ 'Position' ],
            none_of = [ 'Renderable' ])


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.ecs = Engine()
        self.world = self.ecs.create_world()

    def testInitializations(self):
        self.assertTrue(self.ecs)
        self.assertTrue(self.world)

    def testAdd(self):
        monster = self.world.create_entity()
        self.ecs.register_component(Position)
        self.ecs.register_component(Renderable)

        monster.add(Position, {'x': 0, 'y': 0})
        monster.add(Renderable, {'char': 'T', 'fg': 0xFFFF00FF, 'bg': 0xFF151515})


if __name__ == '__main__':
    unittest.main()
