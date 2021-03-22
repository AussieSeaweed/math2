from functools import partial
from math import pi, sin, sqrt
from operator import add, matmul, mul
from unittest import main

from auxiliary import ExtendedTestCase

from math2.linear import (DimensionError, angle, col, cols, cross, diag, empty, eye, full, i, j, k, norm, ones,
                          orthogonal, parallel, proj, random, row, rows, singleton, unit, zeros)


class MatrixTestCase(ExtendedTestCase):
    def test_abs(self):
        self.assertAlmostEqual(abs(rows((range(3), range(3, 6)))), 7.416198487095663)
        self.assertAlmostEqual(abs(row(range(6))), 7.416198487095663)
        self.assertAlmostEqual(abs(col(range(6))), 7.416198487095663)

    def test_iter(self):
        self.assertIterableEqual(rows((range(3), range(3, 6))), range(6))
        self.assertIterableEqual(row(range(6)), range(6))
        self.assertIterableEqual(col(range(6)), range(6))

    def test_getitem(self):
        self.assertEqual(rows((range(3), range(3, 6)))[4], 4)
        self.assertEqual(row(range(6))[4], 4)
        self.assertEqual(col(range(6))[4], 4)

        self.assertIterableEqual(rows((range(3), range(3, 6)))[2:5], range(2, 5))
        self.assertIterableEqual(row(range(6))[2:5], range(2, 5))
        self.assertIterableEqual(col(range(6))[2:5], range(2, 5))

        self.assertIterableEqual(rows((range(3), range(3, 6)))[::-1], reversed(range(6)))
        self.assertIterableEqual(row(range(6))[::-1], reversed(range(6)))
        self.assertIterableEqual(col(range(6))[::-1], reversed(range(6)))

        self.assertEqual(rows((range(3), range(3, 6)))[1, 1], 4)
        self.assertEqual(row(range(6))[0, 4], 4)
        self.assertEqual(col(range(6))[4, 0], 4)

        self.assertEqual(rows((range(3), range(3, 6)))[:, :], rows((range(3), range(3, 6))))
        self.assertEqual(row(range(6))[:, :], row(range(6)))
        self.assertEqual(col(range(6))[:, :], col(range(6)))

        self.assertEqual(rows((range(3), range(3, 6)))[:, :2], rows((range(2), range(3, 5))))
        self.assertEqual(row(range(6))[0, :], row(range(6)))
        self.assertEqual(col(range(6))[:, 0], col(range(6)))

    def test_len(self):
        self.assertEqual(len(rows((range(3), range(3, 6)))), 6)
        self.assertEqual(len(row(range(6))), 6)
        self.assertEqual(len(col(range(6))), 6)

    def test_pos(self):
        self.assertEqual(+rows((range(3), range(3, 6))), rows((range(3), range(3, 6))))
        self.assertEqual(+row(range(6)), row(range(6)))
        self.assertEqual(+col(range(6)), col(range(6)))

    def test_neg(self):
        self.assertEqual(-rows((range(3), range(3, 6))), rows((range(0, -3, -1), range(-3, -6, -1))))
        self.assertEqual(-row(range(6)), rows((range(0, -6, -1),)))
        self.assertEqual(-col(range(6)), rows(tuple((-x,) for x in range(6))))

    def test_add(self):
        self.assertEqual(rows((range(3), range(3, 6))) + rows((range(6, 9), range(9, 12))),
                         rows(((6, 8, 10), (12, 14, 16))))
        self.assertEqual(row(range(5, -1, -1)) + row(range(6)), row((5,) * 6))
        self.assertEqual(col(range(5, -1, -1)) + col(range(6)), col((5,) * 6))
        self.assertRaises(TypeError, add, row(range(5)), 5)
        self.assertRaises(DimensionError, add, row(range(5)), col(range(5)))
        self.assertRaises(DimensionError, add, row(range(5)), row(range(6)))

    def test_mul(self):
        self.assertEqual(rows((range(3), range(3, 6))) * 5, rows((range(0, 15, 5), range(15, 30, 5))))
        self.assertEqual(row(range(5, -1, -1)) * 5, row(range(25, -1, -5)))
        self.assertEqual(col(range(5, -1, -1)) * 5, col(range(25, -1, -5)))

        self.assertEqual(rows((range(3), range(3, 6))) * rows((range(2), range(2, 4), range(4, 6))),
                         rows(((10, 13), (28, 40))))
        self.assertEqual(row(range(5, -1, -1)) * col(range(6)), singleton(20))
        self.assertEqual(col(range(6)) * row(range(6)), rows((
            (0,) * 6, range(6), range(0, 12, 2), range(0, 18, 3), range(0, 24, 4), range(0, 30, 5),
        )))
        self.assertRaises(DimensionError, mul, row(range(5)), row(range(5)))
        self.assertRaises(DimensionError, mul, row(range(5)), col(range(6)))

    def test_rmul(self):
        self.assertEqual(5 * rows((range(3), range(3, 6))), rows((range(0, 15, 5), range(15, 30, 5))))
        self.assertEqual(5 * row(range(5, -1, -1)), row(range(25, -1, -5)))
        self.assertEqual(5 * col(range(5, -1, -1)), col(range(25, -1, -5)))

    def test_matmul(self):
        self.assertEqual(rows((range(3), range(3, 6))) @ rows((range(6, 9), range(9, 12))), 145)
        self.assertEqual(row(range(5, -1, -1)) @ row(range(6)), 20)
        self.assertEqual(col(range(5, -1, -1)) @ col(range(6)), 20)
        self.assertRaises(DimensionError, matmul, row(range(5)), col(range(5)))
        self.assertRaises(DimensionError, matmul, row(range(5)), row(range(6)))

    def test_transposed(self):
        self.assertEqual(rows((range(3), range(3, 6))) ** 'T', rows(((0, 3), (1, 4), (2, 5))))
        self.assertEqual(row(range(6)) ** 'T', col(range(6)))
        self.assertEqual(col(range(6)) ** 'T', row(range(6)))


