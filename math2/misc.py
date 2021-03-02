from collections import Iterable, Iterator
from functools import reduce
from operator import mul
from typing import Optional, TypeVar

from math2.utils import SupportsLessThan, SupportsMul

_SLT = TypeVar('_SLT', bound=SupportsLessThan)


def limit(value: _SLT, lower: _SLT, upper: _SLT) -> _SLT:
    """Binds the value by the given interval.

    :param value: The value
    :param lower: The lower limit
    :param upper: The upper limit
    :return: The bound value
    """
    if upper < lower:
        raise ValueError('Lower bound is greater than the upper bound')

    if value < lower:
        return lower
    elif upper < value:
        return upper
    else:
        return value


_SM = TypeVar('_SM', bound=SupportsMul)


def product(values: Iterable[_SM]) -> _SM:
    """Calculates the product of the elements in the iterable.

    :param values: The values
    :return: The product
    """
    try:
        return reduce(mul, values)
    except TypeError:
        raise ValueError('Invalid iterable')


def frange(start: float, stop: Optional[float] = None, step: Optional[float] = None) -> Iterator[float]:
    """Generates a range of floating point values.

    :param start: The start value
    :param stop: The stop value
    :param step: The step value
    :return: The iterator of range values
    """
    if stop is None:
        yield from frange(0, start, step)
    elif step is None:
        yield from frange(start, stop, 1)
    else:
        while start < stop:
            yield start
            start += step
