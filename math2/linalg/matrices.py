from collections.abc import Iterable, Sequence
from itertools import chain
from math import sqrt

from auxiliary import const, iter_equal

from math2.linalg.exceptions import DimensionError


class Matrix(Sequence):
    def __init__(self, it=()):
        self.__values = tuple(map(tuple, it))

        if not const(map(len, self.__values)):
            raise DimensionError('The number of columns are not constant')

        if self.column_count == 0:
            self.__values = ()

    @property
    def rows(self):
        return (Matrix((row,)) for row in self.__values)

    @property
    def columns(self):
        return (Matrix(((self.__values[j][i] for j in range(self.row_count)),)) for i in range(self.column_count))

    @property
    def row_count(self):
        return len(self.__values)

    @property
    def column_count(self):
        return len(self.__values[0]) if self.__values else 0

    @property
    def dimensions(self):
        return self.row_count, self.column_count

    def __pos__(self):
        return Matrix((+scalar for scalar in row) for row in self.rows)

    def __neg__(self):
        return Matrix((-scalar for scalar in row) for row in self.rows)

    def __add__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        elif self.dimensions == other.dimensions:
            return Matrix((x + y for x, y in zip(row1, row2)) for row1, row2 in zip(self.rows, other.rows))
        else:
            raise DimensionError('The matrices do not have identical dimensions')

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            try:
                return Matrix((scalar * other for scalar in row) for row in self.__values)
            except TypeError:
                return NotImplemented
        elif self.column_count == other.row_count:
            return Matrix((row @ column for column in other.columns) for row in self.rows)
        else:
            raise DimensionError('The matrices do not have valid dimensions for multiplication')

    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        elif self.dimensions == other.dimensions:
            return sum(sum(x * y for x, y in zip(row1, row2)) for row1, row2 in zip(self.rows, other.rows))
        else:
            raise DimensionError('The matrices do not have identical dimensions')

    def __sub__(self, other):
        try:
            return self + -other
        except TypeError:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        try:
            return self * (1 / other)
        except TypeError:
            return NotImplemented

    def __pow__(self, power, modulo=None):
        if modulo is None:
            if power == 'T':
                return Matrix(self.columns)

        return NotImplemented

    def __abs__(self):
        return sqrt(sum(x ** 2 for x in self))

    def __iter__(self):
        return chain(*self.__values)

    def __getitem__(self, i):
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
            return tuple(self)[i]

    def __len__(self):
        return self.row_count * self.column_count

    def __eq__(self, other):
        if isinstance(other, Matrix):
            return self.__values == other.__values
        elif isinstance(other, Iterable):
            return iter_equal(self, other)
        else:
            return NotImplemented

    def __repr__(self):
        return str(self.__values)