class FactoryTestCase(ExtendedTestCase):
    def test_empty(self):
        self.assertEqual(empty().dims, (0, 0))

    def test_singleton(self):
        self.assertEqual(singleton(5), rows(((5,),)))
        self.assertEqual(singleton(0), rows(((0,),)))
        self.assertEqual(singleton(10), rows(((10,),)))

    def test_row(self):
        self.assertEqual(row(()).dims, (1, 0))
        self.assertEqual(row(range(10)), rows((range(10),)))
        self.assertEqual(row(tuple(map(partial(pow, 2), range(5)))), rows(((1, 2, 4, 8, 16),)))

    def test_col(self):
        self.assertEqual(col(()).dims, (0, 1))
        self.assertEqual(col(range(10)), rows(tuple((x,) for x in range(10))))
        self.assertEqual(col(tuple(map(partial(pow, 2), range(5)))), rows(((1,), (2,), (4,), (8,), (16,))))

    def test_rows(self):
        self.assertEqual(rows(((1, 2), (3, 6))).dims, (2, 2))

    def test_cols(self):
        self.assertEqual(cols(((1, 2), (3, 6))).dims, (2, 2))

    def test_diag(self):
        self.assertEqual(diag(()), empty())
        self.assertEqual(diag((1, 1, 1)), eye(3))
        self.assertEqual(diag(range(5)), rows((
            (0,) * 5,
            (0, 1, 0, 0, 0),
            (0, 0, 2, 0, 0),
            (0, 0, 0, 3, 0),
            (0, 0, 0, 0, 4),
        )))

    def test_zeros(self):
        self.assertEqual(zeros(0), empty())
        self.assertEqual(zeros(5), rows(((0,) * 5, (0,) * 5, (0,) * 5, (0,) * 5, (0,) * 5)))
        self.assertEqual(zeros(5, 5), rows(((0,) * 5, (0,) * 5, (0,) * 5, (0,) * 5, (0,) * 5)))
        self.assertEqual(zeros(1, 5), row((0,) * 5))
        self.assertEqual(zeros(5, 1), col((0,) * 5))

    def test_ones(self):
        self.assertEqual(ones(0), empty())
        self.assertEqual(ones(5), rows(((1,) * 5, (1,) * 5, (1,) * 5, (1,) * 5, (1,) * 5)))
        self.assertEqual(ones(5, 5), rows(((1,) * 5, (1,) * 5, (1,) * 5, (1,) * 5, (1,) * 5)))
        self.assertEqual(ones(1, 5), row((1,) * 5))
        self.assertEqual(ones(5, 1), col((1,) * 5))

    def test_eye(self):
        self.assertEqual(eye(0), empty())
        self.assertEqual(eye(5), rows((
            (1, 0, 0, 0, 0),
            (0, 1, 0, 0, 0),
            (0, 0, 1, 0, 0),
            (0, 0, 0, 1, 0),
            (0, 0, 0, 0, 1),
        )))
        self.assertEqual(eye(5, 5), rows((
            (1, 0, 0, 0, 0),
            (0, 1, 0, 0, 0),
            (0, 0, 1, 0, 0),
            (0, 0, 0, 1, 0),
            (0, 0, 0, 0, 1),
        )))
        self.assertEqual(eye(1, 5), row((1, 0, 0, 0, 0)))
        self.assertEqual(eye(5, 1), col((1, 0, 0, 0, 0)))

    def test_full(self):
        self.assertEqual(full(2, 1), cols(((1, 1), (1, 1))))
        self.assertEqual(full(2, 2, 1), cols(((1, 1), (1, 1))))

    def test_random(self):
        self.assertEqual(random(5).dims, (5, 5))
        self.assertEqual(random(5, 1).dims, (5, 1))
        self.assertEqual(random(1, 5).dims, (1, 5))


