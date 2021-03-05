from collections import Callable
from math import ceil, exp, log
from unittest import TestCase, main

from auxiliary import ExtendedTestCase

from math2.calc import newton
from math2.econ import (Bond, CompoundInterest, ContinuousInterest, EffectiveInterest, Mortgage, NominalInterest,
                        Project, Relationship, SimpleInterest, SubperiodInterest, combinations, fp, from_table, irr, pa,
                        pf, pg, relationship)
from math2.misc import interpolate


class InterestTestCase(TestCase):
    def test_difference(self) -> None:
        r, p, t, s, c = 0.07, 24, 2020 - 1626, 685.92, 9066082143624.828

        self.assertAlmostEqual(p * SimpleInterest(r).to_factor(t), s)
        self.assertAlmostEqual(p * EffectiveInterest(r).to_factor(t), c)

    def test_comparison(self) -> None:
        self.assertLess(NominalInterest(0.06, 12).to_effective().rate, SubperiodInterest(0.063, 1).to_effective().rate)

    def test_consistency(self) -> None:
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


class InstrumentTestCase(ExtendedTestCase):
    def test_relationships(self) -> None:
        self.assertEqual(relationship([5000, 7000, 6000, 3000], 1000000), Relationship.INDEPENDENT)
        self.assertEqual(relationship([5000, 7000, 6000, 3000], 7000), Relationship.MUTUALLY_EXCLUSIVE)
        self.assertEqual(relationship([5000, 7000, 6000, 3000], 10000), Relationship.RELATED)

    def test_combinations(self) -> None:
        self.assertLen(tuple(combinations([5000, 7000, 6000, 3000], 10000)), 8)

    def test_projects(self) -> None:
        self.assertAlmostEqual(Project(-20000, 4000 - 1000, 4000, 10).present_worth(EffectiveInterest(0.05)),
                               9680.783294664216)
        self.assertAlmostEqual(Project(-20000, 4000 - 1000, 4000, 10).annual_worth(EffectiveInterest(0.05)),
                               727.9268005526942)


class PS1TestCase(TestCase):
    def test_1(self) -> None:
        self.assertLess(8000 + 1200, 6800 + 2500)
        self.assertAlmostEqual(newton(lambda mv: 8000 + 1200 - (mv + 2500), 6800), 6700)

    def test_2(self) -> None:
        self.assertAlmostEqual(newton(lambda t: 7500 - t * 1700, 0), 4.411764705882353)
        self.assertAlmostEqual(newton(lambda t: 9000 - t * 2200, 0), 4.09090909)

    def test_3(self) -> None:
        self.assertAlmostEqual((1 + 0.05 / 1000000) ** 1000000, exp(0.05))

    def test_4(self) -> None:
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

    def test_5(self) -> None:
        fv, c, cd = 100, 0.023, 0.02

        self.assertAlmostEqual(ContinuousInterest(c).to_effective().rate, 0.02326653954721758)
        self.assertAlmostEqual(fv / ContinuousInterest(c).to_factor(0.5), 98.8565872247913)
        self.assertAlmostEqual(fv / ContinuousInterest(c).to_factor(0.75), 98.28979294344309)
        self.assertAlmostEqual(fv / ContinuousInterest(cd).to_factor(0.5), 99.0049833749168)
        self.assertAlmostEqual(fv / ContinuousInterest(cd).to_factor(0.75), 98.51119396030627)

    def test_6(self) -> None:
        self.assertAlmostEqual(EffectiveInterest(0.08).to_subperiod(12).rate, 0.00643403011000343)
        self.assertAlmostEqual(NominalInterest(0.035, 252).to_effective().rate, 0.03561719190449408)
        self.assertAlmostEqual(NominalInterest(0.04, 4).to_continuous().rate, 0.039801323412672354)
        self.assertAlmostEqual(CompoundInterest.from_factor(SubperiodInterest(0.015, 12).to_factor(1), 4)
                               .to_continuous().rate, 0.04466583748125169)
        self.assertAlmostEqual(CompoundInterest.from_factor(CompoundInterest.from_factor(
            NominalInterest(0.012, 3).to_factor(1), 1 / 4).to_factor(3), 1).to_nominal(6).rate, 0.1454477030768886)


