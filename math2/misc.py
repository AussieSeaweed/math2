from collections.abc import Iterator
from typing import Optional

from auxiliary import default

from math2.typing import Scalar


def arange(start: Scalar, stop: Optional[Scalar] = None, step: Optional[Scalar] = None) -> Iterator[Scalar]:
    """Generates a range of floating point values.

    :param start: The start value.
    :param stop: The stop value.
    :param step: The step value.
    :return: The iterator of range values.
    """
    if stop is None:
        yield from arange(0, start, step)
    elif step is None:
        yield from arange(start, stop, 1)
    else:
        while start < stop:
            yield start
            start += step


def linspace(start: Scalar, stop: Scalar, n: Scalar = 100) -> Iterator[Scalar]:
    """Generates an iterator of values from start to stop with length of n.

    :param start: The start value.
    :param stop: The stop value.
    :param n: The number of values, defaults to 100.
    :return: The linspace of arguments.
    """
    return arange(start, stop, (stop - start) / n)


def interpolate(x: Scalar, x0: Scalar, x1: Scalar, y0: Scalar, y1: Scalar) -> Scalar:
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
