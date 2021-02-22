from math import log
from unittest import main, TestCase

from math2.economics import ContinuousInterest, EffectiveInterest, NominalInterest, SubperiodInterest


class InterestTestCase(TestCase):
    r, n, t, a = 0.1, 4, 2.5, 1.2800845441963565
    counts = list(range(1, 366))

    def test_interests(self) -> None:
        factors = [
            EffectiveInterest((1 + self.r / self.n) ** self.n - 1),
            ContinuousInterest(log((1 + self.r / self.n) ** self.n)),
            NominalInterest(self.r, self.n),
            SubperiodInterest(self.r / self.n, self.n),
        ]

        for factor in factors:
            self.assertAlmostEqual(factor(self.t), self.a)
            self.assertAlmostEqual(factor.to_effective()(self.t), self.a)
            self.assertAlmostEqual(factor.to_continuous()(self.t), self.a)

            for count in self.counts:
                self.assertAlmostEqual(factor.to_nominal(count)(self.t), self.a)
                self.assertAlmostEqual(factor.to_subperiod(count)(self.t), self.a)

        self.assertAlmostEqual(NominalInterest(self.r, self.n).to_nominal()(self.t), self.a)
        self.assertAlmostEqual(NominalInterest(self.r, self.n).to_subperiod()(self.t), self.a)
        self.assertAlmostEqual(SubperiodInterest(self.r / self.n, self.n).to_nominal()(self.t), self.a)
        self.assertAlmostEqual(SubperiodInterest(self.r / self.n, self.n).to_subperiod()(self.t), self.a)


if __name__ == '__main__':
    main()
