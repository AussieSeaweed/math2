from __future__ import annotations

from collections.abc import Iterable, MutableSequence
from typing import SupportsFloat, Union, cast, overload

from auxiliary import const_len


class Vector(MutableSequence[float]):
    def __init__(self, it: Iterable[float] = ()):
        self.__values = list(it)

    @overload
    def __getitem__(self, i: int) -> float:
        ...

    @overload
    def __getitem__(self, s: slice) -> Vector:
        ...

    def __getitem__(self, i: Union[int, slice]) -> Union[float, Vector]:
        return self.__values[i] if isinstance(i, int) else Vector(self.__values[i])

    @overload
    def __setitem__(self, i: int, o: float) -> None:
        ...

    @overload
    def __setitem__(self, s: slice, o: Iterable[float]) -> None:
        ...

    def __setitem__(self, i: Union[int, slice], o: Union[float, Iterable[float]]) -> None:
        if isinstance(i, int) and isinstance(o, SupportsFloat):
            self.__values[i] = float(o)
        elif isinstance(i, slice) and isinstance(o, Iterable):
            self.__values[i] = o
        else:
            raise TypeError('Unknown Type')

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
        self.__values = [x + y for x, y in zip(self, other)]

        return self

    @const_len
    def __isub__(self, other: Iterable[float]) -> Vector:
        self.__values = [x - y for x, y in zip(self, other)]

        return self

    def __imul__(self, other: float) -> Vector:
        self.__values = [x * other for x in self]

        return self

    def __itruediv__(self, other: float) -> Vector:
        self.__values = [x / other for x in self]

        return self

    def insert(self, index: int, value: float) -> None:
        self.__values.insert(index, value)


class Matrix(MutableSequence[Vector]):
    def __init__(self, it: Iterable[Iterable[float]] = (())):
        self.__values = list(map(Vector, it))

    @overload
    def __getitem__(self, i: int) -> Vector:
        ...

    @overload
    def __getitem__(self, s: slice) -> Matrix:
        ...

    def __getitem__(self, i: Union[int, slice]) -> Union[Vector, Matrix]:
        return self.__values[i] if isinstance(i, int) else Matrix(self.__values[i])

    @overload
    def __setitem__(self, i: int, o: Iterable[float]) -> None:
        ...

    @overload
    def __setitem__(self, s: slice, o: Iterable[Iterable[float]]) -> None:
        ...

    def __setitem__(self, i: Union[int, slice], o: Union[Iterable[float], Iterable[Iterable[float]]]) -> None:
        if isinstance(i, int):
            self.__values[i] = Vector(cast(Iterable[float], o))
        elif isinstance(i, slice):
            self.__values[i] = map(Vector, cast(Iterable[Iterable[float]], o))
        else:
            raise TypeError('Unknown Type')

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

    def __pos__(self) -> Matrix:
        return Matrix(self)

    def __neg__(self) -> Matrix:
        return Matrix(-x for x in self)

    @const_len
    def __add__(self, other: Iterable[Iterable[float]]) -> Matrix:
        return Matrix(x + y for x, y in zip(self, other))

    @const_len
    def __sub__(self, other: Iterable[Iterable[float]]) -> Matrix:
        return Matrix(x - y for x, y in zip(self, other))

    def __mul__(self, other: Union[float, Iterable[Iterable[float]]]) -> Matrix:
        if isinstance(other, float):
            return Matrix(x * other for x in self)
        elif isinstance(other, Iterable):
            from math2.linalg import transposed

            return Matrix((row @ col for col in transposed(Matrix(other))) for row in self)
        else:
            return NotImplemented

    def __rmul__(self, other: float) -> Matrix:
        return self * other

    def __truediv__(self, other: float) -> Matrix:
        return Matrix(x / other for x in self)

    @const_len
    def __matmul__(self, other: Iterable[Iterable[float]]) -> float:
        return sum(x @ y for x, y in zip(self, other))

    @const_len
    def __iadd__(self, other: Iterable[Iterable[float]]) -> Matrix:
        self.__values = [x + y for x, y in zip(self, other)]

        return self

    @const_len
    def __isub__(self, other: Iterable[Iterable[float]]) -> Matrix:
        self.__values = [x - y for x, y in zip(self, other)]

        return self

    def __imul__(self, other: Union[float, Iterable[Iterable[float]]]) -> Matrix:
        if isinstance(other, float):
            self.__values = [x * other for x in self]
        elif isinstance(other, Iterable):
            from math2.linalg import transposed

            self.__values = list(map(Vector, ((row @ col for col in transposed(Matrix(other))) for row in self)))
        else:
            return NotImplemented

        return self

    def __itruediv__(self, other: float) -> Matrix:
        self.__values = [x / other for x in self]

        return self

    def insert(self, index: int, value: Iterable[float]) -> None:
        self.__values.insert(index, Vector(value))
