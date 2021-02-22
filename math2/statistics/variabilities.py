from collections import Collection
from math import sqrt

from math2.statistics.averages import mean


def range_(values: Collection[float]) -> float:
    """Calculates the range of the values.

    :param values: the collection of values
    :return: the range of the values
    """
    return max(values) - min(values)


def variance(values: Collection[float]) -> float:
    """Calculates the variance of the values.

    :param values: the collection of values
    :return: the variance of the values
    """
    mean_value = mean(values)

    return sum((value - mean_value) ** 2 for value in values) / (len(values) - 1)


def standard_deviation(values: Collection[float]) -> float:
    """Calculates the standard deviation of the values.

    :param values: the collection of values
    :return: the standard deviation of the values
    """
    return sqrt(variance(values))
