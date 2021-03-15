def af(i, n):
    """Calculates the sinking fund factor.

    :param i: The interest rate.
    :param n: The number of periods.
    :return: The calculated factor.
    """
    return i / ((1 + i) ** n - 1)


def ag(i, n):
    """Calculates the arithmetic gradient to annuity conversion factor.

    :param i: The interest rate.
    :param n: The number of periods.
    :return: The calculated factor.
    """
    return 1 / i - n / ((1 + i) ** n - 1)


def ap(i, n):
    """Calculates the capital recovery factor.

    :param i: The interest rate.
    :param n: The number of periods.
    :return: The calculated factor.
    """
    return i * (1 + i) ** n / ((1 + i) ** n - 1)


def fa(i, n):
    """Calculates the uniform series compound amount factor.

    :param i: The interest rate.
    :param n: The number of periods.
    :return: The calculated factor.
    """
    return ((1 + i) ** n - 1) / i


def fp(i, n):
    """Calculates the compound amount factor.

    :param i: The interest rate.
    :param n: The number of periods.
    :return: The calculated factor.
    """
    return (1 + i) ** n


def pa(i, n, g=None):
    """If the geometric gradient rate is supplied, calculates the geometric gradient to present worth conversion factor.
       Otherwise, calculates the series present worth factor.

    :param i: The interest rate.
    :param n: The number of periods.
    :param g: The optional geometric gradient rate.
    :return: The calculated factor.
    """
    if g is None:
        return ((1 + i) ** n - 1) / (i * (1 + i) ** n)
    else:
        return pa((1 + i) / (1 + g) - 1, n) / (1 + g)


def pf(i, n):
    """Calculates the present worth factor.

    :param i: The interest rate.
    :param n: The number of periods.
    :return: The calculated factor.
    """
    return (1 + i) ** -n


def pg(i, n):
    """Calculates the arithmetic gradient to present worth factor.

    :param i: The interest rate.
    :param n: The number of periods.
    :return: The calculated factor.
    """
    return 1 / i ** 2 * (1 - (1 + i * n) / (1 + i) ** n)


def perp(i):
    """Calculates the perpetuity to present worth factor.

    :param i: The interest rate.
    :return: The calculated factor.
    """
    return 1 / i
