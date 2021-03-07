from collections.abc import Iterable

from auxiliary import ilen, retain_iter, trim


@retain_iter
def mean(values: Iterable[float]) -> float:
    """Calculates the mean of the values.

    :param values: The values.
    :return: The mean.
    """
    return sum(values) / ilen(values)


def trimmed_mean(values: Iterable[float], percentage: float) -> float:
    """Calculates the trimmed mean of the values.

    :param values: The values.
    :param percentage: The percentage value.
    :return: The trimmed mean.
    """
    return mean(trim(sorted(values), percentage))


def median(values: Iterable[float]) -> float:
    """Calculates the median of the values.

    :param values: The values.
    :return: The median.
    """
    if len(values := sorted(values)) % 2:
        return values[len(values) // 2]
    else:
        return (values[len(values) // 2 - 1] + values[len(values) // 2]) / 2
