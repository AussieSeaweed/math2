from math import acos

from math2.linalg import row


def norm(m, p=2):
    return sum(s ** p for s in m) ** (1 / p)


def angle_between(u, v):
    return acos(u @ v / (abs(u) * abs(v)))


def unit(v):
    return v / abs(v)


def project(u, v):
    return u @ v / abs(v) * unit(v)


def cross(u, v):
    if not (2 <= len(u) <= 3) or not (2 <= len(v) <= 3):
        raise ValueError('Length of operand not 2 or 3')

    u = u[0], u[1], (0 if len(v) == 2 else u[2])
    v = v[0], v[1], (0 if len(u) == 2 else v[2])

    return row((u[1] * v[2] - v[1] * u[2], u[2] * v[0] - v[2] * u[0], u[0] * v[1] - v[0] * u[1]))


def parallel(u, v):
    return abs(u @ v) == abs(v) * abs(u)


def orthogonal(u, v):
    return u @ v == 0
