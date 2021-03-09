from collections.abc import Callable

from math2.consts import EPS
from math2.misc import frange


def diff(f: Callable[[float], float], x: float, eps: float = EPS) -> float:
    """Perform numerical differentiation on the supplied function.

    :param f: The function to be differentiated.
    :param x: The point of differentiation.
    :param eps: The accuracy.
    :return: The derivative at the point.
    """
    return (f(x + eps) - f(x - eps)) / (2 * eps)


def newton(f: Callable[[float], float], x: float, eps: float = EPS) -> float:
    """Solves the root of the supplied function with the Newton's method.
.
    :param f: The function to solve.
    :param x: The initial guess.
    :param eps: The accuracy.
    :return: The root coordinate.
    """
    while eps < abs(y := f(x)):
        x -= y / diff(f, x, eps)
    else:
        return x


def euler(f: Callable[[float], float], xlo: float, xhi: float, n: float = 100) -> float:
    """Integrates the function between two given bounds with the Euler's method.

    :param f: The function to integrate.
    :param xlo: The lower bound.
    :param xhi: The upper bound.
    :param n: The number of evaluation points.
    :return: The numerical integral of the function.
    """
    dx = (xhi - xlo) / n

    return sum(dx * f(x) for x in frange(xlo, xhi, dx))
