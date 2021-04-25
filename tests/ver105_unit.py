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


class Material(Component):
    allow_multiple = True
    def __init__(self, name: str):
        self.name = name


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
        self.ecs.register_component(Position)
        self.ecs.register_component(Renderable)
        self.ecs.register_component(Material)

    def testInitializations(self):
        self.assertTrue(self.ecs)
        self.assertTrue(self.world)

    def testAdd(self):
        monster = self.world.create_entity()
        monster.add(Position, {'x': 0, 'y': 0})
        monster.add(Renderable, {'char': 'T', 'fg': 0xFFFF00FF, 'bg': 0xFF151515})

    def testAddRemove(self):
        monster = self.world.create_entity()

        # Add and Remove using class symbol
        monster.add(Position, {'x': 0, 'y': 0})
        monster.remove(Position)

        # Add and Remove using string name
        monster.add('Position', {'x': 0, 'y': 0})
        monster.remove('Position')

    def testDestroy(self):
        monster = self.world.create_entity()
        monster.add(Position, {'x': 0, 'y': 0})
        monster.add(Renderable, {'char': 'T', 'fg': 0xFFFFFFFF, 'bg': 0xFF151515})

        self.assertTrue(monster in self.world.entities)
        monster.destroy()
        self.assertTrue(monster not in self.world.entities)

    def testDestroyEntities(self):
        for _ in range(100):
            self.world.create_entity()
        self.assertTrue(len(self.world.entities) == 100)

        self.world.destroy_entities()
        self.assertTrue(len(self.world.entities) == 0)

    def testCreatePrefabs(self):
        self.ecs.prefabs.register({
            'name': 'Being',
            'components': [
                {
                    'type': 'Position',
                    'properties': {
                        'x': 0, 'y': 0
                    }
                },
                {
                    'type': 'Material',
                    'properties': {
                        'name': 'flesh'
                    },
                },
            ]
        })

        self.ecs.prefabs.register({
            'name': 'Warrior',
            'components': [
                {
                    'type': 'Material',
                    'properties': {
                        'name': 'steel'
                    }
                }
            ]
        })

        self.ecs.prefabs.register({
            'name': 'HumanWarrior',
            'inherit': ['Being', 'Warrior'],
            'components': [
                {
                    'type': 'Material',
                    'overwrite': True,
                    'properties': {
                        'name': 'silver'
                    }
                }
            ]
        })

        warrior = self.world.create_prefab('HumanWarrior', {
            'position': {
                'x': 20, 'y': 50
            }
        })
        self.assertTrue(warrior.has('Material'))
        self.assertTrue(warrior['Material'].name == 'silver')
        self.assertTrue(warrior['Position'].x == 20)


if __name__ == '__main__':
    unittest.main()
