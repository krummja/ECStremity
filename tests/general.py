from __future__ import annotations

import time

from ecstremity import Engine, Component

class Position(Component):
    name = "POSITION"
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

class Velocity(Component):
    name = "VELOCITY"
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y =y


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

            kinematics = ecs.create_query(all_of=['Position', 'Velocity'])

            now = time.time()
            dt = now - last_update

            for entity in kinematics.result:
                entity['POSITION'].x += entity['VELOCITY'].x * dt
                entity['POSITION'].y += entity['VELOCITY'].y * dt
                print(entity['POSITION'].x, entity['POSITION'].y)

            last_update = now

    start()

if __name__ == '__main__':
    main()
