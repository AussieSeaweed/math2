from math2.linalg.tensors import Vector


def zeros(size: int) -> Vector:
    return Vector(0 for _ in range(size))


def ones(size: int) -> Vector:
    return Vector(1 for _ in range(size))


def full(size: int, value: float) -> Vector:
    return Vector(value for _ in range(size))


def deleted(vector: Vector, index: int) -> Vector:
    vector = Vector(vector)
    del vector[index]

    return vector


def inserted(vector: Vector, index: int, value: float) -> Vector:
    vector = Vector(vector)
    vector.insert(index, value)

    return vector


def replaced(vector: Vector, index: int, value: float) -> Vector:
    vector = Vector(vector)
    vector[index] = value

    return vector
