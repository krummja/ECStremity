from __future__ import annotations

import unittest
from unittest.mock import create_autospec

from ecstremity.engine import Engine
from ecstremity.component import Component
from ecstremity.entity import  Entity


def function(a, b, c):
    pass

mock_function = create_autospec(function, return_value='Mock Callback!')


class Position(Component):
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x = x
        self.y = y


class Renderable(Component):
    def __init__(self, char: str, fg: str, bg: str) -> None:
        self.char = char
        self.fg = fg
        self.bg = bg


class System:
    def __init__(self, ecs):
        self.ecs = ecs
        self._query = self.ecs.create_query(
            all_of=['Position'],
            none_of=['Renderable'])

    def update(self):
        for entity in self._query.result:
            pass


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
        position2 = self.ecs.create_component('poSiTion', {'x': 1.0, 'y': 10.0})

        self.assertTrue(isinstance(position, Component))
        self.assertTrue(position.x == 1.0)
        self.assertTrue(position.y == 10.0)
        self.assertTrue(isinstance(position2, Component))
        self.assertTrue(position2.x == 1.0)
        self.assertTrue(position2.y == 10.0)

    def testAttachComponent(self):
        self.ecs.register_component(Position)
        self.ecs.register_component(Renderable)
        monster = self.ecs.create_entity()
        monster.add('Position', {'x': 10, 'y': 9})

    def testAnyOfQuery(self):
        self.ecs.register_component(Position)
        self.ecs.register_component(Renderable)

        monster = self.ecs.create_entity()
        monster.add(Position, {'x': 0, 'y': 0})
        monster.add(Renderable, {'char': '@', 'fg': '#0f0', 'bg': '#000'})

        empty_monster = self.ecs.create_entity()

        # Expect False for an empty Entity
        query = self.ecs.create_query(any_of=['Renderable'])
        result = query.candidate(empty_monster)
        self.assertFalse(result)

        # Expect True if Entity has the Component
        query = self.ecs.create_query(any_of=['Position'])
        result = query.candidate(monster)
        self.assertTrue(result)

        # Expect True if Entity has at least one of listed Components
        query = self.ecs.create_query(any_of=['Position', 'Geometry', 'Renderable'])
        true_result = query.candidate(monster)
        false_result = query.candidate(empty_monster)
        self.assertTrue(true_result)
        self.assertFalse(false_result)

    def testAllOfQuery(self):
        self.ecs.register_component(Position)
        self.ecs.register_component(Renderable)

        monster = self.ecs.create_entity()
        monster.add('Position', {'x': 0, 'y': 0})
        monster.add('Renderable', {'char': '@', 'fg': '#0f0', 'bg': '#000'})

        empty_monster = self.ecs.create_entity()

        query = self.ecs.create_query(all_of=['Position', 'Renderable'])

        # Should return True for an Entity that has all of the listed Components
        true_result = query.candidate(monster)
        self.assertTrue(true_result)

        # Should return False for an empty Entity
        false_result = query.candidate(empty_monster)
        self.assertFalse(false_result)

        # Should return False for an Entity that has a subset of the listed Components
        other_monster = self.ecs.create_entity()
        other_monster.add(Position, {'x': 10, 'y': 2})

        false_result = query.candidate(other_monster)
        self.assertFalse(false_result)

    def testNoneOfQuery(self):
        self.ecs.register_component(Position)
        self.ecs.register_component(Renderable)

        monster = self.ecs.create_entity()
        monster.add('Position', {'x': 0, 'y': 0})
        monster.add('Renderable', {'char': '@', 'fg': '#0f0', 'bg': '#000'})

        empty_monster = self.ecs.create_entity()

        query = self.ecs.create_query(none_of=['Position', 'Renderable'])

        # Should return True for an empty Entity
        true_result = query.candidate(empty_monster)
        self.assertTrue(true_result)

        # Should return False for an Entity that has any of the listed Components
        false_result = query.candidate(monster)
        self.assertFalse(false_result)

    def testCombinationQuery(self):
        self.ecs.register_component(Position)
        self.ecs.register_component(Renderable)

        monster = self.ecs.create_entity()
        monster.add('Position', {'x': 0, 'y': 0})
        monster.add('Renderable', {'char': '@', 'fg': '#0f0', 'bg': '#000'})

        empty_monster = self.ecs.create_entity()

        query = self.ecs.create_query(
            all_of=['Position', 'Renderable'],
            none_of=['Combatant', 'Geometry']
            )

        true_result = query.candidate(monster)
        false_result = query.candidate(empty_monster)

        self.assertTrue(true_result)
        self.assertFalse(false_result)

    def testQueryCallbacks(self):
        self.ecs.register_component(Renderable)
        entity = self.ecs.create_entity()
        query = self.ecs.create_query(any_of=['Renderable'])

        on_added_callback1 = create_autospec(lambda e: e, return_value="Entity added")
        query.on_entity_added(on_added_callback1)
        entity.add('Renderable', {'char': '#', 'fg': '#0f0', 'bg': '#000'})
        query.candidate(entity)
        on_added_callback1.assert_called_once_with(entity)

        on_removed_callback1 = create_autospec(lambda e: e, return_value="Entity removed")
        query.on_entity_removed(on_removed_callback1)
        entity.remove('Renderable')
        query.candidate(entity)
        on_removed_callback1.assert_called_once_with(entity)

    def test_add_remove(self):
        self.ecs.register_component(Position)
        entity = self.ecs.create_entity()

        entity.add('Position', {'x': 10, 'y': 10})
        self.assertTrue(entity.has('Position'))
        entity['Position'].destroy()
        self.assertFalse(entity.has('Position'))

        entity.add('Position', {'x': 10, 'y': 10})
        self.assertTrue(entity.has('Position'))
        entity.remove('Position')
        self.assertFalse(entity.has('Position'))

    def test_query_caching(self):
        self.ecs.queries.hard_reset()
        self.ecs.register_component(Position)
        self.ecs.register_component(Renderable)

        system = System(self.ecs)
        for i in range(10):
            self.ecs.create_entity()

        player = self.ecs.create_entity()

        for entity in self.ecs.entities.get_all:
            entity.add('Position', {'x': 0.0, 'y': 0.0})
            # entity.add('Renderable', {'char': '@', 'fg': '#0f0', 'bg': '#000'})

        player.add('Position', {'x': 1.0, 'y': 2.0})

        loop = 0
        while loop <= 100:
            system.update()
            loop += 1

            if loop == 49:
                self.assertTrue(len(system._query.result) == 11)
            if loop == 50:
                player.add('Renderable', {'char': '@', 'fg': '#0f0', 'bg': '#000'})
            if loop == 51:
                self.assertTrue(len(system._query.result) == 10)

            if loop == 52:
                # player.remove('Renderable')
                player['Renderable'].remove()
            if loop == 90:
                self.assertTrue(len(system._query.result) == 11)


if __name__ == '__main__':
    unittest.main()
