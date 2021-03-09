from collections.abc import Callable
from math import ceil, exp, inf, log
from unittest import TestCase, main

from auxiliary import ExtTestCase, ilen

from math2.calc import newton
from math2.econ import (Bond, CashFlow, CompInt, ContInt, DblDeclBalDeprec, DeclBalDeprec, EfInt, Mortgage, NomInt,
                        Project, Rel, SYDDeprec, SimpleInt, StrLineDeprec, SubperiodInt, UPDeprec, aw, de_facto_marr,
                        fp,
                        from_table, irr,
                        pa, payback, pf, pg, pw, rel, rel_combinations)
from math2.misc import interp


class InterestTestCase(TestCase):
    def test_difference(self) -> None:
        r, p, t, s, c = 0.07, 24, 2020 - 1626, 685.92, 9066082143624.828

        self.assertAlmostEqual(p * SimpleInt(r).to_factor(t), s)
        self.assertAlmostEqual(p * EfInt(r).to_factor(t), c)

    def test_comparison(self) -> None:
        self.assertLess(NomInt(0.06, 12).to_ef().rate, SubperiodInt(0.063, 1).to_ef().rate)

    def test_consistency(self) -> None:
        nr, sc, t, f = 0.1, 4, 2.5, 1.2800845441963565
        counts = range(1, 366)

        interests = (
            EfInt((1 + nr / sc) ** sc - 1),
            ContInt(log((1 + nr / sc) ** sc)),
            NomInt(nr, sc),
            SubperiodInt(nr / sc, sc),
        )

        for interest in interests:
            self.assertAlmostEqual(interest.to_factor(t), f)
            self.assertAlmostEqual(interest.to_ef().to_factor(t), f)
            self.assertAlmostEqual(interest.to_cont().to_factor(t), f)

            for count in counts:
                self.assertAlmostEqual(interest.to_nom(count).to_factor(t), f)
                self.assertAlmostEqual(interest.to_subperiod(count).to_factor(t), f)

        self.assertAlmostEqual(NomInt(nr, sc).to_nom().to_factor(t), f)
        self.assertAlmostEqual(NomInt(nr, sc).to_subperiod().to_factor(t), f)
        self.assertAlmostEqual(SubperiodInt(nr / sc, sc).to_nom().to_factor(t), f)
        self.assertAlmostEqual(SubperiodInt(nr / sc, sc).to_subperiod().to_factor(t), f)


class InstrumentTestCase(ExtTestCase):
    def test_relationships(self) -> None:
        self.assertEqual(rel((5000, 7000, 6000, 3000), 1000000), Rel.INDEP)
        self.assertEqual(rel((5000, 7000, 6000, 3000), 7000), Rel.MEX)
        self.assertEqual(rel((5000, 7000, 6000, 3000), 10000), Rel.REL)

    def test_combinations(self) -> None:
        self.assertEqual(ilen(rel_combinations((5000, 7000, 6000, 3000), 10000)), 8)

    def test_projects(self) -> None:
        self.assertAlmostEqual(pw(Project(-20000, 4000, 4000 - 1000, 10).cash_flows(), EfInt(0.05)), 5620.857801717468)
        self.assertAlmostEqual(aw(Project(-20000, 4000, 4000 - 1000, 10).cash_flows(), EfInt(0.05)), 727.9268005526942)


class CashFlowTestCase(TestCase):
    def test_payback_period(self) -> None:
        self.assertAlmostEqual(payback((), 0), 0)
        self.assertAlmostEqual(payback((), 10), inf)
        self.assertAlmostEqual(payback((CashFlow(0, 100), CashFlow(1, 200), CashFlow(2, 300)), 450), 1.5)


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
        e, p, t = EfInt(0.034), 100000, 4

        self.assertAlmostEqual(e.to_nom(2).rate, 0.03371581102178567)
        self.assertAlmostEqual(e.to_nom(12).rate, 0.033481397886386155)
        self.assertAlmostEqual(e.to_nom(365).rate, 0.03343630748129267)
        self.assertAlmostEqual(e.to_cont().rate, 0.03343477608623742)

        self.assertAlmostEqual(p * e.to_nom(2).to_factor(t), p * e.to_nom(12).to_factor(t))
        self.assertAlmostEqual(p * e.to_nom(12).to_factor(t), p * e.to_nom(365).to_factor(t))
        self.assertAlmostEqual(p * e.to_nom(365).to_factor(t), p * e.to_cont().to_factor(t))
        self.assertAlmostEqual(p * e.to_cont().to_factor(t), 114309.4552336)

    def test_5(self) -> None:
        fv, c, cd = 100, 0.023, 0.02

        self.assertAlmostEqual(ContInt(c).to_ef().rate, 0.02326653954721758)
        self.assertAlmostEqual(fv / ContInt(c).to_factor(0.5), 98.8565872247913)
        self.assertAlmostEqual(fv / ContInt(c).to_factor(0.75), 98.28979294344309)
        self.assertAlmostEqual(fv / ContInt(cd).to_factor(0.5), 99.0049833749168)
        self.assertAlmostEqual(fv / ContInt(cd).to_factor(0.75), 98.51119396030627)

    def test_6(self) -> None:
        self.assertAlmostEqual(EfInt(0.08).to_subperiod(12).rate, 0.00643403011000343)
        self.assertAlmostEqual(NomInt(0.035, 252).to_ef().rate, 0.03561719190449408)
        self.assertAlmostEqual(NomInt(0.04, 4).to_cont().rate, 0.039801323412672354)
        self.assertAlmostEqual(CompInt.from_factor(SubperiodInt(0.015, 12).to_factor(1), 4).to_cont().rate,
                               0.04466583748125169)
        self.assertAlmostEqual(CompInt.from_factor(CompInt.from_factor(
            NomInt(0.012, 3).to_factor(1), 1 / 4).to_factor(3), 1).to_nom(6).rate, 0.1454477030768886)


