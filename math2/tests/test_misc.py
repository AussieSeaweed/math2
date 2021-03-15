from unittest import main

from math2.misc import series_sum
from auxiliary import ExtendedTestCase


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


if __name__ == '__main__':
    main()
