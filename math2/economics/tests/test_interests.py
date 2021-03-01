from math import log
from unittest import TestCase, main

from math2.economics import ContinuousInterest, EffectiveInterest, NominalInterest, SimpleInterest, SubperiodInterest


class InterestTestCase(TestCase):
    def test_difference(self):
        r, p, t, s, c = 0.07, 24, 2020 - 1626, 685.92, 9066082143624.828

        self.assertAlmostEqual(p * SimpleInterest(r).to_factor(t), s)
        self.assertAlmostEqual(p * EffectiveInterest(r).to_factor(t), c)

    def test_comparison(self):
        self.assertLess(NominalInterest(0.06, 12).to_effective().rate, SubperiodInterest(0.063, 1).to_effective().rate)

    def test_consistency(self):
        nr, sc, t, f = 0.1, 4, 2.5, 1.2800845441963565
        counts = range(1, 366)

        interests = [
            EffectiveInterest((1 + nr / sc) ** sc - 1),
            ContinuousInterest(log((1 + nr / sc) ** sc)),
            NominalInterest(nr, sc),
            SubperiodInterest(nr / sc, sc),
        ]

        for interest in interests:
            self.assertAlmostEqual(interest.to_factor(t), f)
            self.assertAlmostEqual(interest.to_effective().to_factor(t), f)
            self.assertAlmostEqual(interest.to_continuous().to_factor(t), f)

            for count in counts:
                self.assertAlmostEqual(interest.to_nominal(count).to_factor(t), f)
                self.assertAlmostEqual(interest.to_subperiod(count).to_factor(t), f)

        self.assertAlmostEqual(NominalInterest(nr, sc).to_nominal().to_factor(t), f)
        self.assertAlmostEqual(NominalInterest(nr, sc).to_subperiod().to_factor(t), f)
        self.assertAlmostEqual(SubperiodInterest(nr / sc, sc).to_nominal().to_factor(t), f)
        self.assertAlmostEqual(SubperiodInterest(nr / sc, sc).to_subperiod().to_factor(t), f)


if __name__ == '__main__':
    main()
