from functools import partial
from math import pi, sin, sqrt
from operator import add, matmul, mul
from unittest import main

from auxiliary import ExtendedTestCase

from math2.linear import (DimensionError, Matrix, column, columns, diagonal_matrix, empty_column, empty_matrix,
                          empty_row,
                          empty_vector,
                          full_matrix, full_vector, i,
                          identity_matrix, j, k, norm, one_matrix, one_vector, random_matrix, random_vector, row, rows,
                          singleton_matrix, singleton_vector, vector,
                          zero_matrix, zero_vector)


class TensorTestCase(ExtendedTestCase):
    def test_pos(self) -> None:
        self.assertEqual(+rows((range(3), range(3, 6))), rows((range(3), range(3, 6))))
        self.assertEqual(+row(range(6)), row(range(6)))
        self.assertEqual(+column(range(6)), column(range(6)))
        self.assertEqual(+vector(range(6)), vector(range(6)))

    def test_neg(self) -> None:
        self.assertEqual(-rows((range(3), range(3, 6))), rows((range(0, -3, -1), range(-3, -6, -1))))
        self.assertEqual(-row(range(6)), rows((range(0, -6, -1),)))
        self.assertEqual(-column(range(6)), rows(tuple((-x,) for x in range(6))))
        self.assertEqual(-vector(range(6)), vector(range(0, -6, -1)))

    def test_add(self) -> None:
        self.assertEqual(
            rows((range(3), range(3, 6))) + rows((range(6, 9), range(9, 12))), rows(((6, 8, 10), (12, 14, 16))))
        self.assertEqual(row(range(5, -1, -1)) + row(range(6)), row((5,) * 6))
        self.assertEqual(column(range(5, -1, -1)) + column(range(6)), column((5,) * 6))
        self.assertEqual(vector(range(5, -1, -1)) + vector(range(6)), vector((5,) * 6))
        self.assertRaises(TypeError, add, row(range(5)), 5)
        self.assertRaises(DimensionError, add, row(range(5)), column(range(5)))
        self.assertRaises(DimensionError, add, row(range(5)), row(range(6)))
        self.assertRaises(DimensionError, add, row(range(5)), vector(range(5)))

    def test_sub(self) -> None:
        self.assertEqual(
            rows((range(3), range(3, 6))) - rows((range(6, 9), range(9, 12))), rows(((-6, -6, -6), (-6, -6, -6))))
        self.assertEqual(row(range(5, -1, -1)) - row(range(6)), row(range(5, -6, -2)))
        self.assertEqual(column(range(5, -1, -1)) - column(range(6)), column(range(5, -6, -2)))
        self.assertEqual(vector(range(5, -1, -1)) - vector(range(6)), vector(range(5, -6, -2)))

    def test_mul(self) -> None:
        self.assertEqual(rows((range(3), range(3, 6))) * 5, rows((range(0, 15, 5), range(15, 30, 5))))
        self.assertEqual(row(range(5, -1, -1)) * 5, row(range(25, -1, -5)))
        self.assertEqual(column(range(5, -1, -1)) * 5, column(range(25, -1, -5)))
        self.assertEqual(vector(range(5, -1, -1)) * 5, vector(range(25, -1, -5)))

    def test_rmul(self) -> None:
        self.assertEqual(5 * rows((range(3), range(3, 6))), rows((range(0, 15, 5), range(15, 30, 5))))
        self.assertEqual(5 * row(range(5, -1, -1)), row(range(25, -1, -5)))
        self.assertEqual(5 * column(range(5, -1, -1)), column(range(25, -1, -5)))
        self.assertEqual(5 * vector(range(5, -1, -1)), vector(range(25, -1, -5)))

    def test_div(self) -> None:
        self.assertEqual(rows((range(0, 15, 5), range(15, 30, 5))) / 5, rows((range(3), range(3, 6))))
        self.assertEqual(row(range(25, -1, -5)) / 5, row(range(5, -1, -1)))
        self.assertEqual(column(range(25, -1, -5)) / 5, column(range(5, -1, -1)))
        self.assertEqual(vector(range(25, -1, -5)) / 5, vector(range(5, -1, -1)))

    def test_matmul(self) -> None:
        self.assertEqual(rows((range(3), range(3, 6))) @ rows((range(6, 9), range(9, 12))), 145)
        self.assertEqual(row(range(5, -1, -1)) @ row(range(6)), 20)
        self.assertEqual(column(range(5, -1, -1)) @ column(range(6)), 20)
        self.assertEqual(vector(range(5, -1, -1)) @ vector(range(6)), 20)
        self.assertRaises(DimensionError, matmul, row(range(5)), column(range(5)))
        self.assertRaises(DimensionError, matmul, row(range(5)), row(range(6)))

    def test_abs(self) -> None:
        self.assertAlmostEqual(abs(rows((range(3), range(3, 6)))), 7.416198487095663)
        self.assertAlmostEqual(abs(row(range(6))), 7.416198487095663)
        self.assertAlmostEqual(abs(column(range(6))), 7.416198487095663)

    def test_getitem(self) -> None:
        self.assertEqual(rows((range(3), range(3, 6)))[4], 4)
        self.assertEqual(row(range(6))[4], 4)
        self.assertEqual(column(range(6))[4], 4)
        self.assertEqual(vector(range(6))[4], 4)

        self.assertIterableEqual(rows((range(3), range(3, 6)))[2:5], range(2, 5))
        self.assertIterableEqual(row(range(6))[2:5], range(2, 5))
        self.assertIterableEqual(column(range(6))[2:5], range(2, 5))
        self.assertIterableEqual(vector(range(6))[2:5], range(2, 5))


