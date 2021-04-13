from __future__ import annotations
from typing import *
import numpy as np
from itertools import zip_longest


def compose_dtype(fields, types):

    if not isinstance(types, list):
        types_list = []
        for _ in range(len(fields)):
            types_list.append(types)
    else:
        types_list = types

    dtype = []
    for f, t in zip(fields, types_list):
        dtype.append((f, t))
    return np.dtype(dtype)


class ComponentMeta(type):

    def __new__(mcs, clsname, bases, clsdict):
        clsobj = super().__new__(mcs, clsname, bases, clsdict)
        clsobj.name = str(clsname).upper()
        return clsobj


class Component(metaclass=ComponentMeta):
    _fields = []
    _types = []
    ctype: np.dtype

    def __init__(self, *args):
        for name, val in zip_longest(self._fields, args):
            setattr(self, name, val)
        self.ctype = compose_dtype(self._fields, self._types)


class Position(Component):
    _fields = ['x', 'y', 'z']
    _types  = [int, int, int]

    @property
    def xy(self):
        return self.x, self.y


class Renderable(Component):
    _fields = ['ch', 'fg', 'bg']
    _types  = [str, '3B', '3B']
