from collections import Callable


def derivative(func: Callable[[float], float], x: float, eps: float = 1e-8) -> float:
    """Perform numerical differentiation on the supplied function.

    :param func: The function to be differentiated
    :param x: The point of differentiation
    :param eps: The accuracy
    :return: The derivative at the point
    """
    return (func(x + eps) - func(x - eps)) / (2 * eps)


def newton(func: Callable[[float], float], x: float, eps: float = 1e-8) -> float:
    """Solves the root of the supplied function with Newton's method.

    :param func: The function to solve
    :param x: The initial argument
    :param eps: The accuracy
    :return: The root coordinate
    """
    while eps < abs(y := func(x)):
        x -= y / derivative(func, x)
    else:
        return x
