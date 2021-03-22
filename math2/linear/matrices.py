from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from itertools import chain
from math import sqrt
from typing import Any, Optional, Union, overload

from auxiliary import const, iter_equal

from math2.linear.exceptions import DimensionError


class Matrix(Sequence[float]):
    def __init__(self, it: Iterable[Iterable[float]] = ()):
        self.__values = tuple(map(tuple[float], it))

        if not const(map(len, self.__values)):
            raise DimensionError('The number of columns are not constant')

        if self.column_count == 0:
            self.__values = ()

    @property
    def rows(self) -> Iterator[Matrix]:
        return (Matrix((row,)) for row in self.__values)

    @property
    def columns(self) -> Iterator[Matrix]:
        return (Matrix(((self.__values[j][i] for j in range(self.row_count)),)) for i in range(self.column_count))

    @property
    def row_count(self) -> int:
        return len(self.__values)

    @property
    def column_count(self) -> int:
        return len(self.__values[0]) if self.__values else 0

    @property
    def dimensions(self) -> tuple[int, int]:
        return self.row_count, self.column_count

    def __pos__(self) -> Matrix:
        return Matrix((+scalar for scalar in row) for row in self.rows)

    def __neg__(self) -> Matrix:
        return Matrix((-scalar for scalar in row) for row in self.rows)

    def __add__(self, other: Matrix) -> Matrix:
        if not isinstance(other, Matrix):
            return NotImplemented
        elif self.dimensions == other.dimensions:
            return Matrix((x + y for x, y in zip(row1, row2)) for row1, row2 in zip(self.rows, other.rows))
        else:
            raise DimensionError('The matrices do not have identical dimensions')

    def __mul__(self, other: Union[Matrix, float]) -> Matrix:
        if not isinstance(other, Matrix):
            try:
                return Matrix((scalar * other for scalar in row) for row in self.__values)
            except TypeError:
                return NotImplemented
        elif self.column_count == other.row_count:
            return Matrix((row @ column for column in other.columns) for row in self.rows)
        else:
            raise DimensionError('The matrices do not have valid dimensions for multiplication')

    def __matmul__(self, other: Matrix) -> float:
        if not isinstance(other, Matrix):
            return NotImplemented
        elif self.dimensions == other.dimensions:
            return sum(sum(x * y for x, y in zip(row1, row2)) for row1, row2 in zip(self.rows, other.rows))
        else:
            raise DimensionError('The matrices do not have identical dimensions')

    def __sub__(self, other: Matrix) -> Matrix:
        try:
            return self + -other
        except TypeError:
            return NotImplemented

    def __rmul__(self, other: float) -> Matrix:
        return self * other

    def __truediv__(self, other: float) -> Matrix:
        try:
            return self * (1 / other)
        except TypeError:
            return NotImplemented

    def __pow__(self, power: str, modulo: Optional[str] = None) -> Matrix:
        if modulo is None:
            if power == 'T':
                return Matrix(self.columns)

        return NotImplemented

    def __abs__(self) -> float:
        return sqrt(sum(x ** 2 for x in self))

    def __iter__(self) -> Iterator[float]:
        return chain(*self.__values)

    @overload
    def __getitem__(self, i: int) -> float:
        ...

    @overload
    def __getitem__(self, i: slice) -> Sequence[float]:
        ...

    @overload
    def __getitem__(self, i: tuple[int, int]) -> float:
        ...

    @overload
    def __getitem__(self, i: tuple[int, slice]) -> Matrix:
        ...

    @overload
    def __getitem__(self, i: tuple[slice, int]) -> Matrix:
        ...

    @overload
    def __getitem__(self, i: tuple[slice, slice]) -> Matrix:
        ...

    def __getitem__(self, i: Union[int, slice, Iterable[Union[int, slice]]]) -> Union[float, Sequence[float], Matrix]:
        if isinstance(i, Iterable):
            i, j = i

            if isinstance(i, int) and isinstance(j, int):
                return self.__values[i][j]
            elif isinstance(i, int) and isinstance(j, slice):
                return Matrix((self.__values[i][j],))
            elif isinstance(i, slice) and isinstance(j, int):
                return Matrix((row[j],) for row in self.__values[i])
            elif isinstance(i, slice) and isinstance(j, slice):
                return Matrix(row[j] for row in self.__values[i])
            else:
                return NotImplemented
        else:
            return tuple(self)[i]

    def __len__(self) -> int:
        return self.row_count * self.column_count

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Matrix):
            return self.__values == other.__values
        elif isinstance(other, Iterable):
            return iter_equal(self, other)
        else:
            return NotImplemented

    def __repr__(self) -> str:
        return str(self.__values)
