from unittest import main

from auxiliary import ExtendedTestCase

from math2.misc import frange, interpolate, limit, product


class MiscTestCase(ExtendedTestCase):
    def test_product(self) -> None:
        self.assertEqual(product(range(6)), 0)
        self.assertEqual(product(range(1, 6)), 120)
        self.assertRaises(ValueError, product, ())

    def test_limit(self) -> None:
        self.assertEqual(limit(1, 0, 2), 1)
        self.assertEqual(limit(-100, 0, 2), 0)
        self.assertEqual(limit(100, 0, 2), 2)
        self.assertRaises(ValueError, limit, 100, 2, 0)

    def test_frange(self) -> None:
        self.assertIterableAlmostEqual(frange(5), (0, 1, 2, 3, 4))
        self.assertIterableAlmostEqual(frange(1, 5), (1, 2, 3, 4))
        self.assertIterableAlmostEqual(frange(1, 5, 0.5), (1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5))

    def test_interpolate(self) -> None:
        self.assertAlmostEqual(interpolate(1, 0, 2, 0, 3), 1.5)
        self.assertAlmostEqual(interpolate(1, 0, 1, 0, 3), 3)
        self.assertAlmostEqual(interpolate(2, 0, 1, 0, 6), 12)


if __name__ == '__main__':
    main()
