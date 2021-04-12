from __future__ import annotations
from typing import *
import numpy as np


def _nearest_pow2(v):
    # From http://graphics.stanford.edu/~seander/bithacks.html#RoundUpPowerOf2
    # Credit: Sean Anderson
    v -= 1
    v |= v >> 1
    v |= v >> 2
    v |= v >> 4
    v |= v >> 8
    v |= v >> 16
    return v + 1


class BaseComponent:

    def __init__(self, name: str, dim: Tuple[int, ...], datatype, size: int = 0) -> None:
        self.name: str = name
        self.datatype = datatype
        self.capacity = size
        self._dim = dim

        if dim == (1,):
            self._buffer = np.empty(size, dtype=datatype)
            self.resize = self._resize_singledim
        elif dim > (1,):
            self._buffer = np.empty((size,) + dim, dtype=datatype)
            self.resize = self._resize_multidim
        else:
            raise ValueError("Component dim must be >= 1")

    @property
    def dim(self):
        return self._dim

    def assert_capacity(self, new_capacity):
        if self.capacity < new_capacity:
            self.resize(_nearest_pow2(new_capacity))
            self.capacity = new_capacity

    def reallocate(self, old_selector, new_selector):
        self._buffer[new_selector] = self._buffer[old_selector]

    def __getitem__(self, selector):
        return self._buffer[selector]

    def __setitem__(self, selector, data):
        self._buffer[selector] = data
        assert self.datatype == self._buffer.dtype, 'NumPy dtype may not change.'

    def _resize_multidim(self, count):
        shape = (count,) + self._dim
        try:
            self._buffer.resize(shape)
        except ValueError:
            self._buffer = np.resize(self._buffer, shape)

    def _resize_singledim(self, count):
        self._buffer = np.resize(self._buffer, count)

    def __repr__(self):
        return f"<Component: {self.name}>"
