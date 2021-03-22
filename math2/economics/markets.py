import numpy as np

from math2.economics import EfInt


def fair(bull, bear, m_price, m_bull, m_bear, rf):
    """Calculates the fair price of an asset, given its potential payoffs.

    :param bull: The asset price in a bull market.
    :param bear: The asset price in a bear market.
    :param m_price: the price of market investment.
    :param m_bull: The market investment price in a bull market.
    :param m_bear: The market investment price in a bear market.
    :param rf: The risk free rate.
    :return: The fair price of an asset.
    """
    a, b = np.linalg.solve(((m_bull, rf.to_factor()), (m_bear, rf.to_factor())), (bull, bear))

    return m_price * a + b


def ror(price, bull, bear, p):
    """Calculates the expected rate of return of an asset.

    :param price: The price of an asset.
    :param bull: The asset price in a bullish market.
    :param bear: The asset price in a bearish market.
    :param p: The percentage of a bull market.
    :return: The expected rate of return.
    """
    return EfInt((bull * p + bear * (1 - p)) / price - 1)


def beta(a_ror, m_ror, rf):
    """Calculates the asset risk.

    :param a_ror: The rate of return of an asset.
    :param m_ror: The market rate of return.
    :param rf: The risk free rate.
    :return:
    """
    return (a_ror.to_ef().rate - rf.to_ef().rate) / (m_ror.to_ef().rate - rf.to_ef().rate)


def capm(b, rf, em):
    """Calculates the expected return using the CAPM model.

    :param b: The company risk.
    :param rf: The risk-free rate.
    :param em: The expected market return rate.
    :return: The expected return.
    """
    return EfInt(rf.to_ef().rate + b * (em.to_ef().rate - rf.to_ef().rate))
