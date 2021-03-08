from unittest import main

from auxiliary import ExtendedTestCase

from math2.ntheory import gcd, lcm


class NTheoryTestCase(ExtendedTestCase):
    def test_gcd(self) -> None:
        self.assertEqual(gcd(9, 15), 3)
        self.assertEqual(gcd(5, 3), 1)
        self.assertEqual(gcd(5, 5), 5)
        self.assertEqual(gcd(0, 1), 1)
        self.assertEqual(gcd(1, 0), 1)
        self.assertEqual(gcd(0, 0), 0)
        self.assertAlmostEqual(gcd(0.75, 0.5), 0.25)
        self.assertIsInstance(gcd(9, 15), int)
        self.assertIsInstance(gcd(0.75, 0.5), float)

    def test_lcm(self) -> None:
        self.assertEqual(lcm(5, 10), 10)
        self.assertEqual(lcm(75, 10), 150)
        self.assertAlmostEqual(lcm(0.75, 1), 3)
        self.assertAlmostEqual(lcm(0.75, 0.5), 1.5)
        self.assertIsInstance(lcm(75, 10), int)
        self.assertIsInstance(lcm(0.75, 1), float)


if __name__ == '__main__':
    main()
