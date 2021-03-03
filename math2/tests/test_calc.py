from math import cos, sin
from unittest import main

from math2.calc import derivative
from math2.utils import ExtendedTestCase


class CalcTestCase(ExtendedTestCase):
    def test_derivative(self) -> None:
        self.assertAlmostEqual(derivative(lambda x: -3 * sin(2 * x), 5, 1e-7), -6 * cos(2 * 5))
        self.assertAlmostEqual(derivative(lambda x: x ** 3 - 2 * x ** 2, 3, 1e-7), 3 * 3 ** 2 - 4 * 3)


if __name__ == '__main__':
    main()