class UtilTestCase(ExtendedTestCase):
    MONTE_CARLO_TEST_COUNT = 10

    def test_norm(self):
        self.assertAlmostEqual(norm(row((1 / sqrt(2), 1 / sqrt(2)))), 1)
        self.assertAlmostEqual(norm(col((1, 0, 0))), 1)
        self.assertAlmostEqual(norm(eye(5, 10)), abs(eye(5, 10)))

    def test_angle(self):
        self.assertAlmostEqual(angle(row((1, 0)), row((0, 10))), pi / 2)
        self.assertAlmostEqual(angle(row((1, 0)), row((1000, 0))), 0)
        self.assertAlmostEqual(angle(row((1, 0)), row((-1000, 0))), pi)

    def test_unit(self):
        self.assertIterableAlmostEqual(unit(row((1, 1))), row((1 / sqrt(2), 1 / sqrt(2))))
        self.assertIterableAlmostEqual(unit(row((100, 0))), row((1, 0)))

    def test_proj(self):
        self.assertIterableAlmostEqual(proj(row((1, 1, 1)), i), row((1, 0, 0)))
        self.assertIterableAlmostEqual(proj(row((100, 100, 100)), i), row((100, 0, 0)))
        self.assertIterableAlmostEqual(proj(row((100, 100, 100)), j), row((0, 100, 0)))
        self.assertIterableAlmostEqual(proj(row((100, 100, 100)), k), row((0, 0, 100)))

    def test_cross(self):
        self.assertIterableAlmostEqual(cross(i, i), zeros(1, 3))
        self.assertIterableAlmostEqual(cross(i, j), k)
        self.assertIterableAlmostEqual(cross(i, k), -j)
        self.assertIterableAlmostEqual(cross(j, i), -k)
        self.assertIterableAlmostEqual(cross(j, j), zeros(1, 3))
        self.assertIterableAlmostEqual(cross(j, k), i)
        self.assertIterableAlmostEqual(cross(k, i), j)
        self.assertIterableAlmostEqual(cross(k, j), -i)
        self.assertIterableAlmostEqual(cross(k, k), zeros(1, 3))

        for _ in range(self.MONTE_CARLO_TEST_COUNT):
            u, v = random(1, 3), random(1, 3)

            self.assertAlmostEqual(abs(cross(u, v)), abs(u) * abs(v) * sin(angle(u, v)))

    def test_parallel(self):
        self.assertTrue(parallel(row((1, 0, 0)), row((100, 0, 0))))
        self.assertTrue(parallel(row((1, 0, 0)), row((-100, 0, 0))))
        self.assertFalse(parallel(row((1, 0, 0)), row((-100, 1, 0))))

        self.assertTrue(parallel(i, i))
        self.assertFalse(parallel(i, j))
        self.assertFalse(parallel(i, k))
        self.assertFalse(parallel(j, i))
        self.assertTrue(parallel(j, j))
        self.assertFalse(parallel(j, k))
        self.assertFalse(parallel(k, i))
        self.assertFalse(parallel(k, j))
        self.assertTrue(parallel(k, k))

    def test_orthogonal(self):
        self.assertFalse(orthogonal(i, i))
        self.assertTrue(orthogonal(i, j))
        self.assertTrue(orthogonal(i, k))
        self.assertTrue(orthogonal(j, i))
        self.assertFalse(orthogonal(j, j))
        self.assertTrue(orthogonal(j, k))
        self.assertTrue(orthogonal(k, i))
        self.assertTrue(orthogonal(k, j))
        self.assertFalse(orthogonal(k, k))


if __name__ == '__main__':
    main()
