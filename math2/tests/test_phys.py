from itertools import repeat
from math import sqrt
from unittest import main

from auxiliary import ExtendedTestCase

from math2.linear import row, zeros
from math2.phys import DiscreteCharge, ElectricField


class PS1TestCase(ExtendedTestCase):
    def test_1(self):
        field = ElectricField()
        field.charges = DiscreteCharge(row((0, 0)), 1),
        a = abs(field.force(DiscreteCharge(row((1, 0)), 1)))
        field.charges = DiscreteCharge(row((0, 0)), 2),
        b = abs(field.force(DiscreteCharge(row((1, -1)), -2)))
        self.assertLess(a, b)

    def test_2(self):
        field = ElectricField()
        field.charges = DiscreteCharge(row((0, 0)), 2), DiscreteCharge(row((0.5, sqrt(1 - 0.5 ** 2))), -1)
        e = field.intensity(row((1, 0)))
        self.assertGreater(e[0], 0)
        self.assertGreater(e[1], 0)
        self.assertLess(e[1], e[0])

    def test_3(self):
        q, a = -1e-9, 1
        field = ElectricField()
        field.charges = (
            DiscreteCharge(row((a, 0, 0)), q),
            DiscreteCharge(row((0, a, 0)), q),
            DiscreteCharge(row((0, 0, a)), q),
        )
        self.assertIterableAlmostEqual(field.intensity(zeros(1, 3)), repeat(8.987551792261172, 3))
        self.assertIterableAlmostEqual(field.intensity(row((0, 0, 100))), (0, 0, -0.0027142443154663546), 4)


if __name__ == '__main__':
    main()
