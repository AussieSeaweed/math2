from collections import Iterable
from math import sqrt

from math2.stats.averages import mean
from math2.utils import retain_iter


@retain_iter
def range_(values: Iterable[float]) -> float:
    """Calculates the range of the values.

    :param values: The values.
    :return: The range.
    """
    return max(values) - min(values)


def variance(values: Iterable[float]) -> float:
    """Calculates the variance of the values.

    :param values: The values.
    :return: The variance.
    """
    values = tuple(values)
    mean_value = mean(values)

    return sum((value - mean_value) ** 2 for value in values) / (len(values) - 1)


def standard_deviation(values: Iterable[float]) -> float:
    """Calculates the standard deviation of the values.

    :param values: The values.
    :return: The standard deviation.
    """
    return sqrt(variance(values))