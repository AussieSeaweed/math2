from unittest import main

from math2.ntheory import gcd, lcm
from math2.utils import ExtendedTestCase


class NTheoryTestCase(ExtendedTestCase):
    def test_gcd(self) -> None:
        self.assertAlmostEqual(gcd(0.75, 0.5), 0.25)
        self.assertAlmostEqual(gcd(9, 15), 3)
        self.assertAlmostEqual(gcd(5, 3), 1)
        self.assertAlmostEqual(gcd(5, 5), 5)
        self.assertAlmostEqual(gcd(0, 1), 1)
        self.assertAlmostEqual(gcd(1, 0), 1)
        self.assertAlmostEqual(gcd(0, 0), 0)

    def test_lcm(self) -> None:
        self.assertAlmostEqual(lcm(0.75, 1), 3)
        self.assertAlmostEqual(lcm(0.75, 0.5), 1.5)


if __name__ == '__main__':
    main()
