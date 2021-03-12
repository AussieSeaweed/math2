from collections.abc import Iterable, Iterator, Sequence
from random import shuffle
from statistics import fmean

from auxiliary import trimmed

from math2.typing import Scalar, _T


def trimmed_mean(values: Iterable[Scalar], percentage: Scalar) -> Scalar:
    """Calculates the trimmed mean of the values.

    :param values: The values.
    :param percentage: The trimmed percentage.
    :return: The trimmed mean.
    """
    return fmean(trimmed(sorted(values), percentage))


def range_(values: Iterable[Scalar]) -> Scalar:
    """Calculates the range of the values.

    :param values: The values.
    :return: The range of the values.
    """
    return range_(tuple(values)) if isinstance(values, Iterator) else max(values) - min(values)


def shuffled(values: Iterable[_T]) -> Sequence[_T]:
    """Shuffles the copied values and returns the list.

    :param values: The values to be shuffled.
    :return: The shuffled sequence.
    """
    values = list(values)

    shuffle(values)

    return values