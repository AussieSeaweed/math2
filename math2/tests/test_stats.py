from unittest import main

from auxiliary import ExtTestCase

from math2.stats import range_, shuffled, trimmed_mean


class StatsTestCase(ExtTestCase):
    value_sets = ((0.32, 0.53, 0.28, 0.37, 0.47, 0.43, 0.36, 0.42, 0.38, 0.43),
                  (0.26, 0.43, 0.47, 0.49, 0.52, 0.75, 0.79, 0.86, 0.62, 0.46),
                  (7.07, 7.00, 7.10, 6.97, 7.00, 7.03, 7.01, 7.01, 6.98, 7.08),
                  (1., 2., 3., 4., 5.))

    def test_trimmed_mean(self) -> None:
        self.assertIterableAlmostEqual(map(lambda seq: trimmed_mean(seq, 0.1), self.value_sets),
                                       (0.39750, 0.56625, 7.0225, 3))

    def test_range(self) -> None:
        self.assertAlmostEqual(range_(map(float, range(5))), 4)
        self.assertIterableAlmostEqual(map(range_, self.value_sets), (0.25, 0.6, 0.13, 4))

    def test_shuffled(self) -> None:
        a = list(range(1000))

        self.assertNotEqual(shuffled(a), a)


if __name__ == '__main__':
    main()
