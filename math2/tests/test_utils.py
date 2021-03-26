from unittest import main

from auxiliary import ExtendedTestCase

from math2.utils import linspace, series_sum


class UtilsTestCase(ExtendedTestCase):
    def test_series_sum(self) -> None:
        self.assertEqual(series_sum(-5, 0), -15)
        self.assertEqual(series_sum(-5, 0), -15)
        self.assertEqual(series_sum(0, -5), -15)
        self.assertEqual(series_sum(5, 0), 15)
        self.assertEqual(series_sum(0, 5), 15)
        self.assertEqual(series_sum(0, 5, 6), 15)
        self.assertEqual(series_sum(0, 5, 2), 5)
        self.assertEqual(series_sum(1, 1, 1), 1)

    def test_linspace(self) -> None:
        self.assertIterableAlmostEqual(linspace(0, 5, 6), range(6))
        self.assertIterableAlmostEqual(linspace(1, 6, 5), (1, 2.25, 3.5, 4.75, 6))
        self.assertIterableAlmostEqual(linspace(2, 5, 2), (2, 5))


if __name__ == '__main__':
    main()
