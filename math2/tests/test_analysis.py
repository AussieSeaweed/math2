from math import cos, pi, sin
from operator import mul
from unittest import main

from auxiliary import ExtendedTestCase

from math2.analysis import MidpointIntegrator, SimpsonIntegrator, TrapezoidIntegrator, dbl_quad, quad, tpl_quad


class MiscTestCase(ExtendedTestCase):
    def test_quad(self):
        self.assertAlmostEqual(MidpointIntegrator().quad(lambda x: x ** 2, -1, 1, 100), 2 / 3, 3)
        self.assertAlmostEqual(TrapezoidIntegrator().quad(lambda x: x ** 2, -1, 1, 100), 2 / 3, 3)
        self.assertAlmostEqual(SimpsonIntegrator().quad(lambda x: x ** 2, -1, 1, 100), 2 / 3)
        self.assertAlmostEqual(quad(lambda x: x ** 2, -1, 1), 2 / 3)
        self.assertAlmostEqual(MidpointIntegrator().quad(sin, 0, 2 * pi, 100), 0)
        self.assertAlmostEqual(TrapezoidIntegrator().quad(sin, 0, 2 * pi, 100), 0)
        self.assertAlmostEqual(SimpsonIntegrator().quad(sin, 0, 2 * pi, 100), 0)
        self.assertAlmostEqual(quad(sin, 0, 2 * pi), 0)

    def test_dbl_quad(self):
        self.assertAlmostEqual(
            MidpointIntegrator().dbl_quad(lambda x, y: x * y ** 2, 0, 1, 0, lambda x: x, 100), 1 / 15, 3)
        self.assertAlmostEqual(
            TrapezoidIntegrator().dbl_quad(lambda x, y: x * y ** 2, 0, 1, 0, lambda x: x, 100), 1 / 15, 3)
        self.assertAlmostEqual(
            SimpsonIntegrator().dbl_quad(lambda x, y: x * y ** 2, 0, 1, 0, lambda x: x, 100), 1 / 15)
        self.assertAlmostEqual(dbl_quad(lambda x, y: x * y ** 2, 0, 1, 0, lambda x: x), 1 / 15)
        self.assertAlmostEqual(
            MidpointIntegrator().dbl_quad(lambda x, y: x ** 2 * y, 0, 1, 0, lambda x: x, 100), 0.1, 4)
        self.assertAlmostEqual(
            TrapezoidIntegrator().dbl_quad(lambda x, y: x ** 2 * y, 0, 1, 0, lambda x: x, 100), 0.1, 4)
        self.assertAlmostEqual(
            SimpsonIntegrator().dbl_quad(lambda x, y: x ** 2 * y, 0, 1, 0, lambda x: x, 100), 0.1)
        self.assertAlmostEqual(dbl_quad(lambda x, y: x ** 2 * y, 0, 1, 0, lambda x: x), 0.1)

    def test_tpl_quad(self):
        # self.assertAlmostEqual(MidpointIntegrator().tpl_quad(
        #     lambda x, y, z: sin(x) * cos(y) * z,
        #     -5, 1,
        #     -10, lambda x: x,
        #     lambda x, y: -x * y * 2, mul,
        #     50,
        # ), 1289.4240604730014)
        # self.assertAlmostEqual(TrapezoidIntegrator().tpl_quad(
        #     lambda x, y, z: sin(x) * cos(y) * z,
        #     -5, 1,
        #     -10, lambda x: x,
        #     lambda x, y: -x * y * 2, mul,
        #     50,
        # ), 1289.4240604730014)
        # self.assertAlmostEqual(SimpsonIntegrator().tpl_quad(
        #     lambda x, y, z: sin(x) * cos(y) * z,
        #     -5, 1,
        #     -10, lambda x: x,
        #     lambda x, y: -x * y * 2, mul,
        #     50,
        # ), 1289.4240604730014)
        self.assertAlmostEqual(tpl_quad(
            lambda x, y, z: sin(x) * cos(y) * z,
            -5, 1,
            -10, lambda x: x,
            lambda x, y: -x * y * 2, mul,
        ), 1289.4240604730014)


if __name__ == '__main__':
    main()
