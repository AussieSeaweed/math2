from collections.abc import Iterable
from statistics import fmean

from auxiliary import retain_iter, trimmed


def trimmed_mean(values: Iterable[float], percentage: float) -> float:
    """Calculates the trimmed mean of the values.

    :param values: The values.
    :param percentage: The percentage value.
    :return: The trimmed mean.
    """
    return fmean(trimmed(sorted(values), percentage))


@retain_iter
def range_(values: Iterable[float]) -> float:
    """Calculates the range of the values.

    :param values: The values.
    :return: The range.
    """
    return max(values) - min(values)
