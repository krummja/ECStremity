from __future__ import annotations

import sys
import unittest
import logging

from ecstremity.engine import Engine
from ecstremity.component import Component
from ecstremity.entity import  Entity

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def debugattr(cls):
    orig_getattribute = cls.__getattribute__

    def __getattribute__(self, name):
        print('Get: ', name)
        return orig_getattribute(self, name)
    cls.__getattribute__ = __getattribute__

    return cls

@debugattr
class Position(Component):
    name = "POSITION"
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x = x
        self.y = y

@debugattr
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
        logging.debug("engine successfully initialized")

    def testCreateEntity(self):
        monster = self.ecs.create_entity()
        self.assertTrue(isinstance(monster, Entity))
        logging.debug(f"entity created with UID {monster.uid}")

    def testCreateAndRegisterComponents(self):
        self.ecs.register_component(Position)
        logging.debug(f"created component {Position.name}")

        position = self.ecs.create_component('POSITION', {'x': 1.0, 'y': 10.0})

        self.assertTrue(isinstance(position, Component))
        self.assertTrue(position.x == 1.0)
        self.assertTrue(position.y == 10.0)

    def testAttachComponent(self):
        self.ecs.register_component(Position)
        self.ecs.register_component(Renderable)
        logging.debug(self.ecs.components._definitions)

        # monster = self.ecs.create_entity()
        # monster.add('Position', {'x': 10, 'y': 9})

if __name__ == '__main__':
    unittest.main()