class PS2TestCase(ExtTestCase):
    def test_1(self) -> None:
        factor = NomInt(0.15, 4).to_factor(4 / 12) * ContInt(0.11).to_factor(5 / 12)

        self.assertAlmostEqual(CompInt.from_factor(factor, 9 / 12).rate, 0.134915472328168)

    def test_2(self) -> None:
        p, i, n = 100, 0.05, 10

        self.assertAlmostEqual(p * pa(i, n), p * ((1 + i) ** n - 1) / (i * (1 + i) ** n))

    def test_3(self) -> None:
        cases = (
            (1, 99.52, 0.05943811, 0.05773868),
            (4, 99.01, 0.03029791, 0.02984799),
            (8, 97.64, 0.03647384, 0.03582441),
            (12, 95.85, 0.04329682, 0.04238572),
        )

        for m, p, a, b in cases:
            self.assertAlmostEqual(newton(lambda y: p * EfInt(y).to_factor(m / 12) - 100, 0), a)
            self.assertAlmostEqual(newton(lambda y: p * ContInt(y).to_factor(m / 12) - 100, 0), b)

        self.assertAlmostEqual(interp(7, 4, 8, 0.03029791, 0.03647384), 0.0349298575)
        self.assertAlmostEqual(interp(7, 4, 8, 0.02984799, 0.03582441), 0.034330305)

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
            t: newton(lambda y: p * ContInt(y).to_factor(t / 12) - 100, 0)
            for t, p in data.items()
        }

        r[4] = interp(4, 2, 6, r[2], r[6])
        r[5.5] = interp(5.5, 2, 6, r[2], r[6])
        r[7] = interp(7, 6, 9, r[6], r[9])
        r[10] = interp(10, 9, 12, r[9], r[12])

        self.assertAlmostEqual(100 * ContInt(r[2]).to_factor(-1. / 12), 99.55400544428134)
        self.assertAlmostEqual(100 * ContInt(r[4]).to_factor(-4. / 12), 98.68531340424114)
        self.assertAlmostEqual(100 * ContInt(r[5.5]).to_factor(-5.5 / 12), 98.66834503291024)
        self.assertAlmostEqual(100 * ContInt(r[7]).to_factor(-7 / 12), 98.18488742486127)
        self.assertAlmostEqual(100 * ContInt(r[10]).to_factor(-10 / 12), 96.54750684004732)
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
        i1 = NomInt(0.02, 2)
        i2 = NomInt(0.04, 2)
        p = m.payment(i1)

        self.assertAlmostEqual(p, 10145.891129693951)
        self.assertAlmostEqual(p * 12 * 3, 365252.08066898223)
        self.assertAlmostEqual(m.pay(5, i1).payment(i2), 12128.043601452593)

    def test_2(self) -> None:
        i = NomInt(0.07, 2)

        self.assertAlmostEqual(pw(Bond(100, 0, 2, 3 / 12).cash_flows(), i), 98.2946374365981)
        self.assertAlmostEqual(pw(Bond(100, 0, 2, 5 / 12).cash_flows(), i), 97.17391685967232)
        self.assertAlmostEqual(pw(Bond(100, 0, 2, 3).cash_flows(), i), 81.35006443077528)
        self.assertAlmostEqual(pw(Bond.from_rate(100, 0.04, 2, 3).cash_flows(), i), 92.00717047033226)
        self.assertAlmostEqual(pw(Bond.from_rate(100, 0.06, 2, 3.25).cash_flows(), i), 95.94840994600501)

    def test_3(self) -> None:
        self.assertAlmostEqual(newton(
            lambda y: pw(Bond.from_rate(100, 0.07, 2, 3).cash_flows(), NomInt(y, 2)) - 100, 0.1), 0.07)
        self.assertAlmostEqual(pw(Bond.from_rate(100, 0.04, 2, 3).cash_flows(), NomInt(0.05, 2)) + 100 * 0.04 / 2,
                               99.24593731921009)
        self.assertAlmostEqual(newton(
            lambda y: pw(Bond.from_rate(100, 0.03, 2, 2.25).cash_flows(), NomInt(y, 2)) - 100, 0.1,
        ), 0.026754568040623247)
        self.assertAlmostEqual(pw(Bond.from_rate(100, 0.07, 2, 2.25).cash_flows(), NomInt(0.05, 2)), 102.65033622528411)
        self.assertAlmostEqual(newton(
            lambda c: pw(Bond.from_rate(100, c, 2, 2.25).cash_flows(), NomInt(0.03, 2)) - 114, 0.1,
        ), 0.10627047075771787)

    def test_4(self) -> None:
        pass

    def test_5(self) -> None:
        y = newton(
            lambda y_: pw(Bond.from_rate(100, 0.07, 2, 7.5).cash_flows(), NomInt(y_, 2)) * fp(y_ / 2, 0.5) - 108, 0.1,
        )
        b: Callable[[float], float] = lambda cr: pw(Bond.from_rate(1000, cr, 2, 9).cash_flows(), NomInt(y, 2))

        cur_cr = ceil(newton(lambda cr: 9500000 / 2 - (4400 * b(cr)), 0.1) / 0.0025) * 0.0025
        self.assertAlmostEqual(cur_cr, 0.0725)
        self.assertAlmostEqual(4400 * b(cur_cr), 4802235.185695931)

        cur_cr = ceil(newton(lambda cr: 9500000 / 2 / (1 - 0.008) - (4400 * b(cr)), 0.1) / 0.0025) * 0.0025
        self.assertAlmostEqual(cur_cr, 0.0725)
        self.assertAlmostEqual(4400 * b(cur_cr) * (1 - 0.008), 4763817.304210364)

    def test_6(self) -> None:
        i = NomInt(0.060755, 2)

        self.assertAlmostEqual(Mortgage.from_down(500000, 50000).payment(i), 2899.3558026129626)
        self.assertAlmostEqual(Mortgage.from_down(500000, 50000).pay(3, i, 700).payment(i), 3490.3113416458878)
        self.assertLess(Mortgage.from_down(500000, 50000, 25).pay(3, i).principal,
                        Mortgage.from_down(500000, 50000, 25).pay(3, i, 700).principal)


