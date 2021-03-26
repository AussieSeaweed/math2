from __future__ import annotations

from collections.abc import Hashable, Iterable, Sequence
from functools import partial
from itertools import starmap
from math import sqrt
from operator import add, mul, neg
from typing import Any, Final, TypeVar, Union, overload

from auxiliary import product

from math2.linear.exceptions import DimensionError


class Tensor(Sequence[float], Hashable):
    def __init__(self, values: Iterable[float], dimensions: Iterable[int]):
        self._values = tuple(values)
        self.dimensions: Final = tuple(dimensions)

        if len(self) != product(self.dimensions, 1):
            raise DimensionError('The dimensions do not fit the values')

    def __pos__(self: T) -> T:
        return self

    def __neg__(self: T) -> T:
        return type(self)(map(neg, self), self.dimensions)

    def __add__(self: T, other: Tensor) -> T:
        if not isinstance(other, Tensor):
            return NotImplemented
        elif self.dimensions == other.dimensions:
            return type(self)(starmap(add, zip(self, other)), self.dimensions)  # type: ignore
        else:
            raise DimensionError('Adding two tensors requires identical dimensions')

    def __sub__(self: T, other: Tensor) -> T:
        try:
            return self + -other
        except TypeError:
            return NotImplemented

    def __mul__(self: T, other: float) -> T:
        try:
            return type(self)(map(partial(mul, other), self), self.dimensions)
        except TypeError:
            return NotImplemented

    def __rmul__(self: T, other: float) -> T:
        return self * other

    def __truediv__(self: T, other: float) -> T:
        try:
            return self * (1 / other)
        except TypeError:
            return NotImplemented

    def __matmul__(self, other: Tensor) -> float:
        if not isinstance(other, Tensor):
            return NotImplemented
        elif self.dimensions == other.dimensions:
            return sum(x * y for x, y in zip(self, other))
        else:
            raise DimensionError('Calculating the dot product of two tensors requires identical dimensions')

    def __abs__(self) -> float:
        return sqrt(self @ self)

    @overload
    def __getitem__(self, i: int) -> float:
        ...

    @overload
    def __getitem__(self, s: slice) -> Sequence[float]:
        ...

    def __getitem__(self, i: Union[int, slice]) -> Union[float, Sequence[float]]:
        return self._values[i]

    def __len__(self) -> int:
        return len(self._values)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Tensor):
            return self.dimensions == other.dimensions and self._values == other._values
        else:
            return NotImplemented

    def __repr__(self) -> str:
        return f'Tensor({self._values}, {self.dimensions})'

    def __hash__(self) -> int:
        return hash(self.dimensions) ^ hash(self._values)


T = TypeVar('T', bound=Tensor)
