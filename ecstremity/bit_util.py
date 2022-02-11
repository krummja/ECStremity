
def subtract_bit(num: int, bit: int) -> int:
    return num & ~(1 << bit)


def add_bit(num: int, bit: int) -> int:
    return num | (1 << bit)


def has_bit(num: int, bit: int) -> bool:
    return (num >> bit) % 2 != 0


def bit_intersection(n1: int, n2: int) -> int:
    return n1 & n2
