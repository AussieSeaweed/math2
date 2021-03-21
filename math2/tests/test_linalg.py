from functools import partial
from itertools import repeat
from math import pi, sin, sqrt
from operator import add, matmul, mul
from unittest import main

from auxiliary import ExtendedTestCase

from math2.linalg import (DimensionError, Matrix, angle_between, column, cross, diagonal, i, identity, j, k, norm, ones,
                          project, random, row, singleton, unit, zeros)


class LinAlgTestCase(ExtendedTestCase):
    def test_abs(self) -> None:
        self.assertAlmostEqual(abs(Matrix((range(3), range(3, 6)))), 7.416198487095663)
        self.assertAlmostEqual(abs(row(range(6))), 7.416198487095663)
        self.assertAlmostEqual(abs(column(range(6))), 7.416198487095663)

    def test_iter(self) -> None:
        self.assertEqual(Matrix((range(3), range(3, 6))), range(6))
        self.assertEqual(row(range(6)), range(6))
        self.assertEqual(column(range(6)), range(6))

    def test_getitem(self) -> None:
        self.assertEqual(Matrix((range(3), range(3, 6)))[4], 4)
        self.assertEqual(row(range(6))[4], 4)
        self.assertEqual(column(range(6))[4], 4)

        self.assertIterableEqual(Matrix((range(3), range(3, 6)))[2:5], range(2, 5))
        self.assertIterableEqual(row(range(6))[2:5], range(2, 5))
        self.assertIterableEqual(column(range(6))[2:5], range(2, 5))

        self.assertIterableEqual(Matrix((range(3), range(3, 6)))[::-1], reversed(range(6)))
        self.assertIterableEqual(row(range(6))[::-1], reversed(range(6)))
        self.assertIterableEqual(column(range(6))[::-1], reversed(range(6)))

        self.assertEqual(Matrix((range(3), range(3, 6)))[1, 1], 4)
        self.assertEqual(row(range(6))[0, 4], 4)
        self.assertEqual(column(range(6))[4, 0], 4)

        self.assertEqual(Matrix((range(3), range(3, 6)))[:, :], Matrix((range(3), range(3, 6))))
        self.assertEqual(row(range(6))[:, :], row(range(6)))
        self.assertEqual(column(range(6))[:, :], column(range(6)))

        self.assertEqual(Matrix((range(3), range(3, 6)))[:, :2], Matrix((range(2), range(3, 5))))
        self.assertEqual(row(range(6))[0, :], row(range(6)))
        self.assertEqual(column(range(6))[:, 0], column(range(6)))

    def test_len(self) -> None:
        self.assertEqual(len(Matrix((range(3), range(3, 6)))), 6)
        self.assertEqual(len(row(range(6))), 6)
        self.assertEqual(len(column(range(6))), 6)

    def test_pos(self) -> None:
        self.assertEqual(+Matrix((range(3), range(3, 6))), Matrix((range(3), range(3, 6))))
        self.assertEqual(+row(range(6)), row(range(6)))
        self.assertEqual(+column(range(6)), column(range(6)))

    def test_neg(self) -> None:
        self.assertEqual(-Matrix((range(3), range(3, 6))), Matrix((range(0, -3, -1), range(-3, -6, -1))))
        self.assertEqual(-row(range(6)), Matrix((range(0, -6, -1),)))
        self.assertEqual(-column(range(6)), Matrix((-x,) for x in range(6)))

    def test_add(self) -> None:
        self.assertEqual(Matrix((range(3), range(3, 6))) + Matrix((range(6, 9), range(9, 12))),
                         Matrix(((6, 8, 10), (12, 14, 16))))
        self.assertEqual(row(range(5, -1, -1)) + row(range(6)), row(repeat(5, 6)))
        self.assertEqual(column(range(5, -1, -1)) + column(range(6)), column(repeat(5, 6)))
        self.assertRaises(TypeError, add, row(range(5)), 5)
        self.assertRaises(DimensionError, add, row(range(5)), column(range(5)))
        self.assertRaises(DimensionError, add, row(range(5)), row(range(6)))

    def test_mul(self) -> None:
        self.assertEqual(Matrix((range(3), range(3, 6))) * 5, Matrix((range(0, 15, 5), range(15, 30, 5))))
        self.assertEqual(row(range(5, -1, -1)) * 5, row(range(25, -1, -5)))
        self.assertEqual(column(range(5, -1, -1)) * 5, column(range(25, -1, -5)))

        self.assertEqual(Matrix((range(3), range(3, 6))) * Matrix((range(2), range(2, 4), range(4, 6))),
                         Matrix(((10, 13), (28, 40))))
        self.assertEqual(row(range(5, -1, -1)) * column(range(6)), singleton(20))
        self.assertEqual(column(range(6)) * row(range(6)), Matrix((
            repeat(0, 6), range(6), range(0, 12, 2), range(0, 18, 3), range(0, 24, 4), range(0, 30, 5),
        )))
        self.assertRaises(DimensionError, mul, row(range(5)), row(range(5)))
        self.assertRaises(DimensionError, mul, row(range(5)), column(range(6)))

    def test_rmul(self) -> None:
        self.assertEqual(5 * Matrix((range(3), range(3, 6))), Matrix((range(0, 15, 5), range(15, 30, 5))))
        self.assertEqual(5 * row(range(5, -1, -1)), row(range(25, -1, -5)))
        self.assertEqual(5 * column(range(5, -1, -1)), column(range(25, -1, -5)))

    def test_matmul(self) -> None:
        self.assertEqual(Matrix((range(3), range(3, 6))) @ Matrix((range(6, 9), range(9, 12))), 145)
        self.assertEqual(row(range(5, -1, -1)) @ row(range(6)), 20)
        self.assertEqual(column(range(5, -1, -1)) @ column(range(6)), 20)
        self.assertRaises(DimensionError, matmul, row(range(5)), column(range(5)))
        self.assertRaises(DimensionError, matmul, row(range(5)), row(range(6)))

    def test_transposed(self):
        self.assertEqual(Matrix((range(3), range(3, 6))) ** 'T', Matrix(((0, 3), (1, 4), (2, 5))))
        self.assertEqual(row(range(6)) ** 'T', column(range(6)))
        self.assertEqual(column(range(6)) ** 'T', row(range(6)))


