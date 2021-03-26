from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from itertools import product, starmap
from operator import matmul
from typing import Any, Literal, Optional, Union, overload

from auxiliary import chunked, flattened

from math2.linear.exceptions import DimensionError
from math2.linear.tensors import Tensor
from math2.linear.vectors import Vector


class Matrix(Tensor):
    def __init__(self, values: Iterable[float], dimensions: Iterable[int]):
        super().__init__(values, dimensions)

        if len(self.dimensions) != 2:
            raise DimensionError('Matrices should have two dimensions')

    @property
    def row_dimension(self) -> int:
        return self.dimensions[0]

    @property
    def column_dimension(self) -> int:
        return self.dimensions[1]

    @property
    def rows(self) -> Iterator[Matrix]:
        return (Matrix(row, (1, self.column_dimension)) for row in chunked(self, self.column_dimension))

    @property
    def columns(self) -> Iterator[Matrix]:
        for j in range(self.column_dimension):
            yield Matrix((self[i, j] for i in range(self.row_dimension)), (self.row_dimension, 1))

    @property
    def determinant(self) -> float:
        raise NotImplementedError  # TODO

    @property
    def eigenpairs(self) -> Iterator[tuple[float, Vector]]:
        raise NotImplementedError  # TODO

    @property
    def eigenvalues(self) -> Iterator[float]:
        return (pair[0] for pair in self.eigenpairs)

    @property
    def eigenvectors(self) -> Iterator[Vector]:
        return (pair[1] for pair in self.eigenpairs)

    def is_square(self) -> bool:
        return self.row_dimension == self.column_dimension

    def __mul__(self, other: Union[float, Matrix, Vector]) -> Matrix:
        if isinstance(other, Matrix):
            if self.column_dimension == other.row_dimension:
                return Matrix(
                    starmap(matmul, product(self.rows, (other ** 'T').rows)),
                    (self.row_dimension, other.column_dimension),
                )
            else:
                raise DimensionError('The matrices do not have valid dimensions for multiplication')
        elif isinstance(other, Vector):
            return self * Matrix(other, (other.dimension, 1))
        else:
            return super().__mul__(other)

    def __pow__(self, power: Union[int, Literal['T']], modulo: Optional[Any] = None) -> Matrix:
        if modulo is None:
            if power == 'T':
                return Matrix(flattened(self.columns), reversed(self.dimensions))
            elif isinstance(power, int):
                raise NotImplementedError

        return NotImplemented

    @overload
    def __getitem__(self, i: int) -> float:
        ...

    @overload
    def __getitem__(self, s: slice) -> Sequence[float]:
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

    def __getitem__(
            self, i: Union[int, slice, tuple[int, int], tuple[int, slice], tuple[slice, int], tuple[slice, slice]],
    ) -> Union[float, Sequence[float], float, Matrix]:
        if isinstance(i, tuple):
            try:
                i, j = i
            except ValueError:
                raise ValueError('Matrices only support two indices, one each for row and column')

            if isinstance(i, int) and isinstance(j, int):
                return self[i * self.column_dimension + j]
            elif isinstance(i, int) and isinstance(j, slice):
                row = tuple(self.rows)[i][j]

                return Matrix(row, (1, len(row)))
            elif isinstance(i, slice) and isinstance(j, int):
                column = tuple(self.columns)[j][i]

                return Matrix(column, (len(column), 1))
            elif isinstance(i, slice) and isinstance(j, slice):
                rows = tuple(row[j] for row in tuple(self.rows)[i])

                return Matrix(flattened(rows), (len(rows), len(rows[0]) if rows else 0))
            else:
                raise ValueError('Indices must be of instance int or slice')
        else:
            return super().__getitem__(i)
