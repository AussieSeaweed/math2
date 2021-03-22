from collections.abc import Iterable
from functools import partial
from itertools import product, starmap
from math import sqrt
from operator import add, matmul, mul, neg, pos

from auxiliary import chunked, flattened

from math2.linear.exceptions import DimensionError


class Matrix(list):
    def __init__(self, values, row_count, col_count):
        super().__init__(values)

        self.row_count = row_count
        self.col_count = col_count

        if len(self) != self.row_count * self.col_count:
            raise DimensionError('The values do not fit the required number of rows and columns')

    @property
    def rows(self):
        return (Matrix(row, 1, self.col_count) for row in chunked(self, self.col_count))

    @property
    def cols(self):
        return (Matrix((self[i, j] for i in range(self.row_count)), self.row_count, 1) for j in range(self.col_count))

    @property
    def dims(self):
        return self.row_count, self.col_count

    def __pos__(self):
        return Matrix(map(pos, self), self.row_count, self.col_count)

    def __neg__(self):
        return Matrix(map(neg, self), self.row_count, self.col_count)

    def __add__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        elif self.dims == other.dims:
            return Matrix(starmap(add, zip(self, other)), self.row_count, self.col_count)
        else:
            raise DimensionError('The matrices do not have identical dimensions')

    def __sub__(self, other):
        try:
            return self + -other
        except TypeError:
            return NotImplemented

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            try:
                return Matrix(map(partial(mul, other), self), self.row_count, self.col_count)
            except TypeError:
                return NotImplemented
        elif self.col_count == other.row_count:
            return Matrix(starmap(matmul, product(self.rows, (other ** 'T').rows)), self.row_count, other.col_count)
        else:
            raise DimensionError('The matrices do not have valid dimensions for multiplication')

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        try:
            return self * (1 / other)
        except TypeError:
            return NotImplemented

    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        elif self.dims == other.dims:
            return sum(starmap(mul, zip(self, other)))
        else:
            raise DimensionError('The matrices do not have identical dimensions')

    def __pow__(self, power, modulo=None):
        if modulo is None:
            if power == 'T':
                return Matrix(flattened(self.cols), self.col_count, self.row_count)

        return NotImplemented

    def __abs__(self):
        return sqrt(sum(x ** 2 for x in self))

    def __getitem__(self, i):
        if isinstance(i, Iterable):
            try:
                i, j = i
            except ValueError:
                return NotImplemented

            if isinstance(i, int) and isinstance(j, int):
                return self[i * self.col_count + j]
            elif isinstance(i, int) and isinstance(j, slice):
                row = tuple(self.rows)[i][j]

                return Matrix(row, 1, len(row))
            elif isinstance(i, slice) and isinstance(j, int):
                col = tuple(self.cols)[j][i]

                return Matrix(col, len(col), 1)
            elif isinstance(i, slice) and isinstance(j, slice):
                rows = tuple(row[j] for row in tuple(self.rows)[i])

                return Matrix(flattened(rows), len(rows), len(rows[0]) if rows else 0)
            else:
                return NotImplemented
        else:
            return super().__getitem__(i)

    def __eq__(self, other):
        if isinstance(other, Matrix):
            return self.dims == other.dims and super().__eq__(other)
        else:
            return super().__eq__(other)
