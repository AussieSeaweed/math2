from math import acos

from math2.linear.factories import row
from math2.linear.matrices import Matrix


def norm(m: Matrix, p: float = 2) -> float:
    return sum(s ** p for s in m) ** (1 / p)


def angle_between(u: Matrix, v: Matrix) -> float:
    return acos(u @ v / (abs(u) * abs(v)))


def unit(v: Matrix) -> Matrix:
    return v / abs(v)


def project(u: Matrix, v: Matrix) -> Matrix:
    return u @ v / abs(v) * unit(v)


def cross(u: Matrix, v: Matrix) -> Matrix:
    if not (2 <= len(u) <= 3) or not (2 <= len(v) <= 3):
        raise ValueError('Length of operand not 2 or 3')

    a = u[0], u[1], (0 if len(v) == 2 else u[2])
    b = v[0], v[1], (0 if len(u) == 2 else v[2])

    return row((a[1] * b[2] - b[1] * a[2], a[2] * b[0] - b[2] * a[0], a[0] * b[1] - b[0] * a[1]))


def parallel(u: Matrix, v: Matrix) -> bool:
    return abs(u @ v) == abs(v) * abs(u)


def orthogonal(u: Matrix, v: Matrix) -> bool:
    return u @ v == 0
