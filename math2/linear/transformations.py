from __future__ import annotations

from math2.linear.matrices import Matrix


class Transformation:
    def __init__(self, matrix: Matrix):
        self.matrix = matrix

    @property
    def from_dimension(self) -> int:
        return self.matrix.column_dimension

    @property
    def to_dimension(self) -> int:
        return self.matrix.row_dimension

    def __pos__(self) -> Transformation:
        return self

    def __neg__(self) -> Transformation:
        return Transformation(-self.matrix)

    def __add__(self, other: Transformation) -> Transformation:
        if isinstance(other, Transformation):
            return Transformation(self.matrix + other.matrix)
        else:
            return NotImplemented

    def __sub__(self, other: Transformation) -> Transformation:
        return self + -other

    def __mul__(self, other: float) -> Transformation:
        try:
            return Transformation(self.matrix * other)
        except TypeError:
            return NotImplemented

    def __rmul__(self, other: float) -> Transformation:
        return self * other

    def __truediv__(self, other: float) -> Transformation:
        try:
            return self * (1 / other)
        except TypeError:
            return NotImplemented
