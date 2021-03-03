from collections import Iterable, Iterator, Sized
from itertools import chain, islice
from typing import Any, Optional, cast

from math2.utils.types import _F, _T


def const_len(func: _F) -> _F:
    """Decorates a function to make sure all sized arguments are of the same length.

    :param func: The function to decorate.
    :return: The decorated function.
    """

    def checked_func(*args: Any, **kwargs: Any) -> Any:
        if const(len(arg) for arg in chain(args, kwargs.values()) if isinstance(arg, Sized)):
            return func(*args, **kwargs)
        else:
            raise ValueError('Collection arguments are not of constant length')

    return cast(_F, checked_func)


def retain_iter(func: _F) -> _F:
    """Decorates a function to make sure all iterators are converted to sequences to persist after iterations.

    :param func: The function to decorate.
    :return: The decorated function.
    """

    def retained_func(*args: Any, **kwargs: Any) -> Any:
        args = tuple(tuple(arg) if isinstance(arg, Iterator) else arg for arg in args)
        kwargs = {key: value if isinstance(value, Iterator) else tuple(value) for key, value in kwargs.items()}

        return func(*args, **kwargs)

    return cast(_F, retained_func)


def ilen(it: Iterable[Any]) -> int:
    """Gets the length of the given iterator.

    :param it: The iterator.
    :return: The length of the iterator.
    """
    return len(it) if isinstance(it, Sized) else len(tuple(it))


@retain_iter
def chunk(values: Iterable[_T], width: int) -> Iterator[Iterator[_T]]:
    """Chunks the iterable by the given width.

    :param values: The values to chunk.
    :param width: The chunk width.
    :return: The chunks.
    """
    return (islice(values, i, i + width) for i in range(0, ilen(values), width))


@retain_iter
def window(values: Iterable[_T], width: int) -> Iterator[Iterator[_T]]:
    """Returns the sliding window views of the supplied iterable.

    :param values: The values to generate the views on.
    :param width: The sliding window width.
    :return: The window views.
    """
    return (islice(values, i, i + width) for i in range(ilen(values) - width + 1))


@retain_iter
def trim(values: Iterable[_T], percentage: float) -> Iterator[_T]:
    """Trims the iterable by the percentage.

    :param values: The values to trim.
    :param percentage: The trimmed percentage.
    :return: The trimmed sequence.
    """
    n = int(ilen(values) * percentage)

    return islice(values, n, ilen(values) - n)


@retain_iter
def rotate(values: Iterable[_T], index: int) -> Iterator[_T]:
    """Rotates the iterable by the given index.

    :param values: The values to rotate.
    :param index: The index of rotation.
    :return: The rotated iterator.
    """
    return chain(islice(values, index % ilen(values), None), islice(values, index % ilen(values)))


@retain_iter
def iter_equal(it1: Iterable[_T], it2: Iterable[_T]) -> bool:
    """Checks if all elements in both iterables are equal to the elements in the other iterable at the same position.

    :param it1: The first iterable.
    :param it2: The second iterable.
    :return: True if the equality check passes, else False.
    """
    return ilen(it1) == ilen(it2) and all(x == y for x, y in zip(it1, it2))


def const(values: Iterable[_T]) -> bool:
    """Checks if all elements inside the iterable are equal to each other.

       If the iterable is empty, True is returned.

    :param values: The values.
    :return: True if all elements are equal, else False.
    """
    return all(x == y for x, y in window(values, 2))


def next_or_none(it: Iterator[_T]) -> Optional[_T]:
    """Tries to get the next element of the iterator.

    :param it: The iterator to consume.
    :return: None if there is no next element, else the next element.
    """
    try:
        return next(it)
    except StopIteration:
        return None


def default(optional: Optional[_T], default_: _T) -> _T:
    """Checks if the value is not None and returns it or the default value.

    :param optional: The optional value.
    :param default_: The default value.
    :return: The default value if the value to check is None, else the checked value.
    """
    return default_ if optional is None else optional


def get(optional: Optional[_T]) -> _T:
    """Checks if the optional value is not none and returns it.

    :param optional: The optional value.
    :return: The checked value.
    """
    if optional is None:
        raise ValueError('The checked value is None')
    else:
        return optional
