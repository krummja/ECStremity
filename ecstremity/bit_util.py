

def subtract_bit(num, bit):
    return num & ~(1 << bit)


def add_bit(num, bit):
    return num | (1 << bit)


def has_bit(num, bit):
    return (num >> bit) % 2 != 0


def bit_intersection(n1, n2):
    return n1 & n2
