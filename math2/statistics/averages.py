from collections import Iterable

from math2.utils import trim


def mean(values: Iterable[float]) -> float:
    """Calculates the mean of the values.

    :param values: the values
    :return: the mean
    """
    values = tuple(values)

    return sum(values) / len(values)


def trimmed_mean(values: Iterable[float], percentage: float) -> float:
    """Calculates the trimmed mean of the values.

    :param values: the values
    :param percentage: the percentage value
    :return: the trimmed mean
    """
    return mean(trim(sorted(values), percentage))


def median(values: Iterable[float]) -> float:
    """Calculates the median of the values.

    :param values: the values
    :return: the median
    """
    values = sorted(values)

    if len(values) % 2:
        return values[len(values) // 2]
    else:
        return (values[len(values) // 2 - 1] + values[len(values) // 2]) / 2