class MatrixTestCase(ExtendedTestCase):
    def test_row_dimension(self) -> None:
        self.assertEqual(zero_matrix(3).row_dimension, 3)
        self.assertEqual(zero_matrix(3, 4).row_dimension, 3)
        self.assertEqual(zero_matrix(4, 3).row_dimension, 4)

    def test_column_dimension(self) -> None:
        self.assertEqual(zero_matrix(3).column_dimension, 3)
        self.assertEqual(zero_matrix(3, 4).column_dimension, 4)
        self.assertEqual(zero_matrix(4, 3).column_dimension, 3)

    def test_rows(self) -> None:
        self.assert2DIterableEqual(row(range(5)).rows, (range(5),))
        self.assert2DIterableEqual(column(range(5)).rows, ((0,), (1,), (2,), (3,), (4,)))
        self.assert2DIterableEqual(Matrix(range(6), (2, 3)).rows, (range(3), range(3, 6)))

    def test_columns(self) -> None:
        self.assert2DIterableEqual(row(range(5)).columns, ((0,), (1,), (2,), (3,), (4,)))
        self.assert2DIterableEqual(column(range(5)).columns, (range(5),))
        self.assert2DIterableEqual(Matrix(range(6), (2, 3)).columns, ((0, 3), (1, 4), (2, 5)))

    def test_determinant(self) -> None:
        pass  # TODO

    def test_eigenpairs(self) -> None:
        pass  # TODO

    def test_eigenvalues(self) -> None:
        pass  # TODO

    def test_eigenvectors(self) -> None:
        pass  # TODO

    def test_is_square(self) -> None:
        self.assertTrue(zero_matrix(3))
        self.assertTrue(zero_matrix(3, 4))
        self.assertTrue(zero_matrix(4, 3))

    def test_mul(self) -> None:
        self.assertEqual(
            rows((range(3), range(3, 6))) * rows((range(2), range(2, 4), range(4, 6))), rows(((10, 13), (28, 40))))
        self.assertEqual(row(range(5, -1, -1)) * column(range(6)), singleton_matrix(20))
        self.assertEqual(column(range(6)) * row(range(6)), rows((
            (0,) * 6, range(6), range(0, 12, 2), range(0, 18, 3), range(0, 24, 4), range(0, 30, 5),
        )))
        self.assertEqual(row(range(5, -1, -1)) * vector(range(6)), singleton_matrix(20))
        self.assertRaises(DimensionError, mul, row(range(5)), row(range(5)))
        self.assertRaises(DimensionError, mul, row(range(5)), column(range(6)))

    def test_pow(self) -> None:
        self.assertEqual(rows((range(3), range(3, 6))) ** 'T', rows(((0, 3), (1, 4), (2, 5))))
        self.assertEqual(row(range(6)) ** 'T', column(range(6)))
        self.assertEqual(column(range(6)) ** 'T', row(range(6)))

        # TODO: powers and inverses

    def test_getitem(self) -> None:
        self.assertIterableEqual(rows((range(3), range(3, 6)))[::-1], reversed(range(6)))
        self.assertIterableEqual(row(range(6))[::-1], reversed(range(6)))
        self.assertIterableEqual(column(range(6))[::-1], reversed(range(6)))

        self.assertEqual(rows((range(3), range(3, 6)))[1, 1], 4)
        self.assertEqual(row(range(6))[0, 4], 4)
        self.assertEqual(column(range(6))[4, 0], 4)

        self.assertEqual(rows((range(3), range(3, 6)))[:, :], rows((range(3), range(3, 6))))
        self.assertEqual(row(range(6))[:, :], row(range(6)))
        self.assertEqual(column(range(6))[:, :], column(range(6)))

        self.assertEqual(rows((range(3), range(3, 6)))[:, :2], rows((range(2), range(3, 5))))
        self.assertEqual(row(range(6))[0, :], row(range(6)))
        self.assertEqual(column(range(6))[:, 0], column(range(6)))


