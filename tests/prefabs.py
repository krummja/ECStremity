from __future__ import annotations

import unittest
import timeit
from ecstremity import *


class Position(Component):
    def __init__(self, x: int = 0, y: int = 0) -> None:
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


class DummyFlagA(Component):
    """Flag Component"""


class DummyFlagB(Component):
    """Flag Component"""


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.ecs = Engine()
        self.world = self.ecs.create_world()
        self.ecs.register_component(Position)
        self.ecs.register_component(Renderable)
        self.ecs.register_component(DummyFlagA)
        self.ecs.register_component(DummyFlagB)

    def testInitializations(self):
        self.assertTrue(self.ecs)
        self.assertTrue(self.world)

    def testCreatePrefabs(self):
        self.ecs.prefabs.register({
            "name": "Being",
            "components": [
                {
                    "type": "Position",
                    "properties": {
                        "x": 0, "y": 0
                    }
                }
            ]
        })  # Character
        self.ecs.prefabs.register({
            "name": "Character",
            "inherit": ["Being"],
            "components": [
                {
                    "type": "Renderable",
                    "properties": {
                        "char": "@",
                        "fg": (0, 255, 255),
                        "bg": (21, 21, 21)
                    }
                }
            ]
        })  # Being     -> Character
        self.ecs.prefabs.register({
            "name": "DummyA",
            "inherit": ["Character"],
            "components": [
                {
                    "type": "DummyFlagA"
                }
            ]
        })  # DummyA    -> Character
        self.ecs.prefabs.register({
            "name": "DummyB",
            "inherit": ["DummyA"],
            "components": [
                {
                    "type": "DummyFlagB"
                }
            ]
        })  # DummyB    -> DummyA
        self.ecs.prefabs.register({
            "name": "DummyC",
            "inherit": ["Character"],
            "components": [
                {
                    "type": "DummyFlagA"
                },
                {
                    "type": "DummyFlagB"
                }
            ]
        })  # DummyC    -> Character

        self.world.create_prefab("Character", {}, "CharacterA")
        self.world.create_prefab("DummyA", {}, "DummyEntityA")
        self.world.create_prefab("DummyB", {}, "DummyEntityB")
        self.world.create_prefab("DummyC", {
            "Position": {
                "x": 100, "y": 20
            }
        }, "DummyEntityC")

        char_a = self.world.get_entity("CharacterA")
        dummy_a = self.world.get_entity("DummyEntityA")
        dummy_b = self.world.get_entity("DummyEntityB")
        dummy_c = self.world.get_entity("DummyEntityC")

        print(char_a)
        print(dummy_a)
        print(dummy_b)
        print(dummy_c)


if __name__ == '__main__':
    unittest.main()
