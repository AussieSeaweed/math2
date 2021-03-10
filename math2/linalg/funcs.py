from collections.abc import Sequence
from itertools import chain

from math2.linalg.data import Vector


def zeros(size: int) -> Vector:
    return Vector(0 for _ in range(size))


def ones(size: int) -> Vector:
    return Vector(1 for _ in range(size))


def full(size: int, value: float) -> Vector:
    return Vector(value for _ in range(size))


def deleted(vector: Vector, index: int) -> Vector:
    return Vector(x for i, x in enumerate(vector) if i != index)


def inserted(vector: Vector, index: int, value: float) -> Vector:
    return Vector(chain(vector[:index], (value,), vector[index:]))


def replaced(vector: Vector, index: int, value: float) -> Vector:
    return Vector(value if index == i else x for i, x in enumerate(vector))


def solve(m: Sequence[Sequence[float]], y: Sequence[float]) -> Sequence[float]:
    """Solves mx = y for x.

    :param m: The matrix.
    :param y: The product.
    :return: The factor.
    """
    if not m:
        return []
    elif len(m) == 1:
        return [y[0] / m[0][0]]
    elif len(m) == 2:
        x = [0.0, 0.0]
        x[1] = (m[1][0] * y[0] - m[0][0] * y[1]) / (m[0][1] * m[1][0] - m[0][0] * m[1][1])
        x[0] = (y[0] - m[0][1] * x[1]) / m[0][0]

        return x
    else:
        raise NotImplementedError
