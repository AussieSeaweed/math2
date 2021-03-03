from collections import Iterable
from math import sqrt

from auxiliary import ilen, retain_iter

from math2.stats.averages import mean


@retain_iter
def range_(values: Iterable[float]) -> float:
    """Calculates the range of the values.

    :param values: The values.
    :return: The range.
    """
    return max(values) - min(values)


@retain_iter
def variance(values: Iterable[float]) -> float:
    """Calculates the variance of the values.

    :param values: The values.
    :return: The variance.
    """
    mean_value = mean(values)

    return sum((value - mean_value) ** 2 for value in values) / (ilen(values) - 1)


def standard_deviation(values: Iterable[float]) -> float:
    """Calculates the standard deviation of the values.

    :param values: The values.
    :return: The standard deviation.
    """
    return sqrt(variance(values))
