from collections import Iterable, Iterator, Sequence
from functools import reduce
from itertools import chain
from operator import lt, mul
from typing import Optional, TypeVar

T = TypeVar('T')


def trim(values: Iterable[T], percentage: float) -> Sequence[T]:
    """Trims the iterable by the percentage.

    :param values: the values
    :param percentage: the trimmed percentage
    :return: the trimmed sequence
    """
    values = tuple(values)
    n = int(len(values) * percentage)

    return values[n:len(values) - n]


def window(values: Iterable[T], width: int) -> Iterator[Sequence[T]]:
    """Returns the sliding window views of the supplied iterable

    :param values: the values
    :param width: the sliding window width
    :return: the window views
    """
    values = tuple(values)

    return (values[i:i + width] for i in range(len(values) - width + 1))


def rotate(values: Iterable[T], index: int) -> Iterator[T]:
    """Rotates the iterable by the given index.

    :param values: the values
    :param index: the index of rotation
    :return: the rotated iterable
    """
    values = tuple(values)

    return chain(values[index:], values[:index])


def constant(values: Iterable[T]) -> bool:
    """Checks if all elements inside the iterable are equal to each other.

       If the iterable is empty, True is returned.

    :param values: the values
    :return: True if all elements are equal, else False
    """
    values = tuple(values)

    return not values or all(v == values[0] for v in values)


def chunk(values: Iterable[T], width: int) -> Iterator[Sequence[T]]:
    """Chunks the iterable by the given width.

    :param values: the values
    :param width: the chunk width
    :return: the chunks
    """
    values = tuple(values)

    return (values[i:i + width] for i in range(0, len(values), width))


def iter_equal(it1: Iterable[T], it2: Iterable[T]) -> bool:
    """Checks if all elements in both iterables are equal to the elements in the other iterable at the same position.

    :param it1: the first iterable
    :param it2: the second iterable
    :return: True if the equality check passes, else False
    """
    it1, it2 = tuple(it1), tuple(it2)

    return len(it1) == len(it2) and all(x == y for x, y in zip(it1, it2))


def product(values: Iterable[T]) -> T:
    """Calculates the product of the elements in the iterable.

    :param values: the values
    :return: the product
    """
    try:
        return reduce(mul, values)
    except TypeError:
        raise ValueError('Invalid iterable')


def limit(value: T, lower: T, upper: T) -> T:
    """Binds the value by the given interval.

    :param value: the value
    :param lower: the lower limit
    :param upper: the upper limit
    :return: the bound value
    """
    if lt(upper, lower):
        raise ValueError('Lower bound is greater than the upper bound')

    if lt(value, lower):
        return lower
    elif lt(upper, value):
        return upper
    else:
        return value


def next_or_none(it: Iterator[T]) -> Optional[T]:
    """Tries to get the next element of the iterator.

    :param it: the iterator to consume
    :return: None if there is no next element, else the next element
    """
    try:
        return next(it)
    except StopIteration:
        return None


def default(optional: Optional[T], default_: T) -> T:
    """Checks if the value is not None and returns it or the default value.

    :param optional: the optional value
    :param default_: the default value
    :return: the default value if the value to check is None, else the checked value
    """
    return default_ if optional is None else optional


def get(optional: Optional[T]) -> T:
    """Checks if the optional value is not none and returns it.

    :param optional: the optional value
    :return: the checked value
    """
    if optional is None:
        raise TypeError('The checked value is None')
    else:
        return optional
