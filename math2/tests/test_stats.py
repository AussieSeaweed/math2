from random import random
from unittest import main

from auxiliary import ExtendedTestCase

from math2.stats import mean, median, range_, standard_deviation, trimmed_mean, variance


class StatsTestCase(ExtendedTestCase):
    def setUp(self):
        self.value_sets = (
            (0.32, 0.53, 0.28, 0.37, 0.47, 0.43, 0.36, 0.42, 0.38, 0.43),
            (0.26, 0.43, 0.47, 0.49, 0.52, 0.75, 0.79, 0.86, 0.62, 0.46),
            (7.07, 7.00, 7.10, 6.97, 7.00, 7.03, 7.01, 7.01, 6.98, 7.08),
            (1., 2., 3., 4., 5.),
        )

    def test_mean(self):
        self.assertIterableAlmostEqual((mean(seq) for seq in self.value_sets), (0.399, 0.565, 7.025, 3))

    def test_trimmed_mean(self):
        self.assertIterableAlmostEqual((trimmed_mean(seq, 0.1) for seq in self.value_sets),
                                       (0.39750, 0.56625, 7.0225, 3))

    def test_range(self):
        self.assertAlmostEqual(range_(range(5)), 4)
        self.assertIterableAlmostEqual(map(range_, self.value_sets), (0.25, 0.6, 0.13, 4))


class PS1TestCase(ExtendedTestCase):
    def test_1(self):
        samples = 3.4, 2.5, 4.8, 2.9, 3.6, 2.8, 3.3, 5.6, 3.7, 2.8, 4.4, 4.0, 5.2, 3.0, 4.8

        self.assertEqual(len(samples), 15)
        self.assertAlmostEqual(mean(samples), 3.7866666666666667)
        self.assertAlmostEqual(median(samples), 3.6)
        self.assertAlmostEqual(trimmed_mean(samples, 0.2), 3.677777777777778)
        self.assertAlmostEqual(mean(samples), trimmed_mean(samples, 0.2), 0)

    def test_5(self):
        control = 7, 3, -4, 14, 2, 5, 22, -7, 9, 5
        treatment = -6, 5, 9, 4, 4, 12, 37, 5, 3, 3

        self.assertAlmostEqual(mean(control), 5.6)
        self.assertAlmostEqual(median(control), 5.0)
        self.assertAlmostEqual(trimmed_mean(control, 0.1), 5.125)
        self.assertAlmostEqual(mean(treatment), 7.6)
        self.assertAlmostEqual(median(treatment), 4.5)
        self.assertAlmostEqual(trimmed_mean(treatment, 0.1), 5.625)

        self.assertNotAlmostEqual(mean(control), mean(treatment), 0)
        self.assertAlmostEqual(median(control), median(treatment), 0)

    def test_6(self):
        twenty = 2.07, 2.14, 2.22, 2.03, 2.21, 2.03, 2.05, 2.18, 2.09, 2.14, 2.11, 2.02
        forty_five = 2.52, 2.12, 2.49, 2.03, 2.37, 2.05, 1.99, 2.42, 2.08, 2.42, 2.29, 2.01

        self.assertAlmostEqual(mean(twenty), 2.1075)
        self.assertAlmostEqual(mean(forty_five), 2.2325)

        self.assertLess(mean(twenty), mean(forty_five))
        self.assertLess(variance(twenty), variance(forty_five))

    def test_7(self):
        samples = 3.4, 2.5, 4.8, 2.9, 3.6, 2.8, 3.3, 5.6, 3.7, 2.8, 4.4, 4.0, 5.2, 3.0, 4.8

        self.assertAlmostEqual(variance(samples), 0.9426666666666667)
        self.assertAlmostEqual(standard_deviation(samples), 0.9709102258533828)

    def test_11(self):
        control = 7, 3, -4, 14, 2, 5, 22, -7, 9, 5
        treatment = -6, 5, 9, 4, 4, 12, 37, 5, 3, 3

        self.assertAlmostEqual(variance(control), 69.37777777777778)
        self.assertAlmostEqual(standard_deviation(control), 8.329332372872257)
        self.assertAlmostEqual(variance(treatment), 128.04444444444445)
        self.assertAlmostEqual(standard_deviation(treatment), 11.315672514015437)

    def test_12(self):
        twenty = 2.07, 2.14, 2.22, 2.03, 2.21, 2.03, 2.05, 2.18, 2.09, 2.14, 2.11, 2.02
        forty_five = 2.52, 2.12, 2.49, 2.03, 2.37, 2.05, 1.99, 2.42, 2.08, 2.42, 2.29, 2.01

        self.assertAlmostEqual(standard_deviation(twenty), 0.07085516597577456)
        self.assertAlmostEqual(standard_deviation(forty_five), 0.20450050011052434)
        self.assertLess(standard_deviation(twenty), standard_deviation(forty_five))

    def test_16(self):
        values = tuple(random() for _ in range(1000))
        mu = mean(values)

        self.assertAlmostEqual(sum(x - mu for x in values), 0)

    def test_18(self):
        samples = (23, 60, 79, 32, 57, 74, 52, 70, 82, 36, 80, 77, 81, 95, 41, 65, 92, 85, 55, 76, 52, 10, 64, 75, 78,
                   25, 80, 98, 81, 67, 41, 71, 83, 54, 64, 72, 88, 62, 74, 43, 60, 78, 89, 76, 84, 48, 84, 90, 15, 79,
                   34, 67, 17, 82, 69, 74, 63, 80, 85, 61)

        self.assertAlmostEqual(mean(samples), 65.48333333333333)
        self.assertAlmostEqual(median(samples), 71.5)
        self.assertAlmostEqual(standard_deviation(samples), 21.133547647240682)

    def test_19(self):
        samples = (2.0, 3.0, 0.3, 3.3, 1.3, 0.4, 0.2, 6.0, 5.5, 6.5, 0.2, 2.3, 1.5, 4.0, 5.9, 1.8, 4.7, 0.7, 4.5, 0.3,
                   1.5, 0.5, 2.5, 5.0, 1.0, 6.0, 5.6, 6.0, 1.2, 0.2)

        self.assertAlmostEqual(mean(samples), 2.796666666666667)
        self.assertAlmostEqual(range_(samples), 6.3)
        self.assertAlmostEqual(standard_deviation(samples), 2.2273354009905533)


class PS2TestCase(ExtendedTestCase):
    pass


class PS3TestCase(ExtendedTestCase):
    pass


class PS4TestCase(ExtendedTestCase):
    pass


if __name__ == '__main__':
    main()
