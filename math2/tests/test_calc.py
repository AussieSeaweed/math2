from math import cos, exp, log, sin
from unittest import main

from math2.calc import derivative, newton
from math2.utils import ExtendedTestCase


class CalcTestCase(ExtendedTestCase):
    def test_derivative(self) -> None:
        self.assertAlmostEqual(derivative(lambda x: x ** 3 - 2 * x ** 2, 3), 3 * 3 ** 2 - 4 * 3)
        self.assertAlmostEqual(derivative(lambda x: -3 * sin(2 * x), 5), -6 * cos(2 * 5))

    def test_newton(self) -> None:
        self.assertAlmostEqual(newton(lambda x: (x - 1) * (x + 5), 4), 1)
        self.assertAlmostEqual(newton(lambda x: exp(2 * x) - 10, 0.1), log(10) / 2)


if __name__ == '__main__':
    main()
