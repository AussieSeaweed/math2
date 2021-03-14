from collections.abc import Iterator
from typing import Optional

from math2.utils import default


def arange(start: float, stop: Optional[float] = None, step: Optional[float] = None) -> Iterator[float]:
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


def linspace(start: float, stop: float, n: float = 100) -> Iterator[float]:
    """Generates an iterator of values from start to stop with length of n.

    :param start: The start value.
    :param stop: The stop value.
    :param n: The number of values, defaults to 100.
    :return: The linspace of arguments.
    """
    return arange(start, stop, (stop - start) / n)


def series_sum(lo: int, hi: Optional[int] = None, n: Optional[int] = None) -> int:
    """Calculates the series sum of the interval.

    :param lo: The start or end value.
    :param hi: The optional end value.
    :param n: The number of elements, defaults to (end - start) + 1.
    :return: the series sum.
    """
    return (lo + default(hi, 0)) * default(n, abs(default(hi, 0) - lo) + 1) // 2