class VectorTestCase(ExtendedTestCase):
    def test_dimension(self) -> None:
        self.assertEqual(empty_vector().dimension, 0)
        self.assertEqual(zero_vector(5).dimension, 5)

    def test_unit(self) -> None:
        self.assertIterableAlmostEqual(vector((1, 1)).unit, vector((1 / sqrt(2), 1 / sqrt(2))))
        self.assertIterableAlmostEqual(vector((100, 0)).unit, vector((1, 0)))
        self.assertIterableAlmostEqual(vector((0, 100, 0)).unit, j)

    def test_x(self) -> None:
        self.assertEqual(vector(range(1, 1)).x, 0)
        self.assertEqual(vector(range(1, 2)).x, 1)
        self.assertEqual(vector(range(1, 3)).x, 1)
        self.assertEqual(vector(range(1, 4)).x, 1)
        self.assertEqual(vector(range(1, 5)).x, 1)
        self.assertEqual(vector(range(1, 6)).x, 1)

    def test_y(self) -> None:
        self.assertEqual(vector(range(1, 1)).y, 0)
        self.assertEqual(vector(range(1, 2)).y, 0)
        self.assertEqual(vector(range(1, 3)).y, 2)
        self.assertEqual(vector(range(1, 4)).y, 2)
        self.assertEqual(vector(range(1, 5)).y, 2)
        self.assertEqual(vector(range(1, 6)).y, 2)

    def test_z(self) -> None:
        self.assertEqual(vector(range(1, 1)).z, 0)
        self.assertEqual(vector(range(1, 2)).z, 0)
        self.assertEqual(vector(range(1, 3)).z, 0)
        self.assertEqual(vector(range(1, 4)).z, 3)
        self.assertEqual(vector(range(1, 5)).z, 3)
        self.assertEqual(vector(range(1, 6)).z, 3)

    def test_w(self) -> None:
        self.assertEqual(vector(range(1, 1)).w, 0)
        self.assertEqual(vector(range(1, 2)).w, 0)
        self.assertEqual(vector(range(1, 3)).w, 0)
        self.assertEqual(vector(range(1, 4)).w, 0)
        self.assertEqual(vector(range(1, 5)).w, 4)
        self.assertEqual(vector(range(1, 6)).w, 4)

    def test_parallel_to(self) -> None:
        self.assertTrue(vector((1, 0, 0)).parallel_to(vector((100, 0, 0))))
        self.assertTrue(vector((1, 0, 0)).parallel_to(vector((-100, 0, 0))))
        self.assertFalse(vector((1, 0, 0)).parallel_to(vector((-100, 1, 0))))

        self.assertTrue(i.parallel_to(i))
        self.assertFalse(i.parallel_to(j))
        self.assertFalse(i.parallel_to(k))
        self.assertFalse(j.parallel_to(i))
        self.assertTrue(j.parallel_to(j))
        self.assertFalse(j.parallel_to(k))
        self.assertFalse(k.parallel_to(i))
        self.assertFalse(k.parallel_to(j))
        self.assertTrue(k.parallel_to(k))

    def test_orthogonal_to(self) -> None:
        self.assertFalse(i.orthogonal_to(i))
        self.assertTrue(i.orthogonal_to(j))
        self.assertTrue(i.orthogonal_to(k))
        self.assertTrue(j.orthogonal_to(i))
        self.assertFalse(j.orthogonal_to(j))
        self.assertTrue(j.orthogonal_to(k))
        self.assertTrue(k.orthogonal_to(i))
        self.assertTrue(k.orthogonal_to(j))
        self.assertFalse(k.orthogonal_to(k))

    def test_cross(self) -> None:
        self.assertIterableAlmostEqual(i.cross(i), zero_vector(3))
        self.assertIterableAlmostEqual(i.cross(j), k)
        self.assertIterableAlmostEqual(i.cross(k), -j)
        self.assertIterableAlmostEqual(j.cross(i), -k)
        self.assertIterableAlmostEqual(j.cross(j), zero_vector(3))
        self.assertIterableAlmostEqual(j.cross(k), i)
        self.assertIterableAlmostEqual(k.cross(i), j)
        self.assertIterableAlmostEqual(k.cross(j), -i)
        self.assertIterableAlmostEqual(k.cross(k), zero_vector(3))

        for _ in range(10):
            u, v = random_vector(3), random_vector(3)

            self.assertAlmostEqual(abs(u.cross(v)), abs(u) * abs(v) * sin(u.angle_between(v)))

    def test_angle_between(self) -> None:
        self.assertAlmostEqual(vector((1, 0)).angle_between(vector((0, 10))), pi / 2)
        self.assertAlmostEqual(vector((1, 0)).angle_between(vector((1000, 0))), 0)
        self.assertAlmostEqual(vector((1, 0)).angle_between(vector((-1000, 0))), pi)

    def test_projection_on(self) -> None:
        self.assertIterableAlmostEqual(vector((1, 1, 1)).projection_on(i), vector((1, 0, 0)))
        self.assertIterableAlmostEqual(vector((100, 100, 100)).projection_on(i), vector((100, 0, 0)))
        self.assertIterableAlmostEqual(vector((100, 100, 100)).projection_on(j), vector((0, 100, 0)))
        self.assertIterableAlmostEqual(vector((100, 100, 100)).projection_on(k), vector((0, 0, 100)))


