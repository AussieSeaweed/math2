from math2.econ import CompInt


def capm(r: CompInt, b: float, e: float) -> float:
    """Calculates the expected return using the CAPM model.

    :param r: The risk-free rate.
    :param b: The company risk.
    :param e: The expected market return.
    :return: The expected return.
    """
    return r.to_ef().rate + b * (e - r.to_ef().rate)
