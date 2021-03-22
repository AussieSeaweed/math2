from math import acos

from math2.linear.factories import row


def norm(m, p=2):
    return sum(s ** p for s in m) ** (1 / p)


def angle(u, v):
    return acos(u @ v / (abs(u) * abs(v)))


def unit(v):
    return v / abs(v)


def proj(u, v):
    return u @ v / abs(v) * unit(v)


def cross(u, v):
    if not (2 <= len(u) <= 3) or not (2 <= len(v) <= 3):
        raise ValueError('Length of operand not 2 or 3')

    a = u[0], u[1], (0 if len(v) == 2 else u[2])
    b = v[0], v[1], (0 if len(u) == 2 else v[2])

    return row((a[1] * b[2] - b[1] * a[2], a[2] * b[0] - b[2] * a[0], a[0] * b[1] - b[0] * a[1]))


def parallel(u, v):
    return abs(u @ v) == abs(v) * abs(u)


def orthogonal(u, v):
    return u @ v == 0
