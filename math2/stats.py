from collections.abc import Iterable, Iterator, Sequence
from itertools import chain, repeat
from random import shuffle
from statistics import fmean

from auxiliary import ilen, retain_iter, trimmed

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


@retain_iter
def sampled(pop: Iterable[_T], n: int) -> Iterator[_T]:
    """Samples n values.

    :param pop: The population.
    :param n: The sample count.
    :return: The samples.
    """
    picks = shuffled(chain(repeat(True, n), repeat(False, ilen(pop) - n)))

    return (x for i, x in enumerate(pop) if picks[i])
