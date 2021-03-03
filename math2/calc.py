from collections import Callable


def derivative(func: Callable[[float], float], x: float, dx: float = 1) -> float:
    """Perform numerical differentiation on the supplied function.

    :param func: The function to be differentiated
    :param x: The point of differentiation
    :param dx: The accuracy
    :return: The derivative at the point
    """
    return (func(x + dx) - func(x - dx)) / (2 * dx)


def newton(func: Callable[[float], float], x: float, dx: float = 1) -> float:
    ...
