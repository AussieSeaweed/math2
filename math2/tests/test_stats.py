from unittest import main

from auxiliary import ExtendedTestCase

from math2.stats import mean, median, range_, standard_deviation, trimmed_mean, variance


class StatsTestCase(ExtendedTestCase):
    value_sets = ((0.32, 0.53, 0.28, 0.37, 0.47, 0.43, 0.36, 0.42, 0.38, 0.43),
                  (0.26, 0.43, 0.47, 0.49, 0.52, 0.75, 0.79, 0.86, 0.62, 0.46),
                  (7.07, 7.00, 7.10, 6.97, 7.00, 7.03, 7.01, 7.01, 6.98, 7.08),
                  (1., 2., 3., 4., 5.))

    def test_averages(self) -> None:
        self.assertIterableAlmostEqual(map(mean, self.value_sets), (0.399, 0.565, 7.025, 3))
        self.assertIterableAlmostEqual(map(lambda seq: trimmed_mean(seq, 0.1), self.value_sets),
                                       (0.39750, 0.56625, 7.0225, 3))
        self.assertIterableAlmostEqual(map(median, self.value_sets), (0.400, 0.505, 7.01, 3))

    def test_vars(self) -> None:
        self.assertAlmostEqual(range_(map(float, range(5))), 4)
        self.assertIterableAlmostEqual(map(range_, self.value_sets), (0.25, 0.6, 0.13, 4))
        self.assertIterableAlmostEqual(map(variance, self.value_sets),
                                       (0.00529888888888889, 0.03487222222222222, 0.0019388888888888889, 2.5))
        self.assertIterableAlmostEqual(map(standard_deviation, self.value_sets),
                                       (0.07279346735036663, 0.18674105660572402, 0.044032816045409685,
                                        1.5811388300841898))


if __name__ == '__main__':
    main()
