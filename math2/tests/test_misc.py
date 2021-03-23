from unittest import main

from auxiliary import ExtendedTestCase

from math2.misc import frange, series_sum


class MiscTestCase(ExtendedTestCase):
    def test_series_sum(self):
        self.assertEqual(series_sum(-5), -15)
        self.assertEqual(series_sum(-5, 0), -15)
        self.assertEqual(series_sum(0, -5), -15)
        self.assertEqual(series_sum(5), 15)
        self.assertEqual(series_sum(0, 5), 15)
        self.assertEqual(series_sum(0, 5, 6), 15)
        self.assertEqual(series_sum(0, 5, 2), 5)
        self.assertEqual(series_sum(1, 1, 1), 1)

    def test_frange(self):
        self.assertIterableEqual(frange(5), range(5))
        self.assertIterableEqual(frange(1, 5), range(1, 5))
        self.assertIterableEqual(frange(2, 5, 2), range(2, 5, 2))


if __name__ == '__main__':
    main()
