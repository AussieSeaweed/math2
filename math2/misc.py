from collections.abc import Iterator
from typing import Optional

from auxiliary import default


def series_sum(begin: int, end_inclusive: int, count: Optional[int] = None) -> int:
    """Calculates the series sum of the interval.

    :param begin: The beginning value of the series.
    :param end_inclusive: The inclusive final value in the series.
    :param count: The number of values in the series, defaults to end_inclusive - begin + 1.
    :return: the series sum.
    """
    return (begin + end_inclusive) * default(count, abs(end_inclusive - begin) + 1) // 2


def linspace(start: float, end: float, count: int) -> Iterator[float]:
    """Constructs an iterator of equally spaced values from start to end.

    :param start: The start value.
    :param end: The end value.
    :param count: The number of values.
    :return: The equally spaced values.
    """
    step = (end - start) / (count - 1)

    return (start + step * i for i in range(count))
