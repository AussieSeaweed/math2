from collections.abc import Callable, Sequence
from itertools import product, starmap
from typing import Optional

from auxiliary import default, flattened

from math2.linear.matrices import Matrix
from math2.linear.vectors import Vector


def row(scalars: Sequence[float]) -> Matrix:
    return Matrix(scalars, (1, len(scalars)))


def column(scalars: Sequence[float]) -> Matrix:
    return Matrix(scalars, (len(scalars), 1))


def rows(scalars: Sequence[Sequence[float]]) -> Matrix:
    if not isinstance(scalars, Sequence):
        scalars = tuple(scalars)

    return Matrix(flattened(scalars), (len(scalars), len(scalars[0]) if scalars else 0))


def columns(scalars: Sequence[Sequence[float]]) -> Matrix:
    return rows(scalars) ** 'T'


def vector(scalars: Sequence[float]) -> Vector:
    return Vector(scalars, (len(scalars),))


def empty_vector() -> Vector:
    return Vector((), (0,))


def empty_matrix() -> Matrix:
    return Matrix((), (0, 0))


def singleton_vector(scalar: float) -> Vector:
    return Vector((scalar,), (1,))


def singleton_matrix(scalar: float) -> Matrix:
    return Matrix((scalar,), (1, 1))


def full_vector(func: Callable[[int], float], dimension: int) -> Vector:
    return Vector(map(func, range(dimension)), (dimension,))


def full_matrix(
        func: Callable[[int, int], float],
        row_dimension: int,
        column_dimension: Optional[int] = None,
) -> Matrix:
    return Matrix(
        starmap(func, product(range(row_dimension), range(default(column_dimension, row_dimension)))),
        (row_dimension, default(column_dimension, row_dimension)),
    )


def zero_vector(dimension: int) -> Vector:
    return full_vector(lambda i: 0, dimension)


def zero_matrix(row_dimension: int, column_dimension: Optional[int] = None) -> Matrix:
    return full_matrix(lambda r, c: 0, row_dimension, column_dimension)


def one_vector(dimension: int) -> Vector:
    return full_vector(lambda i: 1, dimension)


def one_matrix(row_dimension: int, column_dimension: Optional[int] = None) -> Matrix:
    return full_matrix(lambda r, c: 1, row_dimension, column_dimension)


def random_vector(dimension: int) -> Vector:
    from random import random

    return full_vector(lambda i: random(), dimension)


def random_matrix(row_dimension: int, column_dimension: Optional[int] = None) -> Matrix:
    from random import random

    return full_matrix(lambda r, c: random(), row_dimension, column_dimension)


def diagonal_matrix(scalars: Sequence[float]) -> Matrix:
    return full_matrix(lambda r, c: scalars[r] if r == c else 0, len(scalars))


def identity_matrix(row_dimension: int, column_dimension: Optional[int] = None) -> Matrix:
    return full_matrix(lambda r, c: 1 if r == c else 0, row_dimension, column_dimension)
