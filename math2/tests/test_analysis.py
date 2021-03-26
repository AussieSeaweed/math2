from math import cos, pi, sin
from operator import mul, pos
from unittest import main

from auxiliary import ExtendedTestCase

from math2.analysis import (MidpointIntegrator, SimpsonIntegrator, TrapezoidIntegrator, double_integrate, integrate,
                            triple_integrate)
from math2.linear import vector


class IntegratorsTestCase(ExtendedTestCase):
    def test_integrate(self) -> None:
        self.assertAlmostEqual(integrate(
            lambda x: x ** 2, -1, 1, steps=100, integrator=MidpointIntegrator()), 2 / 3, 3)
        self.assertAlmostEqual(integrate(
            lambda x: x ** 2, -1, 1, steps=100, integrator=TrapezoidIntegrator()), 2 / 3, 3)
        self.assertAlmostEqual(integrate(lambda x: x ** 2, -1, 1, steps=100, integrator=SimpsonIntegrator()), 2 / 3)
        self.assertAlmostEqual(integrate(sin, 0, 2 * pi, steps=100, integrator=MidpointIntegrator()), 0)
        self.assertAlmostEqual(integrate(sin, 0, 2 * pi, steps=100, integrator=TrapezoidIntegrator()), 0)
        self.assertAlmostEqual(integrate(sin, 0, 2 * pi, steps=100, integrator=SimpsonIntegrator()), 0)

        self.assertIterableAlmostEqual(
            integrate(lambda x: vector((0, 2 * x, 3 * x ** 2)), -1, 1, steps=100), vector((0, 0, 2)))

    def test_double_integrate(self) -> None:
        self.assertAlmostEqual(double_integrate(
            lambda x, y: x * y ** 2, 0, 1, lambda x: 0, pos, steps=100, integrator=MidpointIntegrator()), 1 / 15, 3)
        self.assertAlmostEqual(double_integrate(
            lambda x, y: x * y ** 2, 0, 1, lambda x: 0, pos, steps=100, integrator=TrapezoidIntegrator()), 1 / 15, 3)
        self.assertAlmostEqual(double_integrate(
            lambda x, y: x * y ** 2, 0, 1, lambda x: 0, pos, steps=100, integrator=SimpsonIntegrator()), 1 / 15)
        self.assertAlmostEqual(double_integrate(
            lambda x, y: x ** 2 * y, 0, 1, lambda x: 0, pos, steps=100, integrator=MidpointIntegrator()), 0.1, 4)
        self.assertAlmostEqual(double_integrate(
            lambda x, y: x ** 2 * y, 0, 1, lambda x: 0, pos, steps=100, integrator=TrapezoidIntegrator()), 0.1, 4)
        self.assertAlmostEqual(double_integrate(
            lambda x, y: x ** 2 * y, 0, 1, lambda x: 0, pos, steps=100, integrator=SimpsonIntegrator()), 0.1)

        self.assertIterableAlmostEqual(double_integrate(
            lambda x, y: vector((2 * y, 2 * x + y ** 2, 3 * x * y)), -10, 1, lambda x: -2 * x, lambda x: x, steps=100,
        ), vector((-1001, -5497.25, 11248.875)))

    def test_triple_integrate(self) -> None:
        self.assertAlmostEqual(triple_integrate(
            lambda x, y, z: sin(x) * cos(y) * z, -5, 1, lambda x: -10, pos, lambda x, y: -x * y * 2, mul,
            steps=50, integrator=MidpointIntegrator(),
        ), 1289.4240604730014, -1)
        self.assertAlmostEqual(triple_integrate(
            lambda x, y, z: sin(x) * cos(y) * z, -5, 1, lambda x: -10, pos, lambda x, y: -x * y * 2, mul,
            steps=50, integrator=TrapezoidIntegrator(),
        ), 1289.4240604730014, -1)
        self.assertAlmostEqual(triple_integrate(
            lambda x, y, z: sin(x) * cos(y) * z, -5, 1, lambda x: -10, pos, lambda x, y: -x * y * 2, mul,
            steps=50, integrator=SimpsonIntegrator(),
        ), 1289.4240604730014, 3)

        self.assertIterableAlmostEqual(triple_integrate(
            lambda x, y, z: vector((1 ** (x * y * z), x + y + z, x * y * z)),
            -1, 2, lambda x: -x, lambda x: 2 * x, lambda x, y: -x * y, lambda x, y: 2 * x * y,
            steps=10,
        ), vector((16.875, 136.35, 179.296875)), 0)


if __name__ == '__main__':
    main()