class PS6TestCase(ExtTestCase):
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

        irrs = tuple(map(lambda d: irr(Project(d[0], 0, d[1], d[2]).cash_flows(), EfInt(0)).rate, data))

        self.assertSequenceAlmostEqual(irrs, (
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

        self.assertAlmostEqual(de_facto_marr((-data[i][0] for i in range(len(data))), irrs, 100000), 0.2178733729868983)

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


class PS7TestCase(ExtTestCase):
    def test_1(self) -> None:
        basis, salvage, life = 92000, 19000, 4

        self.assertIterableAlmostEqual(StrLineDeprec(basis, salvage, life).books, (92000, 73750, 55500, 37250, 19000))
        self.assertIterableAlmostEqual(DeclBalDeprec(basis, salvage, life).books,
                                       (92000, 62019.64424847585, 41809.08992073374, 28184.618296048306, 19000))
        self.assertIterableAlmostEqual(DeclBalDeprec.from_rate(basis, life, 0.25).books,
                                       (92000, 69000, 51750, 38812.5, 29109.375))
        self.assertIterableAlmostEqual(DblDeclBalDeprec(basis, salvage, life).books,
                                       (92000, 46000, 23000, 11500, 5750))
        self.assertIterableAlmostEqual(SYDDeprec(basis, salvage, life).books, (92000, 62800, 40900, 26300, 19000))
        self.assertIterableAlmostEqual(UPDeprec(basis, salvage, (37000, 37000, 32000, 30000)).books,
                                       (92000, 72139.70588235295, 52279.41176470589, 35102.94117647059, 19000))

    def test_2(self) -> None:
        basis, salvage, life, t = 210000, 10000, 20, 6

        self.assertAlmostEqual(StrLineDeprec(basis, salvage, life).book(t), 150000)
        self.assertAlmostEqual(DeclBalDeprec(basis, salvage, life).book(t), 84246.81795174461)
        self.assertAlmostEqual(DeclBalDeprec.from_rate(basis, life, 0.2).book(t), 55050.24)
        self.assertAlmostEqual(DblDeclBalDeprec(basis, salvage, life).book(t), 111602.61)

        self.assertAlmostEqual(StrLineDeprec(basis, salvage, life).amount(t), 10000)
        self.assertAlmostEqual(DeclBalDeprec(basis, salvage, life).amount(t), 13852.157371177402)
        self.assertAlmostEqual(DeclBalDeprec.from_rate(basis, life, 0.2).amount(t), 13762.56)
        self.assertAlmostEqual(DblDeclBalDeprec(basis, salvage, life).amount(t), 12400.29)

    def test_3(self) -> None:
        basis, life, t, book = 145000, 8, 6, 57000

        self.assertAlmostEqual(newton(lambda x: StrLineDeprec(basis, x, life).book(6) - book, 0), 27666.66666666667)
        self.assertAlmostEqual(newton(lambda x: DeclBalDeprec(basis, x, life).book(6) - book, 0), 41755.1908917986)

    def test_4(self) -> None:
        basis, salvage, life = 110000, 25000, 4

        self.assertIterableAlmostEqual(StrLineDeprec(basis, salvage, life).books, (110000, 88750, 67500, 46250, 25000))
        self.assertIterableAlmostEqual(DeclBalDeprec(basis, salvage, life).books,
                                       (110000, 75950.3039160202, 52440.44240850757, 36207.88671287913, 25000))
        self.assertIterableAlmostEqual(DeclBalDeprec.from_rate(basis, life, 0.35).books,
                                       (110000, 71500, 46475, 30208.75, 19635.6875))
        self.assertIterableAlmostEqual(DblDeclBalDeprec(basis, salvage, life).books,
                                       (110000, 55000, 27500, 13750, 6875))
        self.assertIterableAlmostEqual(SYDDeprec(basis, salvage, life).books, (110000, 76000, 50500, 33500, 25000))
        self.assertIterableAlmostEqual(UPDeprec(basis, salvage, (80000, 65000, 50000, 35000)).books,
                                       (110000, 80434.78260869565, 56413.043478260865, 37934.78260869565, 25000))

    def test_5(self) -> None:
        basis, salvage, life, t1, t2 = 23000, 4000, 7, 4, 5

        self.assertAlmostEqual(StrLineDeprec(basis, salvage, life).book(t1), 12142.857142857143)
        self.assertAlmostEqual(DeclBalDeprec(basis, salvage, life).book(t1), 8465.096723059049)
        self.assertAlmostEqual(SYDDeprec(basis, salvage, life).book(t1), 8071.4285714285725)
        self.assertAlmostEqual(UPDeprec(basis, salvage, (50, 60, 40, 20, 10, 15, 5)).book(t1), 6850)

        self.assertAlmostEqual(StrLineDeprec(basis, salvage, life).amount(t2), 2714.285714285714)
        self.assertAlmostEqual(DeclBalDeprec(basis, salvage, life).amount(t2), 1871.7191438152927)
        self.assertAlmostEqual(SYDDeprec(basis, salvage, life).amount(t2), 2035.7142857142856)
        self.assertAlmostEqual(UPDeprec(basis, salvage, (50, 60, 40, 20, 10, 15, 5)).amount(t2), 950)

    def test_6(self) -> None:
        basis, salvage, life, t = 2500000, 200000, 10, 4

        self.assertAlmostEqual(StrLineDeprec(basis, salvage, life).book(t), 1580000)
        self.assertAlmostEqual(DeclBalDeprec(basis, salvage, life).book(t), 910282.1015130404)
        self.assertAlmostEqual(DblDeclBalDeprec(basis, salvage, life).book(t), 1024000)
        self.assertAlmostEqual(SYDDeprec(basis, salvage, life).book(t), 1078181.8181818182)

        self.assertAlmostEqual(StrLineDeprec(basis, salvage, life).amount(t), 230000)
        self.assertAlmostEqual(DeclBalDeprec(basis, salvage, life).amount(t), 261554.3542830096)
        self.assertAlmostEqual(DblDeclBalDeprec(basis, salvage, life).amount(t), 256000)
        self.assertAlmostEqual(SYDDeprec(basis, salvage, life).amount(t), 292727.2727272727)

    def test_7(self) -> None:
        deprec = DeclBalDeprec.from_rate(5000, 5, 0.15)

        self.assertAlmostEqual(deprec.cap_gain(3000), 0)
        self.assertAlmostEqual(deprec.recap_deprec(3000), 781.4734375)
        self.assertAlmostEqual(deprec.loss_on_disp(3000), 0)

        self.assertAlmostEqual(deprec.cap_gain(2000), 0)
        self.assertAlmostEqual(deprec.recap_deprec(2000), 0)
        self.assertAlmostEqual(deprec.loss_on_disp(2000), 218.5265625)

        self.assertAlmostEqual(deprec.cap_gain(6000), 1000)
        self.assertAlmostEqual(deprec.recap_deprec(6000), 2781.4734375)
        self.assertAlmostEqual(deprec.loss_on_disp(6000), 0)


if __name__ == '__main__':
    main()
