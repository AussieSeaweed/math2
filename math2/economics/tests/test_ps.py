from unittest import TestCase, main

import numpy as np
from auxiliary.tests import ExtendedTestCase
from scipy.optimize import fsolve

from math2.economics import (Bond, CompoundInterest, ContinuousInterest, EffectiveInterest, Mortgage, NominalInterest,
                             SubperiodInterest, fp, pa, pf, pg)


class PS1TestCase(TestCase):
    def test_1(self):
        self.assertLess(8000 + 1200, 6800 + 2500)
        self.assertTrue(np.isclose(fsolve(lambda mv: 8000 + 1200 - (mv + 2500), np.array(6800)), np.array(6700)))

    def test_2(self):
        self.assertTrue(np.isclose(fsolve(lambda t: 7500 - t * 1700, np.array(0)), np.array(4.411764705882353)))
        self.assertTrue(np.isclose(fsolve(lambda t: 9000 - t * 2200, np.array(0)), np.array(4.09090909)))

    def test_3(self):
        self.assertAlmostEqual((1 + 0.05 / 1000000) ** 1000000., np.exp(0.05))

    def test_4(self):
        e = EffectiveInterest(0.034)
        p, t = 100000, 4

        self.assertAlmostEqual(e.to_nominal(2).rate, 0.03371581102178567)
        self.assertAlmostEqual(e.to_nominal(12).rate, 0.033481397886386155)
        self.assertAlmostEqual(e.to_nominal(365).rate, 0.03343630748129267)
        self.assertAlmostEqual(e.to_continuous().rate, 0.03343477608623742)

        self.assertAlmostEqual(p * e.to_nominal(2).to_factor(t), p * e.to_nominal(12).to_factor(t))
        self.assertAlmostEqual(p * e.to_nominal(12).to_factor(t), p * e.to_nominal(365).to_factor(t))
        self.assertAlmostEqual(p * e.to_nominal(365).to_factor(t), p * e.to_continuous().to_factor(t))
        self.assertAlmostEqual(p * e.to_continuous().to_factor(t), 114309.4552336)

    def test_5(self):
        fv, c, cd = 100, 0.023, 0.02

        self.assertAlmostEqual(ContinuousInterest(c).to_effective().rate, 0.02326653954721758)
        self.assertAlmostEqual(fv / ContinuousInterest(c).to_factor(0.5), 98.8565872247913)
        self.assertAlmostEqual(fv / ContinuousInterest(c).to_factor(0.75), 98.28979294344309)
        self.assertAlmostEqual(fv / ContinuousInterest(cd).to_factor(0.5), 99.0049833749168)
        self.assertAlmostEqual(fv / ContinuousInterest(cd).to_factor(0.75), 98.51119396030627)

    def test_6(self):
        self.assertAlmostEqual(EffectiveInterest(0.08).to_subperiod(12).rate, 0.00643403011000343)
        self.assertAlmostEqual(NominalInterest(0.035, 252).to_effective().rate, 0.03561719190449408)
        self.assertAlmostEqual(NominalInterest(0.04, 4).to_continuous().rate, 0.039801323412672354)
        self.assertAlmostEqual(CompoundInterest.from_factor(SubperiodInterest(0.015, 12).to_factor(1), 4)
                               .to_continuous().rate, 0.04466583748125169)
        self.assertAlmostEqual(CompoundInterest.from_factor(CompoundInterest.from_factor(
            NominalInterest(0.012, 3).to_factor(1), 1 / 4).to_factor(3), 1).to_nominal(6).rate, 0.1454477030768886)


class PS2TestCase(ExtendedTestCase):
    def test_1(self):
        factor = NominalInterest(0.15, 4).to_factor(4 / 12) * ContinuousInterest(0.11).to_factor(5 / 12)

        self.assertAlmostEqual(CompoundInterest.from_factor(factor, 9 / 12).rate, 0.134915472328168)

    def test_2(self):
        p, i, n = 100, 0.05, 10

        self.assertAlmostEqual(p * pa(i, n), p * ((1 + i) ** n - 1) / (i * (1 + i) ** n))

    def test_3(self):
        cases = [
            (1, 99.52, 0.05943811, 0.05773868),
            (4, 99.01, 0.03029791, 0.02984799),
            (8, 97.64, 0.03647384, 0.03582441),
            (12, 95.85, 0.04329682, 0.04238572),
        ]

        for m, p, x, y in cases:
            self.assertTrue(np.isclose(fsolve(lambda y: p * EffectiveInterest(y).to_factor(m / 12) - 100, np.array(0)),
                                       np.array(x)))
            self.assertTrue(np.isclose(fsolve(lambda y: p * ContinuousInterest(y).to_factor(m / 12) - 100, np.array(0)),
                                       np.array(y)))

        self.assertTrue(np.isclose(np.interp(7, [4, 8], [0.03029791, 0.03647384]), 0.0349298575))
        self.assertTrue(np.isclose(np.interp(7, [4, 8], [0.02984799, 0.03582441]), 0.034330305))

        self.assertTrue(np.isclose(fsolve(lambda y: 1.03029791 ** (4. / 12) * (1 + y) ** (8. / 12) - 1.04329682,
                                          np.array(0)), 0.04985765))

    def test_4(self):
        data = {
            2: 99.11,
            6: 98.72,
            9: 96.85,
            12: 95.97,
        }

        r = {
            t: fsolve(lambda y: p * ContinuousInterest(y).to_factor(t / 12) - 100, np.array(0)).item()
            for t, p in data.items()
        }

        r[4] = np.interp(4, [2, 6], [r[2], r[6]])
        r[5.5] = np.interp(5.5, [2, 6], [r[2], r[6]])
        r[7] = np.interp(7, [6, 9], [r[6], r[9]])
        r[10] = np.interp(10, [9, 12], [r[9], r[12]])

        self.assertAlmostEqual(100 * ContinuousInterest(r[2]).to_factor(-1. / 12),
                               99.55400544428134)
        self.assertAlmostEqual(100 * ContinuousInterest(r[4]).to_factor(-4. / 12),
                               98.68531348348684)
        self.assertAlmostEqual(100 * ContinuousInterest(r[5.5]).to_factor(-5.5 / 12),
                               98.66834503291024)
        self.assertAlmostEqual(100 * ContinuousInterest(r[7]).to_factor(-7 / 12),
                               98.18488742486127)
        self.assertAlmostEqual(100 * ContinuousInterest(r[10]).to_factor(-10 / 12),
                               96.54750684004732)

        self.assertAlmostEqual(2000 * pf(r[2], 1. / 12) + 500 * pf(r[4], 4. / 12) - 1200 * pf(r[7], 7. / 12)
                               - 1000 * pf(r[10], 10. / 12) + 500 * pf(r[12], 1), 820.3872419304298)

    def test_5(self):
        i = 0.02
        options = [
            15500 * pa(i, 10),
            140000,
            155000 * pf(i, 5),
            170000 * pf(i, 10),
        ]

        self.assertSequenceAlmostEqual(options, [139230.06759675476, 140000, 140388.27552363696, 139459.21097877636])
        self.assertEqual(max(range(4), key=lambda i: options[i]), 2)

    def test_6(self):
        i = 0.02
        options = [
            155000 * pf(i, 5),
            10000 * pa(i, 10) + 1500 * pg(i, 10),
        ]

        self.assertAlmostEqual(options[1], 148258.50062422457)
        self.assertEqual(max(range(2), key=lambda i: options[i]), 1)

    def test_7(self):
        i = 0.02
        option = 10000 * pa(i, 10, g=0.05)

        self.assertAlmostEqual(option, 112086.97925088322)


