from collections.abc import Collection, Iterable, Iterator
from math import sqrt

from auxiliary import sum_, trimmed

from math2.typing import _S


def mean(values: Iterable[_S]) -> _S:
    """Calculates the mean of the values.

    :param values: The values.
    :return: The mean.
    """
    return sum_(values) / len(values) if isinstance(values, Collection) else mean(tuple(values))  # type: ignore


def median(values: Iterable[_S]) -> _S:
    """Calculates the median of the values.

    :param values: The values.
    :return: The median.
    """
    values = sorted(values)

    if len(values) % 2:
        return values[len(values) // 2]
    else:
        return (values[len(values) // 2 - 1] + values[len(values) // 2]) / 2


def interquartile_range(values: Iterable[_S]) -> _S:
    """Calculates the interquartile range of the values.

    :param values: The values.
    :return: The interquartile range.
    """
    values = sorted(values)

    return values[3 * len(values) // 4] - values[len(values) // 4]


def trimmed_mean(values: Iterable[_S], percentage: float) -> _S:
    """Calculates the trimmed mean of the values.

    :param values: The values.
    :param percentage: The trimmed percentage.
    :return: The trimmed mean.
    """
    return mean(trimmed(sorted(values), percentage))


def range_(values: Iterable[_S]) -> _S:
    """Calculates the range of the values.

    :param values: The values.
    :return: The range of the values.
    """
    return range_(tuple(values)) if isinstance(values, Iterator) else max(values) - min(values)  # type: ignore


def variance(values: Iterable[_S]) -> _S:
    """Calculates the variance of the values.

    :param values: The values.
    :return: The variance of the values.
    """
    if isinstance(values, Collection):
        mu = mean(values)

        return sum_((x - mu) ** 2 for x in values) / (len(values) - 1)  # type: ignore
    else:
        return variance(tuple(values))


def standard_deviation(values: Iterable[_S]) -> _S:
    """Calculates the standard deviation of the values.

    :param values: The values.
    :return: The variance of the values.
    """
    return sqrt(variance(values))  # type: ignore
