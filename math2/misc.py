from collections.abc import Iterable, Iterator
from functools import reduce
from itertools import chain
from operator import add, mul
from typing import Optional

from auxiliary import default

from math2.typing import _SLT, _T


def bind(value: _SLT, lower: _SLT, upper: _SLT) -> _SLT:
    """Binds the value by the given interval.

    :param value: The value to be bound.
    :param lower: The lower limit.
    :param upper: The upper limit.
    :return: The bound value.
    """
    if upper < lower:
        raise ValueError('Lower bound is greater than the upper bound')
    elif value < lower:
        return lower
    elif upper < value:
        return upper
    else:
        return value


def sum_(values: Iterable[_T], start: Optional[_T] = None) -> _T:
    """Calculates the sum of the elements in the iterable.

    :param values: The values to be summed.
    :param start: The optional start value.
    :return: The sum of the values.
    """
    try:
        return reduce(add, values if start is None else chain((start,), values))
    except TypeError:
        raise ValueError('Invalid iterable')


def prod(values: Iterable[_T], start: Optional[_T] = None) -> _T:
    """Calculates the product of the elements in the iterable.

    :param values: The values to be multiplied.
    :param start: The optional start value.
    :return: The product of the values.
    """
    try:
        return reduce(mul, values if start is None else chain((start,), values))
    except TypeError:
        raise ValueError('Invalid iterable')


def frange(start: float, stop: Optional[float] = None, step: Optional[float] = None) -> Iterator[float]:
    """Generates a range of floating point values.

    :param start: The start value.
    :param stop: The stop value.
    :param step: The step value.
    :return: The iterator of range values.
    """
    if stop is None:
        yield from frange(0, start, step)
    elif step is None:
        yield from frange(start, stop, 1)
    else:
        while start < stop:
            yield start
            start += step


def linspace(start: float, stop: float, n: int = 100) -> Iterator[float]:
    """Generates an iterator of values from start to stop with length of n.

    :param start: The start value.
    :param stop: The stop value.
    :param n: The number of values.
    :return: The linspace of arguments.
    """
    return frange(start, stop, (stop - start) / n)


def interp(x: float, x0: float, x1: float, y0: float, y1: float) -> float:
    """Interpolates the point between two given points.

    :param x: The point to interpolate.
    :param x0: The x coordinate of the first point.
    :param x1: The x coordinate of the second point.
    :param y0: The y coordinate of the first point.
    :param y1: The y coordinate of the second point.
    :return: The interpolated value.
    """
    return (x - x0) / (x1 - x0) * (y1 - y0) + y0


def series_sum(lo: int, hi: Optional[int] = None, n: Optional[int] = None) -> int:
    """Calculates the series sum of the interval.

    :param lo: The start or end value.
    :param hi: The optional end value.
    :param n: The number of elements, defaults to (end - start) + 1.
    :return: the series sum.
    """
    return (lo + default(hi, 0)) * default(n, abs(default(hi, 0) - lo) + 1) // 2
