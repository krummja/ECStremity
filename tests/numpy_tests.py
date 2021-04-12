from pprint import pprint
from ecstremity.accessors import *
from ecstremity.components import *
from ecstremity.global_allocator import *
from ecstremity.table import *

import numpy as np
from collections import namedtuple


if __name__ == '__main__':
    tile_graphic = np.dtype([("ch", np.int32), ("fg", "3B"), ("bg", "3B")])

    allocator = GlobalAllocator([BaseComponent('renderable', (3,), tile_graphic)],
                                allocation_scheme = ((1, 0, 1, 1, 0),
                                                     (1, 1, 1, 1, 1)))

    def add_tile_graphic(char, fg, bg, allocator=allocator):
        allocator.add({'ch': char, 'fg': fg, 'bg': bg})