class PS2TestCase(ExtendedTestCase):
    def test_1(self) -> None:
        factor = NominalInterest(0.15, 4).to_factor(4 / 12) * ContinuousInterest(0.11).to_factor(5 / 12)

        self.assertAlmostEqual(CompoundInterest.from_factor(factor, 9 / 12).rate, 0.134915472328168)

    def test_2(self) -> None:
        p, i, n = 100, 0.05, 10

        self.assertAlmostEqual(p * pa(i, n), p * ((1 + i) ** n - 1) / (i * (1 + i) ** n))

    def test_3(self) -> None:
        cases = [
            (1, 99.52, 0.05943811, 0.05773868),
            (4, 99.01, 0.03029791, 0.02984799),
            (8, 97.64, 0.03647384, 0.03582441),
            (12, 95.85, 0.04329682, 0.04238572),
        ]

        for m, p, a, b in cases:
            self.assertAlmostEqual(newton(lambda y: p * EffectiveInterest(y).to_factor(m / 12) - 100, 0), a)
            self.assertAlmostEqual(newton(lambda y: p * ContinuousInterest(y).to_factor(m / 12) - 100, 0), b)

        self.assertAlmostEqual(interpolate(7, 4, 8, 0.03029791, 0.03647384), 0.0349298575)
        self.assertAlmostEqual(interpolate(7, 4, 8, 0.02984799, 0.03582441), 0.034330305)

        self.assertAlmostEqual(newton(lambda y: 1.03029791 ** (4. / 12) * (1 + y) ** (8. / 12) - 1.04329682, 0),
                               0.04985765)

    def test_4(self) -> None:
        data = {
            2: 99.11,
            6: 98.72,
            9: 96.85,
            12: 95.97,
        }

        r: dict[float, float] = {
            t: newton(lambda y: p * ContinuousInterest(y).to_factor(t / 12) - 100, 0)
            for t, p in data.items()
        }

        r[4] = interpolate(4, 2, 6, r[2], r[6])
        r[5.5] = interpolate(5.5, 2, 6, r[2], r[6])
        r[7] = interpolate(7, 6, 9, r[6], r[9])
        r[10] = interpolate(10, 9, 12, r[9], r[12])

        self.assertAlmostEqual(100 * ContinuousInterest(r[2]).to_factor(-1. / 12), 99.55400544428134)
        self.assertAlmostEqual(100 * ContinuousInterest(r[4]).to_factor(-4. / 12), 98.68531340424114)
        self.assertAlmostEqual(100 * ContinuousInterest(r[5.5]).to_factor(-5.5 / 12), 98.66834503291024)
        self.assertAlmostEqual(100 * ContinuousInterest(r[7]).to_factor(-7 / 12), 98.18488742486127)
        self.assertAlmostEqual(100 * ContinuousInterest(r[10]).to_factor(-10 / 12), 96.54750684004732)
        self.assertAlmostEqual(2000 * pf(r[2], 1. / 12) + 500 * pf(r[4], 4. / 12) - 1200 * pf(r[7], 7. / 12) - 1000
                               * pf(r[10], 10. / 12) + 500 * pf(r[12], 1), 820.3872407904064)

    def test_5(self) -> None:
        i = 0.02
        options = (
            15500 * pa(i, 10),
            140000,
            155000 * pf(i, 5),
            170000 * pf(i, 10),
        )

        self.assertSequenceAlmostEqual(options, (139230.06759675476, 140000, 140388.27552363696, 139459.21097877636))
        self.assertEqual(max(range(4), key=options.__getitem__), 2)

    def test_6(self) -> None:
        i = 0.02
        options = (
            155000 * pf(i, 5),
            10000 * pa(i, 10) + 1500 * pg(i, 10),
        )

        self.assertAlmostEqual(options[1], 148258.50062422457)
        self.assertEqual(max(range(2), key=options.__getitem__), 1)

    def test_7(self) -> None:
        i = 0.02
        option = 10000 * pa(i, 10, g=0.05)

        self.assertAlmostEqual(option, 112086.97925088322)


