from __future__ import annotations

from collections import MutableSequence
from typing import Iterable, Union, overload

from auxiliary import const_len


class Vector(MutableSequence[float]):
    def __init__(self, values: Iterable[float] = ()):
        self.__values = list(values)

    @overload
    def __getitem__(self, i: int) -> float:
        ...

    @overload
    def __getitem__(self, s: slice) -> Vector:
        ...

    def __getitem__(self, i: Union[int, slice]) -> Union[float, Vector]:
        if isinstance(i, int):
            return self.__values[i]
        else:
            return Vector(self.__values[i])

    @overload
    def __setitem__(self, i: int, o: float) -> None:
        ...

    @overload
    def __setitem__(self, s: slice, o: Iterable[float]) -> None:
        ...

    def __setitem__(self, i: Union[int, slice], o: Union[float, Iterable[float]]) -> None:
        if isinstance(i, int) and isinstance(o, float):
            self.__values[i] = o
        elif isinstance(i, slice) and isinstance(o, Iterable):
            self.__values[i] = o
        else:
            raise TypeError('Invalid argument types')

    @overload
    def __delitem__(self, i: int) -> None:
        ...

    @overload
    def __delitem__(self, i: slice) -> None:
        ...

    def __delitem__(self, i: Union[int, slice]) -> None:
        del self.__values[i]

    def __len__(self) -> int:
        return len(self.__values)

    def __pos__(self) -> Vector:
        return Vector(self)

    def __neg__(self) -> Vector:
        return Vector(-x for x in self)

    @const_len
    def __add__(self, other: Iterable[float]) -> Vector:
        return Vector(x + y for x, y in zip(self, other))

    @const_len
    def __sub__(self, other: Iterable[float]) -> Vector:
        return Vector(x - y for x, y in zip(self, other))

    def __mul__(self, other: float) -> Vector:
        return Vector(x * other for x in self)

    def __rmul__(self, other: float) -> Vector:
        return self * other

    def __truediv__(self, other: float) -> Vector:
        return Vector(x / other for x in self)

    @const_len
    def __matmul__(self, other: Iterable[float]) -> float:
        return sum(x * y for x, y in zip(self, other))

    @const_len
    def __iadd__(self, other: Iterable[float]) -> Vector:
        self.__values = (self + other).__values

        return self

    @const_len
    def __isub__(self, other: Iterable[float]) -> Vector:
        self.__values = (self - other).__values

        return self

    def __imul__(self, other: float) -> Vector:
        self.__values = (self * other).__values

        return self

    def __itruediv__(self, other: float) -> Vector:
        self.__values = (self / other).__values

        return self

    def insert(self, index: int, value: float) -> None:
        self.__values.insert(index, value)