class FactoryTestCase(ExtendedTestCase):
    def test_singleton(self):
        self.assertEqual(singleton(5), Matrix(((5,),)))
        self.assertEqual(singleton(0), Matrix(((0,),)))
        self.assertEqual(singleton(10), Matrix(((10,),)))

    def test_row(self):
        self.assertEqual(row(()), Matrix())
        self.assertEqual(row(range(10)), Matrix((range(10),)))
        self.assertEqual(row(map(partial(pow, 2), range(5))), Matrix(((1, 2, 4, 8, 16),)))

    def test_column(self):
        self.assertEqual(column(()), Matrix())
        self.assertEqual(column(range(10)), Matrix((x,) for x in range(10)))
        self.assertEqual(column(map(partial(pow, 2), range(5))), Matrix(((1,), (2,), (4,), (8,), (16,))))

    def test_diagonal(self):
        self.assertEqual(diagonal(()), Matrix())
        self.assertEqual(diagonal((1, 1, 1)), identity(3))
        self.assertEqual(diagonal(range(5)), Matrix((
            repeat(0, 5),
            (0, 1, 0, 0, 0),
            (0, 0, 2, 0, 0),
            (0, 0, 0, 3, 0),
            (0, 0, 0, 0, 4),
        )))

    def test_zeros(self):
        self.assertEqual(zeros(0), Matrix())
        self.assertEqual(zeros(5), Matrix((repeat(0, 5), repeat(0, 5), repeat(0, 5), repeat(0, 5), repeat(0, 5))))
        self.assertEqual(zeros(5, 5), Matrix((repeat(0, 5), repeat(0, 5), repeat(0, 5), repeat(0, 5), repeat(0, 5))))
        self.assertEqual(zeros(1, 5), row(repeat(0, 5)))
        self.assertEqual(zeros(5, 1), column(repeat(0, 5)))

    def test_ones(self):
        self.assertEqual(ones(0), Matrix())
        self.assertEqual(ones(5), Matrix((repeat(1, 5), repeat(1, 5), repeat(1, 5), repeat(1, 5), repeat(1, 5))))
        self.assertEqual(ones(5, 5), Matrix((repeat(1, 5), repeat(1, 5), repeat(1, 5), repeat(1, 5), repeat(1, 5))))
        self.assertEqual(ones(1, 5), row(repeat(1, 5)))
        self.assertEqual(ones(5, 1), column(repeat(1, 5)))

    def test_identity(self):
        self.assertEqual(identity(0), Matrix())
        self.assertEqual(identity(5), Matrix((
            (1, 0, 0, 0, 0),
            (0, 1, 0, 0, 0),
            (0, 0, 1, 0, 0),
            (0, 0, 0, 1, 0),
            (0, 0, 0, 0, 1),
        )))
        self.assertEqual(identity(5, 5), Matrix((
            (1, 0, 0, 0, 0),
            (0, 1, 0, 0, 0),
            (0, 0, 1, 0, 0),
            (0, 0, 0, 1, 0),
            (0, 0, 0, 0, 1),
        )))
        self.assertEqual(identity(1, 5), row((1, 0, 0, 0, 0)))
        self.assertEqual(identity(5, 1), column((1, 0, 0, 0, 0)))

    def test_random(self):
        self.assertEqual(random(5).dimensions, (5, 5))
        self.assertEqual(random(5, 1).dimensions, (5, 1))
        self.assertEqual(random(1, 5).dimensions, (1, 5))


