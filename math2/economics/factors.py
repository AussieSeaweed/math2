from typing import Optional


def af(i: float, n: float) -> float:
    """Calculates the sinking fund factor.

    :param i: the interest rate
    :param n: the number of periods
    :return: the calculated factor
    """
    return i / ((1 + i) ** n - 1)


def ag(i: float, n: float) -> float:
    """Calculates the arithmetic gradient to annuity conversion factor.

    :param i: the interest rate
    :param n: the number of periods
    :return: the calculated factor
    """
    return 1 / i - n / ((1 + i) ** n - 1)


def ap(i: float, n: float) -> float:
    """Calculates the capital recovery factor.

    :param i: the interest rate
    :param n: the number of periods
    :return: the calculated factor
    """
    return i * (1 + i) ** n / ((1 + i) ** n - 1)


def fa(i: float, n: float) -> float:
    """Calculates the uniform series compound amount factor.

    :param i: the interest rate
    :param n: the number of periods
    :return: the calculated factor
    """
    return ((1 + i) ** n - 1) / i


def fp(i: float, n: float) -> float:
    """Calculates the compound amount factor.

    :param i: the interest rate
    :param n: the number of periods
    :return: the calculated factor
    """
    return (1 + i) ** n


def pa(i: float, n: float, g: Optional[float] = None) -> float:
    """If the geometric gradient rate is supplied, calculates the geometric gradient to present worth conversion factor.
    Otherwise, calculates the series present worth factor.

    :param i: the interest rate
    :param n: the number of periods
    :param g: the optional geometric gradient rate
    :return: the calculated factor
    """
    if g is None:
        return ((1 + i) ** n - 1) / (i * (1 + i) ** n)
    else:
        return pa((1 + i) / (1 + g) - 1, n) / (1 + g)


def pf(i: float, n: float) -> float:
    """Calculates the present worth factor.

    :param i: the interest rate
    :param n: the number of periods
    :return: the calculated factor
    """
    return (1 + i) ** -n
