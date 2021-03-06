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
