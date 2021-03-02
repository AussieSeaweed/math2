from collections import Iterable, Iterator, Sequence
from functools import reduce
from itertools import chain
from operator import add, lt, mul
from typing import Optional, TypeVar

T = TypeVar('T')


def trim(it: Iterable[T], percentage: float) -> Sequence[T]:
    """Trims the iterable by the percentage.

    :param it: the iterable to be trimmed
    :param percentage: the percentage to trim
    :return: the trimmed sequence
    """
    if isinstance(it, Sequence):
        n = int(len(it) * percentage)

        return it[n:len(it) - n]
    else:
        return trim(tuple(it), percentage)


def window(it: Iterable[T], n: int) -> Iterator[Sequence[T]]:
    """Returns the sliding window views of the supplied iterable

    :param it: the iterable to be operated on
    :param n: the width of the sliding window
    :return: the window views
    """
    if isinstance(it, Sequence):
        return (it[i:i + n] for i in range(len(it) - n + 1))
    else:
        return window(tuple(it), n)


def rotate(it: Iterable[T], i: int) -> Iterator[T]:
    """Rotates the iterable by the given index.

    :param it: the iterable to rotate
    :param i: the index of rotation
    :return: the rotated iterable
    """
    if isinstance(it, Sequence):
        return chain(it[i:], it[:i])
    else:
        return rotate(tuple(it), i)


def constant(it: Iterable[T]) -> bool:
    """Checks if all elements inside the iterable are equal to each other.

    If the iterable is empty, True is returned.

    :param it: the iterable
    :return: True if all elements are equal, else False
    """
    if isinstance(it, Sequence):
        return not it or all(x == it[0] for x in it)
    else:
        return constant(tuple(it))


def chunk(it: Iterable[T], n: int) -> Iterator[Sequence[T]]:
    """Chunks the iterable by the given length.

    :param it: the iterable to chunk
    :param n: the chunk length
    :return: the rotated iterable
    """
    if isinstance(it, Sequence):
        return (it[i:i + n] for i in range(0, len(it), n))
    else:
        return chunk(tuple(it), n)


def iter_equal(it1: Iterable[T], it2: Iterable[T]) -> bool:
    """Checks if all elements in both iterables are equal to the elements in the other iterable at the same position.

    :param it1: the first iterable
    :param it2: the second iterable
    :return: True if the equality check passes, else False
    """
    if isinstance(it1, Sequence) and isinstance(it2, Sequence):
        return len(it1) == len(it2) and all(x == y for x, y in zip(it1, it2))
    else:
        return iter_equal(tuple(it1), tuple(it2))


def sum_(it: Iterable[T]) -> T:
    """Calculates the sum of the elements in the iterable.

    :param it: the iterable
    :return: the sum of the elements
    """
    try:
        return reduce(add, it)
    except TypeError:
        raise ValueError('Invalid iterable')


def product(it: Iterable[T]) -> T:
    """Calculates the product of the elements in the iterable.

    :param it: the iterable
    :return: the product of the elements
    """
    try:
        return reduce(mul, it)
    except TypeError:
        raise ValueError('Invalid iterable')


def limit(v: T, lower: T, upper: T) -> T:
    """Binds the value by the given interval.

    :param v: the value to bind
    :param lower: the lower limit
    :param upper: the upper limit
    :return: the bound value
    """
    if lt(upper, lower):
        raise ValueError('Lower bound is greater than the upper bound')

    if lt(v, lower):
        return lower
    elif lt(upper, v):
        return upper
    else:
        return v


def next_or_none(it: Iterator[T]) -> Optional[T]:
    """Tries to get the next element of the iterator.

    :param it: the iterable to consume
    :return: None if there is no next element, else the next element
    """
    try:
        return next(it)
    except StopIteration:
        return None


def default(t: Optional[T], d: T) -> T:
    """Checks if the value is not None and returns it or the default value.

    :param t: the value to check
    :param d: the default value
    :return: the default value if the value to check is None, else the checked value
    """
    return d if t is None else t


def get(t: Optional[T]) -> T:
    """Checks if the value is not none and returns it.

    :param t: the value to check
    :return: the checked value
    """
    if t is None:
        raise TypeError('The checked value is None')
    else:
        return t