class PS3TestCase(TestCase):
    def test_1(self):
        m = Mortgage.from_dtv(2995000, 0.2, 5, 25)
        i1 = NominalInterest(0.02, 2)
        i2 = NominalInterest(0.04, 2)
        p = m.payment(i1)

        self.assertAlmostEqual(p, 10145.891129693951)
        self.assertAlmostEqual(p * 12 * 3, 365252.08066898223)
        self.assertAlmostEqual(m.pay(i1).payment(i2), 12128.043601452593)

    def test_2(self):
        self.assertAlmostEqual(Bond(100, 0, 2, 3 / 12).present_worth(0.07), 98.2946374365981)
        self.assertAlmostEqual(Bond(100, 0, 2, 5 / 12).present_worth(0.07), 97.17391685967232)
        self.assertAlmostEqual(Bond(100, 0, 2, 3).present_worth(0.07), 81.35006443077528)
        self.assertAlmostEqual(Bond.from_rate(100, 0.04, 2, 3).present_worth(0.07), 92.00717047033226)
        self.assertAlmostEqual(Bond.from_rate(100, 0.06, 2, 3.25).present_worth(0.07), 97.13753584095278)

    def test_3(self):
        self.assertTrue(np.isclose(fsolve(lambda y: Bond.from_rate(100, 0.07, 2, 3).present_worth(y) - 100,
                                          np.array(1)), np.array(0.07)))
        self.assertAlmostEqual(Bond.from_rate(100, 0.04, 2, 3).present_worth(0.05) + 100 * 0.04 / 2, 99.24593731921009)
        self.assertTrue(np.isclose(fsolve(lambda y: Bond.from_rate(100, 0.03, 2, 2.25).present_worth(y) - 100,
                                          np.array(0.1)), np.array(0.03)))
        self.assertAlmostEqual(Bond.from_rate(100, 0.07, 2, 2.25).present_worth(0.05), 104.20662940110009)
        self.assertTrue(np.isclose(fsolve(lambda c: Bond.from_rate(100, c, 2, 2.25).present_worth(0.03) - 114,
                                          np.array(0.1)), np.array(0.09481118)))

    def test_4(self): # TODO
        ...

    def test_5(self):
        y = fsolve(lambda y: Bond.from_rate(100, 0.07, 2, 7.5).present_worth(y) * fp(y / 2, 0.5) - 108,
                   np.array(0.1)).item()
        b = lambda c: Bond.from_rate(1000, c, 2, 9).present_worth(y)
        c = np.ceil(fsolve(lambda c: 9500000 / 2 - (4400 * b(c)), np.array(0.1)).item() / 0.0025) * 0.0025
        self.assertAlmostEqual(c, 0.0725)
        self.assertAlmostEqual(4400 * b(c), 4802235.185695498)
        c = np.ceil(fsolve(lambda c: 9500000 / 2 / (1 - 0.008) - (4400 * b(c)), np.array(0.1)).item() / 0.0025) * 0.0025
        self.assertAlmostEqual(c, 0.0725)
        self.assertAlmostEqual(4400 * b(c) * (1 - 0.008), 4763817.304209935)

    def test_6(self):
        self.assertAlmostEqual(Mortgage.from_down(500000, 50000, 5, 25).payment(NominalInterest(0.060755, 2)),
                               2899.3558026129626)
        self.assertAlmostEqual(Mortgage.from_down(500000, 50000, 3, 25).pay(NominalInterest(0.060755, 2), 700).payment(
            NominalInterest(0.060755, 2)), 3490.3113416458878)
        self.assertLess(Mortgage.from_down(500000, 50000, 3, 25).pay(NominalInterest(0.060755, 2)).principal,
                        Mortgage.from_down(500000, 50000, 3, 25).pay(NominalInterest(0.060755, 2), 700).principal)


if __name__ == '__main__':
    main()
