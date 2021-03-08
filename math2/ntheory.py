from typing import Union, overload


@overload
def gcd(x: int, y: int) -> int: ...


@overload
def gcd(x: float, y: float) -> float: ...


def gcd(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    """Calculates the greatest common denominator of the pair of numbers using the euclidean algorithm.

    :param x: The first number.
    :param y: The second number.
    :return: The greatest common denominator.
    """
    return gcd(y, x % y) if y else x


@overload
def lcm(x: int, y: int) -> int: ...


@overload
def lcm(x: float, y: float) -> float: ...


def lcm(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    """Calculates the least common multiple of the pair of numbers using the euclidean algorithm.

    :param x: The first number.
    :param y: The second number.
    :return: The least common multiple.
    """
    if isinstance(x, int) and isinstance(y, int):
        return x * y // gcd(x, y)
    else:
        return x * y / gcd(x, y)
