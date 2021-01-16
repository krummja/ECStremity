from __future__ import annotations

import unittest

from ecstremity.engine import Engine
from ecstremity.component import Component
from ecstremity.entity import  Entity


class Position(Component):
    name = "POSITION"
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x = x
        self.y = y


class Renderable(Component):
    name = "RENDERABLE"
    def __init__(self, char: str, fg: str, bg: str) -> None:
        self.char = char
        self.fg = fg
        self.bg = bg


class TestECS(unittest.TestCase):

    def setUp(self):
        self.ecs = Engine()

    def testConstructor(self):
        self.assertTrue(self.ecs)

    def testCreateEntity(self):
        monster = self.ecs.create_entity()
        self.assertTrue(isinstance(monster, Entity))

    def testCreateAndRegisterComponents(self):
        self.ecs.register_component(Position)
        position = self.ecs.create_component('POSITION', {'x': 1.0, 'y': 10.0})

        self.assertTrue(isinstance(position, Component))
        self.assertTrue(position.x == 1.0)
        self.assertTrue(position.y == 10.0)

    def testAttachComponent(self):
        self.ecs.register_component(Position)
        self.ecs.register_component(Renderable)
        # monster = self.ecs.create_entity()
        # monster.add('Position', {'x': 10, 'y': 9})

if __name__ == '__main__':
    unittest.main()