class PS3TestCase(TestCase):
    def test_1(self) -> None:
        m = Mortgage.from_dtv(2995000, 0.2)
        i1 = NominalInterest(0.02, 2)
        i2 = NominalInterest(0.04, 2)
        p = m.payment(i1)

        self.assertAlmostEqual(p, 10145.891129693951)
        self.assertAlmostEqual(p * 12 * 3, 365252.08066898223)
        self.assertAlmostEqual(m.pay(i1, 5).payment(i2), 12128.043601452593)

    def test_2(self) -> None:
        i = NominalInterest(0.07, 2)

        self.assertAlmostEqual(Bond(100, 0, 2, 3 / 12).present_worth(i), 98.2946374365981)
        self.assertAlmostEqual(Bond(100, 0, 2, 5 / 12).present_worth(i), 97.17391685967232)
        self.assertAlmostEqual(Bond(100, 0, 2, 3).present_worth(i), 81.35006443077528)
        self.assertAlmostEqual(Bond.from_rate(100, 0.04, 2, 3).present_worth(i), 92.00717047033226)
        self.assertAlmostEqual(Bond.from_rate(100, 0.06, 2, 3.25).present_worth(i), 97.13753584095278)

    def test_3(self) -> None:
        self.assertAlmostEqual(
            newton(lambda y: Bond.from_rate(100, 0.07, 2, 3).present_worth(NominalInterest(y, 2)) - 100, 0.1), 0.07)
        self.assertAlmostEqual(
            Bond.from_rate(100, 0.04, 2, 3).present_worth(NominalInterest(0.05, 2)) + 100 * 0.04 / 2, 99.24593731921009)
        self.assertAlmostEqual(
            newton(lambda y: Bond.from_rate(100, 0.03, 2, 2.25).present_worth(NominalInterest(y, 2)) - 100, 0.1), 0.03)
        self.assertAlmostEqual(
            Bond.from_rate(100, 0.07, 2, 2.25).present_worth(NominalInterest(0.05, 2)), 104.20662940110009)
        self.assertAlmostEqual(newton(
            lambda c: Bond.from_rate(100, c, 2, 2.25).present_worth(NominalInterest(0.03, 2)) - 114, 0.1), 0.09481118)

    def test_4(self) -> None:
        pass

    def test_5(self) -> None:
        y = newton(
            lambda y_: Bond.from_rate(100, 0.07, 2, 7.5).present_worth(NominalInterest(y_, 2)) * fp(y_ / 2, 0.5) - 108,
            0.1)

        b: Callable[[float], float] = lambda c_: Bond.from_rate(1000, c_, 2, 9).present_worth(NominalInterest(y, 2))
        c = ceil(newton(lambda c_: 9500000 / 2 - (4400 * b(c_)), 0.1) / 0.0025) * 0.0025
        self.assertAlmostEqual(c, 0.0725)
        self.assertAlmostEqual(4400 * b(c), 4802235.185695931)
        c = ceil(newton(lambda c_: 9500000 / 2 / (1 - 0.008) - (4400 * b(c_)), 0.1) / 0.0025) * 0.0025
        self.assertAlmostEqual(c, 0.0725)
        self.assertAlmostEqual(4400 * b(c) * (1 - 0.008), 4763817.304210364)

    def test_6(self) -> None:
        i = NominalInterest(0.060755, 2)

        self.assertAlmostEqual(Mortgage.from_down(500000, 50000).payment(i), 2899.3558026129626)
        self.assertAlmostEqual(Mortgage.from_down(500000, 50000).pay(i, 3, 700).payment(i), 3490.3113416458878)
        self.assertLess(Mortgage.from_down(500000, 50000, 25).pay(i, 3).principal,
                        Mortgage.from_down(500000, 50000, 25).pay(i, 3, 700).principal)


class PS6TestCase(ExtendedTestCase):
    def test_1(self) -> None:
        data = ((-41000, 6100, 7),
                (-32000, 6700, 7),
                (-28000, 5700, 5),
                (-28000, 12600, 5),
                (-36000, 9000, 7),
                (-27000, 10600, 6),
                (-53000, 6700, 5),
                (-50000, 15000, 6),
                (-32000, 6900, 7),
                (-42000, 14600, 5))

        irr_set = tuple(map(lambda d: irr(Project(d[0], d[1], 0, d[2]).cash_flows(), 0).rate, data))

        self.assertSequenceAlmostEqual(irr_set, (
            0.010261108929599895,
            0.10584583010815002,
            0.005929015028005828,
            0.3494328573992243,
            0.16326709023510008,
            0.31754169406374866,
            -0.13571830650187303,
            0.1990541470961173,
            0.114956469240095,
            0.2178733729868983,
        ))

        points = sorted(range(len(data)), key=irr_set.__getitem__, reverse=True)

        cost = 0
        marr = 0.0

        for point in points:
            cost -= data[point][0]

            if cost > 100000:
                break

            marr = irr_set[point]

        self.assertAlmostEqual(marr, 0.2178733729868983)

    def test_2(self) -> None:
        self.assertEqual(from_table(
            ((),
             (0.17,),
             (0.14, 0.075),
             (0.19, 0.209, 0.286),
             (0.2, 0.127, 0.257, 0.229),
             (0.18, 0.177, 0.192, 0.158, 0.117),
             (0.13, 0.128, 0.132, 0.106, 0.081, 0.062)),
            0.12,
        ), 4)

        self.assertEqual(from_table(
            ((),
             (0.14,),
             (0.20, 0.29),
             (0.24, 0.32, 0.36),
             (0.21, 0.24, 0.22, 0.11),
             (0.17, 0.18, 0.15, 0.08, 0.06),
             (0.17, 0.18, 0.16, 0.12, 0.13, 0.19)),
            0.12,
        ), 3)

    def test_3(self) -> None:
        table = ((),
                 (0.1096,),
                 (0.132, 0.286),
                 (0.1205, 0.17, -0.058),
                 (0.1293, 0.189, 0.112, 0.228),
                 (0.1286, 0.177, 0.112, 0.187, 0.113),
                 (0.1113, 0.113, 0.079, 0.094, 0.069, 0.063))

        self.assertEqual(from_table(table, 0.04), 6)
        self.assertEqual(from_table(table, 0.06), 6)
        self.assertEqual(from_table(table, 0.08), 5)
        self.assertEqual(from_table(table, 0.10), 5)
        self.assertEqual(from_table(table, 0.12), 2)
        self.assertEqual(from_table(table, 0.14), 0)

    def test_4(self) -> None:
        pass

    def test_5(self) -> None:
        pass


if __name__ == '__main__':
    main()
