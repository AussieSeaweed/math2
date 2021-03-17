from collections.abc import Collection, Iterator
from math import sqrt

from auxiliary import sum_, trimmed


def mean(values):
    """Calculates the mean of the values.

    :param values: The values.
    :return: The mean.
    """
    return sum_(values) / len(values) if isinstance(values, Collection) else mean(tuple(values))


def median(values):
    """Calculates the median of the values.

    :param values: The values.
    :return: The median.
    """
    values = sorted(values)

    if len(values) % 2:
        return values[len(values) // 2]
    else:
        return (values[len(values) // 2 - 1] + values[len(values) // 2]) / 2


def trimmed_mean(values, percentage):
    """Calculates the trimmed mean of the values.

    :param values: The values.
    :param percentage: The trimmed percentage.
    :return: The trimmed mean.
    """
    return mean(tuple(trimmed(sorted(values), percentage)))


def range_(values):
    """Calculates the range of the values.

    :param values: The values.
    :return: The range of the values.
    """
    return range_(tuple(values)) if isinstance(values, Iterator) else max(values) - min(values)


def variance(values):
    """Calculates the variance of the values.

    :param values: The values.
    :return: The variance of the values.
    """
    if isinstance(values, Collection):
        mu = mean(values)

        return sum_((x - mu) ** 2 for x in values) / (len(values) - 1)
    else:
        return variance(tuple(values))


def standard_deviation(values):
    """Calculates the standard deviation of the values.

    :param values: The values.
    :return: The variance of the values.
    """
    return sqrt(variance(values))
