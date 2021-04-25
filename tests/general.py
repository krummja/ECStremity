from __future__ import annotations

import time

from ecstremity import Engine, Component

class Position(Component):
    name = "POSITION"
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

class IsPlayer(Component):
    """Is player flag."""

class Velocity(Component):
    name = "VELOCITY"
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y =y

    def on_event(self, evt):
        print(f"Event Name: {evt.name}")
        print(f"Event Data: {evt.data}")

    def on_try_move(self, evt):
        print(f"Velocity.on_try_move() called in response to event {evt.comp_id}!")


def main():
    global last_update
    ecs = Engine()

    def start():
        ecs.register_component(Position)
        ecs.register_component(Velocity)

        monster = ecs.create_entity()
        monster.add("Position", {'x': 0, 'y': 0})
        monster.add("Velocity", {'x': 1, 'y': 0})

        last_update = time.time()
        loop(last_update)


    def loop(last_update):
        while True:

            # kinematics = ecs.create_query(all_of=['Position', 'Velocity'])

            now = time.time()
            dt = now - last_update

            # for entity in kinematics.result:
            #     entity['POSITION'].x += entity['VELOCITY'].x * dt
            #     entity['POSITION'].y += entity['VELOCITY'].y * dt
            #     delta = (entity['POSITION'].x, entity['POSITION'].y)
            #     entity.fire_event('try_move', delta)

            last_update = now

    start()

if __name__ == '__main__':
    # main()

    ecs = Engine()
    ecs.register_component(Position)
    ecs.register_component(IsPlayer)

    monster = ecs.create_entity()
    monster.add('position', {'x': 10, 'y': 0})
    monster.add('isplayer', {})

    print(monster.has('position'))
    print(monster.has('isplayer'))

    positional = ecs.create_query(all_of=['position'])
    for e in positional.result:
        print(e['position'].x)
