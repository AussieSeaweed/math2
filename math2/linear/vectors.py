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

    @property
    def x(self) -> float:
        return self[0] if len(self) else 0

    @property
    def y(self) -> float:
        return self[1] if len(self) > 1 else 0

    @property
    def z(self) -> float:
        return self[2] if len(self) > 2 else 0

    @property
    def w(self) -> float:
        return self[3] if len(self) > 3 else 0

    def parallel_to(self, other: Vector) -> bool:
        return isclose(abs(self @ other), abs(self) * abs(other))

    def orthogonal_to(self, other: Vector) -> bool:
        return isclose(self @ other, 0)

    def cross(self, other: Vector) -> Vector:
        if not (2 <= len(self) <= 3 and 2 <= len(other) <= 3):
            raise DimensionError('Calculating the cross product requires all vectors to have a length of 2 or 3')

        return Vector((
            self.y * other.z - other.y * self.z,
            self.z * other.x - other.z * self.x,
            self.x * other.y - other.x * self.y,
        ), (3,))

    def angle_between(self, other: Vector) -> float:
        return acos(self @ other / (abs(self) * abs(other)))

    def projection_on(self, other: Vector) -> Vector:
        return self @ other * other.unit
