from collections.abc import Callable

from math2.misc import frange


def derivative(func: Callable[[float], float], x: float, eps: float = 1e-7) -> float:
    """Perform numerical differentiation on the supplied function.

    :param func: The function to be differentiated.
    :param x: The point of differentiation.
    :param eps: The accuracy.
    :return: The derivative at the point.
    """
    return (func(x + eps) - func(x - eps)) / (2 * eps)


def newton(func: Callable[[float], float], x: float, eps: float = 1e-7) -> float:
    """Solves the root of the supplied function with the Newton's method.
.
    :param func: The function to solve.
    :param x: The initial guess.
    :param eps: The accuracy.
    :return: The root coordinate.
    """
    while eps < abs(y := func(x)):
        x -= y / derivative(func, x, eps)
    else:
        return x


def euler(func: Callable[[float], float], xlo: float, xhi: float, n: float = 100) -> float:
    """Integrates the function between two given bounds with the Euler's method.

    :param func: The function to integrate.
    :param xlo: The lower bound.
    :param xhi: The upper bound.
    :param n: The number of evaluation points.
    :return: The numerical integral of the function.
    """
    dx = (xhi - xlo) / n

    return sum(dx * func(x) for x in frange(xlo, xhi, dx))