class UtilTestCase(ExtendedTestCase):
    MONTE_CARLO_TEST_COUNT = 100

    def test_norm(self):
        self.assertAlmostEqual(norm(row((1 / sqrt(2), 1 / sqrt(2)))), 1)
        self.assertAlmostEqual(norm(column((1, 0, 0))), 1)
        self.assertAlmostEqual(norm(identity(5, 10)), abs(identity(5, 10)))

    def test_angle_between(self):
        self.assertAlmostEqual(angle_between(row((1, 0)), row((0, 10))), pi / 2)
        self.assertAlmostEqual(angle_between(row((1, 0)), row((1000, 0))), 0)
        self.assertAlmostEqual(angle_between(row((1, 0)), row((-1000, 0))), pi)

    def test_unit(self):
        self.assertIterableAlmostEqual(unit(row((1, 1))), row((1 / sqrt(2), 1 / sqrt(2))))
        self.assertIterableAlmostEqual(unit(row((100, 0))), row((1, 0)))

    def test_project(self):
        self.assertIterableAlmostEqual(project(row((1, 1, 1)), i), row((1, 0, 0)))
        self.assertIterableAlmostEqual(project(row((100, 100, 100)), i), row((100, 0, 0)))
        self.assertIterableAlmostEqual(project(row((100, 100, 100)), j), row((0, 100, 0)))
        self.assertIterableAlmostEqual(project(row((100, 100, 100)), k), row((0, 0, 100)))

    def test_cross(self):
        self.assertIterableAlmostEqual(cross(i, j), k)
        self.assertIterableAlmostEqual(cross(j, i), -k)
        self.assertIterableAlmostEqual(cross(i, k), -j)
        self.assertIterableAlmostEqual(cross(k, i), j)
        self.assertIterableAlmostEqual(cross(j, k), i)
        self.assertIterableAlmostEqual(cross(k, j), -i)

        for _ in range(self.MONTE_CARLO_TEST_COUNT):
            u, v = random(1, 3), random(1, 3)

            self.assertAlmostEqual(abs(cross(u, v)), abs(u) * abs(v) * sin(angle_between(u, v)))


if __name__ == '__main__':
    main()
