from math import cos, exp, log, sin
from unittest import main

from auxiliary import ExtendedTestCase

from math2.calc import derivative, euler, newton


class CalcTestCase(ExtendedTestCase):
    def test_derivative(self) -> None:
        self.assertAlmostEqual(derivative(lambda x: x ** 3 - 2 * x ** 2, 3), 3 * 3 ** 2 - 4 * 3)
        self.assertAlmostEqual(derivative(lambda x: -3 * sin(2 * x), 5), -6 * cos(2 * 5))

    def test_newton(self) -> None:
        self.assertAlmostEqual(newton(lambda x: (x - 1) * (x + 5), 4), 1)
        self.assertAlmostEqual(newton(lambda x: exp(2 * x) - 10, 0.1), log(10) / 2)

    def test_euler(self) -> None:
        self.assertAlmostEqual(euler(lambda x: x, 0, 1), 0.5, 2)
        self.assertAlmostEqual(euler(lambda x: 2 * x ** 2, -1, 1), 4 / 3, 3)


if __name__ == '__main__':
    main()
