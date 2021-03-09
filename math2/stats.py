from collections.abc import Iterable, Sequence
from random import shuffle
from statistics import fmean

from auxiliary import retain_iter, trimmed

from math2.types import _T


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


def shuffled(values: Iterable[_T]) -> Sequence[_T]:
    """Shuffles the copied values and returns the list.

    :param values: The values.
    :return: The shuffled sequence.
    """
    values = list(values)
    shuffle(values)
    return values
