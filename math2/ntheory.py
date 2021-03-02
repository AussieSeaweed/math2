def gcd(x: float, y: float) -> float:
    """Calculates the greatest common denominator of the pair of numbers using the euclidean algorithm.

    :param x: The first number
    :param y: The second number
    :return: The greatest common denominator
    """
    return gcd(y, x % y) if y else x


def lcm(x: float, y: float) -> float:
    """Calculates the least common multiple of the pair of numbers using the euclidean algorithm.

    :param x: The first number
    :param y: The second number
    :return: The least common multiple
    """
    return x * y / gcd(x, y)
