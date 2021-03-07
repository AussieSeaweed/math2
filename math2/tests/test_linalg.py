from unittest import main

from auxiliary import ExtendedTestCase

from math2.linalg import Vector, full, ones, replaced, zeros


class VectorTestCase(ExtendedTestCase):
    def test_init(self) -> None:
        self.assertIterableAlmostEqual(Vector(range(10)), range(10))

        self.assertIterableAlmostEqual(zeros(10), (0,) * 10)
        self.assertIterableAlmostEqual(ones(10), (1,) * 10)
        self.assertIterableAlmostEqual(full(10, 1 / 3), (1 / 3,) * 10)
        self.assertIterableAlmostEqual(replaced(ones(10), 5, 0), (1,) * 5 + (0,) + (1,) * 4)

    def test_ops(self) -> None:
        a, b = Vector(range(10)), Vector(range(10))

        self.assertIterableAlmostEqual(+a, a)
        self.assertIterableAlmostEqual(-a, (-x for x in range(10)))

        self.assertIterableAlmostEqual(a + b, (x + x for x in range(10)))
        self.assertIterableAlmostEqual(a - b, zeros(10))
        self.assertIterableAlmostEqual(a * 3, (x * 3 for x in range(10)))
        self.assertIterableAlmostEqual(3 * a, (3 * x for x in range(10)))
        self.assertIterableAlmostEqual(a / 3, (x / 3 for x in range(10)))
        self.assertAlmostEqual(a @ b, sum(x * x for x in range(10)))

        a += b
        self.assertIterableAlmostEqual(a, (x + x for x in range(10)))
        a -= b
        self.assertIterableAlmostEqual(a, b)
        a *= 3
        self.assertIterableAlmostEqual(a, (x * 3 for x in range(10)))
        a /= 3
        self.assertIterableAlmostEqual(a, range(10))

        self.assertRaises(ValueError, a.__add__, Vector(range(5)))
        self.assertRaises(ValueError, a.__sub__, Vector(range(5)))


if __name__ == '__main__':
    main()
