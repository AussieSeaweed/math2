from collections.abc import Callable

from math2.consts import EPS
from math2.misc import arange


def derivative(f: Callable[[float], float], x: float) -> float:
    """Performs a numerical differentiation on the supplied function.

    :param f: The function to be differentiated.
    :param x: The coordinate where the differentiation take place.
    :return: The derivative at the point.
    """
    return (f(x + EPS) - f(x - EPS)) / (2 * EPS)


def root(f: Callable[[float], float], x: float) -> float:
    """Solves the root of the supplied function with the Newton's method.

    :param f: The function to solve.
    :param x: The initial guess.
    :return: The root's coordinate.
    """
    while EPS < abs(y := f(x)):
        x -= y / derivative(f, x)
    else:
        return x


def integrate(f: Callable[[float], float], xlo: float, xhi: float, n: float = 100) -> float:
    """Performs a numerical integration on the supplied function between the given bounds with the Euler's method.

    :param f: The function to integrate.
    :param xlo: The lower bound.
    :param xhi: The upper bound.
    :param n: The number of evaluation points.
    :return: The numerical integral of the function.
    """
    dx = (xhi - xlo) / n

    return sum(dx * f(x) for x in arange(xlo, xhi, dx))
