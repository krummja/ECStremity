from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from ecstremity.entity import Entity
    from ecstremity.world import World


class ComponentMeta(type):

    def __new__(mcs, clsname, bases, clsdict):
        clsobj = super().__new__(mcs, clsname, bases, clsdict)
        clsobj.name = str(clsname).upper()
        return clsobj


class Component(metaclass=ComponentMeta):
    world: World
    init_props: Dict[str, Any]
    entity: Entity

    def __str__(self) -> str:
        return str(self.__init__.__dict__)


class Position(Component):

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


if __name__ == '__main__':
    pos1 = Position(20, 2)
    print(pos1.x)
    print(pos1)
