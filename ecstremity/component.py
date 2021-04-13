from __future__ import annotations
from typing import *
from inspect import Parameter, Signature, signature
import numpy as np


def make_signature(names):
    params = []
    for name in names:
        param = Parameter(name, Parameter.POSITIONAL_OR_KEYWORD)
        params.append(param)
    return Signature(*params)


class ComponentMeta(type):

    def __new__(mcs, clsname, bases, clsdict):
        clsobj = super().__new__(mcs, clsname, bases, clsdict)
        clsobj.name = str(clsname).upper()
        return clsobj


class Component(metaclass=ComponentMeta):

    __signature__ = make_signature([])
    __properties__ = [(), {}]

    def __init__(self, *args, **kwargs) -> None:
        bound = self.__signature__.bind(*args, **kwargs)
        for name, value in bound.arguments.items():
            setattr(self, name, val)



class Position(Component):
    pass

if __name__ == '__main__':
    position = Position(10, 10)
    print(position.signature)
