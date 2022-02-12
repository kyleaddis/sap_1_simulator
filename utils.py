def int_to_bin(i, bits):
    if bits == 8:
        return str(format(i, '08b'))
    if bits == 6:
        return str(format(i, '06b'))
    if bits == 4:
        return str(format(i, '04b'))


def binary_addition(a, b):
    _a = int(a, 2)
    _b = int(b, 2)
    _sum = _a + _b
    return int_to_bin(_sum, 8)


def binary_subtraction(a, b):
    _a = int(a, 2)
    _b = int(b, 2)
    _sum = _a - _b
    if _sum < 1:
        _sum = bin(_sum & (2**8 - 1))
        _sum = int(_sum, 2)
    return int_to_bin(_sum, 8)


def hex_to_bin(hex, bits):
    _b = list(hex)
    _b = int(_b[0], 16)
    return int_to_bin(_b, bits)


def hex_to_int(hex):
    _b = list(hex)
    _b = int(_b[0], 16)
    return _b
