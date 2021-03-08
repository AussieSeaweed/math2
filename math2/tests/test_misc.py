from unittest import main

from auxiliary import ExtendedTestCase

from math2.misc import bind, frange, interp, linspace, prod, series_sum, sum_


class MiscTestCase(ExtendedTestCase):
    def test_bind(self) -> None:
        self.assertEqual(bind(1, 0, 2), 1)
        self.assertEqual(bind(-100, 0, 2), 0)
        self.assertEqual(bind(100, 0, 2), 2)
        self.assertRaises(ValueError, bind, 100, 2, 0)

    def test_sum(self) -> None:
        self.assertEqual(sum_(range(6)), 15)
        self.assertEqual(sum_(range(6), 0), 15)
        self.assertEqual(sum_((), 1), 1)
        self.assertRaises(ValueError, sum_, ())

    def test_prod(self) -> None:
        self.assertEqual(prod(range(6)), 0)
        self.assertEqual(prod(range(1, 6)), 120)
        self.assertEqual(prod(range(1, 6), 1), 120)
        self.assertEqual(prod((), 1), 1)
        self.assertRaises(ValueError, prod, ())

    def test_frange(self) -> None:
        self.assertIterableAlmostEqual(frange(5), (0, 1, 2, 3, 4))
        self.assertIterableAlmostEqual(frange(1, 5), (1, 2, 3, 4))
        self.assertIterableAlmostEqual(frange(1, 5, 0.5), (1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5))

    def test_linspace(self) -> None:
        self.assertIterableAlmostEqual(linspace(0, 5), frange(0, 5, 0.05))
        self.assertIterableAlmostEqual(linspace(0, 5, 5), range(5))

    def test_interp(self) -> None:
        self.assertAlmostEqual(interp(1, 0, 2, 0, 3), 1.5)
        self.assertAlmostEqual(interp(1, 0, 1, 0, 3), 3)
        self.assertAlmostEqual(interp(2, 0, 1, 0, 6), 12)

    def test_series_sum(self) -> None:
        self.assertEqual(series_sum(-5), -15)
        self.assertEqual(series_sum(-5, 0), -15)
        self.assertEqual(series_sum(0, -5), -15)
        self.assertEqual(series_sum(5), 15)
        self.assertEqual(series_sum(0, 5), 15)
        self.assertEqual(series_sum(0, 5, 6), 15)
        self.assertEqual(series_sum(0, 5, 2), 5)
        self.assertEqual(series_sum(1, 1, 1), 1)


if __name__ == '__main__':
    main()
