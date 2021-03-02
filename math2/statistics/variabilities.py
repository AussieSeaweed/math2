from collections import Iterable
from math import sqrt

from math2.statistics.averages import mean


def range_(values: Iterable[float]) -> float:
    """Calculates the range of the values.

    :param values: the values
    :return: the range
    """
    values = tuple(values)

    return max(values) - min(values)


def variance(values: Iterable[float]) -> float:
    """Calculates the variance of the values.

    :param values: the values
    :return: the variance
    """
    values = tuple(values)
    mean_value = mean(values)

    return sum((value - mean_value) ** 2 for value in values) / (len(values) - 1)


def standard_deviation(values: Iterable[float]) -> float:
    """Calculates the standard deviation of the values.

    :param values: the values
    :return: the standard deviation
    """
    return sqrt(variance(values))
