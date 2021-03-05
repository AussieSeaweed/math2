from math2.linalg.data import Vector


def zeros(size: int) -> Vector:
    return Vector(0 for _ in range(size))


def ones(size: int) -> Vector:
    return Vector(1 for _ in range(size))


def full(size: int, value: float) -> Vector:
    return Vector(value for _ in range(size))


def replaced(vector: Vector, index: int, value: float) -> Vector:
    return Vector(value if index == i else x for i, x in enumerate(vector))
