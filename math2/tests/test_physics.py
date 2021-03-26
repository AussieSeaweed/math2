from itertools import repeat
from math import sqrt
from unittest import main

from auxiliary import ExtendedTestCase

from math2.linear import vector, zero_vector
from math2.physics import DiscreteCharge, ElectrostaticField


class PS1TestCase(ExtendedTestCase):
    def test_1(self) -> None:
        field = ElectrostaticField()
        field.charges = [DiscreteCharge(vector((0, 0)), 1)]
        a = abs(field.force(DiscreteCharge(vector((1, 0)), 1)))
        field.charges = [DiscreteCharge(vector((0, 0)), 2)]
        b = abs(field.force(DiscreteCharge(vector((1, -1)), -2)))
        self.assertLess(a, b)

    def test_2(self) -> None:
        field = ElectrostaticField()
        field.charges = [DiscreteCharge(vector((0, 0)), 2), DiscreteCharge(vector((0.5, sqrt(1 - 0.5 ** 2))), -1)]
        e = field.intensity(vector((1, 0)))
        self.assertGreater(e[0], 0)
        self.assertGreater(e[1], 0)
        self.assertLess(e[1], e[0])

    def test_3(self) -> None:
        q, a = -1e-9, 1
        field = ElectrostaticField()
        field.charges = [
            DiscreteCharge(vector((a, 0, 0)), q),
            DiscreteCharge(vector((0, a, 0)), q),
            DiscreteCharge(vector((0, 0, a)), q),
        ]
        self.assertIterableAlmostEqual(field.intensity(zero_vector(3)), repeat(8.987551792261172, 3))
        self.assertIterableAlmostEqual(field.intensity(vector((0, 0, 100))), (0, 0, -0.0027142443154663546), 4)


if __name__ == '__main__':
    main()
