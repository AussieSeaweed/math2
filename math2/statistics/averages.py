from collections import Collection

from auxiliary.utils import trim


def mean(values: Collection[float]) -> float:
    """Calculates the mean of the values.

    :param values: the collection of values
    :return: the mean of the values
    """
    return sum(values) / len(values)


def trimmed_mean(values: Collection[float], percentage: float) -> float:
    """Calculates the trimmed mean of the values.

    :param values: the collection of values
    :param percentage: the percentage value
    :return: the trimmed mean of the values
    """
    return mean(trim(sorted(values), percentage))


def median(values: Collection[float]) -> float:
    """Calculates the median of the values.

    :param values: the collection of values
    :return: the median of the values
    """
    values = sorted(values)

    if len(values) % 2:
        return values[len(values) // 2]
    else:
        return (values[len(values) // 2 - 1] + values[len(values) // 2]) / 2