class FactoryTestCase(ExtendedTestCase):
    def test_row(self) -> None:
        self.assertEqual(row(()).dimensions, (1, 0))
        self.assertEqual(row(range(10)), rows((range(10),)))
        self.assertEqual(row(tuple(map(partial(pow, 2), range(5)))), rows(((1, 2, 4, 8, 16),)))

    def test_column(self) -> None:
        self.assertEqual(column(()).dimensions, (0, 1))
        self.assertEqual(column(range(10)), rows(tuple((x,) for x in range(10))))
        self.assertEqual(column(tuple(map(partial(pow, 2), range(5)))), rows(((1,), (2,), (4,), (8,), (16,))))

    def test_rows(self) -> None:
        self.assertEqual(rows(((1, 2), (3, 6))).dimensions, (2, 2))

    def test_columns(self) -> None:
        self.assertEqual(columns(((1, 2), (3, 6))).dimensions, (2, 2))

    def test_vector(self) -> None:
        self.assertEqual(vector(range(5)).dimensions, (5,))

    def test_empty_matrix(self) -> None:
        self.assertEqual(empty_matrix().dimensions, (0, 0))

    def test_empty_row(self) -> None:
        self.assertEqual(empty_row().dimensions, (1, 0))

    def test_empty_column(self) -> None:
        self.assertEqual(empty_column().dimensions, (0, 1))

    def test_empty_vector(self) -> None:
        self.assertEqual(empty_vector().dimensions, (0,))

    def test_singleton_matrix(self) -> None:
        self.assertEqual(singleton_matrix(5), rows(((5,),)))
        self.assertEqual(singleton_matrix(0), rows(((0,),)))
        self.assertEqual(singleton_matrix(10), rows(((10,),)))

    def test_singleton_vector(self) -> None:
        self.assertEqual(singleton_vector(5), vector((5,)))
        self.assertEqual(singleton_vector(0), vector((0,)))
        self.assertEqual(singleton_vector(10), vector((10,)))

    def test_full_matrix(self) -> None:
        self.assertEqual(full_matrix(lambda r, c: 1, 2), columns(((1, 1), (1, 1))))
        self.assertEqual(full_matrix(lambda r, c: 1, 2, 2), columns(((1, 1), (1, 1))))

    def test_full_vector(self) -> None:
        self.assertEqual(full_vector(int, 5), vector(range(5)))

    def test_zero_matrix(self) -> None:
        self.assertEqual(zero_matrix(0), empty_matrix())
        self.assertEqual(zero_matrix(5), rows(((0,) * 5, (0,) * 5, (0,) * 5, (0,) * 5, (0,) * 5)))
        self.assertEqual(zero_matrix(5, 5), rows(((0,) * 5, (0,) * 5, (0,) * 5, (0,) * 5, (0,) * 5)))
        self.assertEqual(zero_matrix(1, 5), row((0,) * 5))
        self.assertEqual(zero_matrix(5, 1), column((0,) * 5))

    def test_zero_vector(self) -> None:
        self.assertEqual(zero_vector(0), empty_vector())
        self.assertEqual(zero_vector(5), vector((0,) * 5))

    def test_one_matrix(self) -> None:
        self.assertEqual(one_matrix(0), empty_matrix())
        self.assertEqual(one_matrix(5), rows(((1,) * 5, (1,) * 5, (1,) * 5, (1,) * 5, (1,) * 5)))
        self.assertEqual(one_matrix(5, 5), rows(((1,) * 5, (1,) * 5, (1,) * 5, (1,) * 5, (1,) * 5)))
        self.assertEqual(one_matrix(1, 5), row((1,) * 5))
        self.assertEqual(one_matrix(5, 1), column((1,) * 5))

    def test_one_vector(self) -> None:
        self.assertEqual(one_vector(0), empty_vector())
        self.assertEqual(one_vector(5), vector((1,) * 5))

    def test_random_matrix(self) -> None:
        self.assertEqual(random_matrix(5).dimensions, (5, 5))
        self.assertEqual(random_matrix(5, 1).dimensions, (5, 1))
        self.assertEqual(random_matrix(1, 5).dimensions, (1, 5))

    def test_random_vector(self) -> None:
        self.assertEqual(random_vector(5).dimensions, (5,))

    def test_diagonal_matrix(self) -> None:
        self.assertEqual(diagonal_matrix(()), empty_matrix())
        self.assertEqual(diagonal_matrix((1, 1, 1)), identity_matrix(3))
        self.assertEqual(diagonal_matrix(range(5)), rows((
            (0,) * 5,
            (0, 1, 0, 0, 0),
            (0, 0, 2, 0, 0),
            (0, 0, 0, 3, 0),
            (0, 0, 0, 0, 4),
        )))

    def test_identity_matrix(self) -> None:
        self.assertEqual(identity_matrix(0), empty_matrix())
        self.assertEqual(identity_matrix(5), rows((
            (1, 0, 0, 0, 0),
            (0, 1, 0, 0, 0),
            (0, 0, 1, 0, 0),
            (0, 0, 0, 1, 0),
            (0, 0, 0, 0, 1),
        )))
        self.assertEqual(identity_matrix(1), singleton_matrix(1))


class UtilTestCase(ExtendedTestCase):
    def test_norm(self) -> None:
        self.assertAlmostEqual(norm(row((1 / sqrt(2), 1 / sqrt(2)))), 1)
        self.assertAlmostEqual(norm(column((1, 0, 0))), 1)
        self.assertAlmostEqual(norm(vector(range(5))), abs(vector(range(5))))
        self.assertAlmostEqual(norm(identity_matrix(2)), sqrt(2))


if __name__ == '__main__':
    main()
