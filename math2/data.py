from __future__ import annotations

from collections import Iterable, MutableSequence
from itertools import zip_longest
from math import sqrt
from typing import Union, overload


class Vector(MutableSequence[float]):
    """Vector is the class for vectors."""

    def __init__(self, values: Iterable[float] = ()):
        self.__values = list(values)

    def __repr__(self) -> str:
        return f'Vector({self.__values})'

    @overload
    def __getitem__(self, i: int) -> float: ...

    @overload
    def __getitem__(self, s: slice) -> MutableSequence[float]: ...

    def __getitem__(self, i: Union[int, slice]) -> Union[float, MutableSequence[float]]:
        return self.__values[i]

    @overload
    def __setitem__(self, i: int, o: float) -> None: ...

    @overload
    def __setitem__(self, s: slice, o: Iterable[float]) -> None: ...

    def __setitem__(self, i: Union[int, slice], o: Union[float, Iterable[float]]) -> None:
        if isinstance(i, int) and isinstance(o, float):
            self.__values[i] = o
        elif isinstance(i, slice) and isinstance(o, Iterable):
            self.__values[i] = o
        else:
            raise TypeError('Invalid type combo')

    @overload
    def __delitem__(self, i: int) -> None: ...

    @overload
    def __delitem__(self, i: slice) -> None: ...

    def __delitem__(self, i: Union[int, slice]) -> None:
        del self[i]

    def __len__(self) -> int:
        return len(self.__values)

    def __add__(self, other: Vector) -> Vector:
        return Vector(x + y for x, y in zip_longest(self, other, fillvalue=0))

    def __sub__(self, other: Vector) -> Vector:
        return Vector(x - y for x, y in zip_longest(self, other, fillvalue=0))

    def __mul__(self, other: float) -> Vector:
        return Vector(x * other for x in self)

    def __rmul__(self, other: float) -> Vector:
        return self * other

    def __truediv__(self, other: float) -> Vector:
        return Vector(x / other for x in self)

    def __matmul__(self, other: Vector) -> float:
        return sum(x * y for x, y in zip(self, other))

    def __abs__(self) -> float:
        return sqrt(sum(x * x for x in self))

    def insert(self, index: int, value: float) -> None:
        self.__values.insert(index, value)

    @property
    def x(self) -> float:
        return self[0]

    @x.setter
    def x(self, value: float) -> None:
        self[0] = value

    @property
    def y(self) -> float:
        return self[1]

    @y.setter
    def y(self, value: float) -> None:
        self[1] = value

    @property
    def z(self) -> float:
        return self[2]

    @z.setter
    def z(self, value: float) -> None:
        self[2] = value


def zeros(n: int) -> Vector:
    return Vector(0 for _ in range(n))


def full(n: int, v: float) -> Vector:
    return Vector(v for _ in range(n))


def copy(vector: Vector) -> Vector:
    return Vector(x for x in vector)


def delete(vector: Vector, i: int) -> Vector:
    vector = copy(vector)
    del vector[i]

    return vector


def insert(vector: Vector, i: int, v: float) -> Vector:
    vector = copy(vector)
    vector.insert(i, v)

    return vector


def replace(vector: Vector, i: int, v: float) -> Vector:
    vector = copy(vector)
    vector[i] = v

    return vector


def maximum(vector: Vector, v: float) -> Vector:
    return Vector(max(x, v) for x in vector)
