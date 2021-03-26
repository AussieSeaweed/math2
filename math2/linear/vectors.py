from __future__ import annotations

from collections.abc import Iterable
from math import acos, isclose

from math2.linear.exceptions import DimensionError
from math2.linear.tensors import Tensor


class Vector(Tensor):
    def __init__(self, values: Iterable[float], dimensions: Iterable[int]):
        super().__init__(values, dimensions)

        if len(self.dimensions) != 1:
            raise DimensionError('Vectors should only have one dimension')

    @property
    def dimension(self) -> int:
        return self.dimensions[0]

    @property
    def unit(self) -> Vector:
        return self / abs(self)

    def parallel_to(self, other: Vector) -> bool:
        return isclose(abs(self @ other), abs(self) * abs(other))

    def orthogonal_to(self, other: Vector) -> bool:
        return isclose(self @ other, 0)

    def cross(self, other: Vector) -> Vector:
        if not (2 <= len(self) <= 3 and 2 <= len(other) <= 3):
            raise DimensionError('Calculating the cross product requires all vectors to have a length of 2 or 3')

        a = self[0], self[1], self[2] if len(self) == 3 else 0
        b = other[0], other[1], other[2] if len(other) == 3 else 0

        return Vector((a[1] * b[2] - b[1] * a[2], a[2] * b[0] - b[2] * a[0], a[0] * b[1] - b[0] * a[1]), (3,))

    def angle_between(self, other: Vector) -> float:
        return acos(self @ other / (abs(self) * abs(other)))

    def projection_on(self, other: Vector) -> Vector:
        return self @ other * other.unit
