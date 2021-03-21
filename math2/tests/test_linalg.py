from itertools import repeat
from operator import add, matmul, mul
from unittest import main

from auxiliary import ExtendedTestCase

from math2.linalg import DimensionError, Matrix, column, row, singleton, transposed


class LinAlgTestCase(ExtendedTestCase):
    def test_abs(self) -> None:
        self.assertAlmostEqual(abs(Matrix((range(3), range(3, 6)))), 7.416198487095663)
        self.assertAlmostEqual(abs(Matrix((range(6),))), 7.416198487095663)
        self.assertAlmostEqual(abs(Matrix((x,) for x in range(6))), 7.416198487095663)

    def test_iter(self) -> None:
        self.assertEqual(Matrix((range(3), range(3, 6))), range(6))
        self.assertEqual(Matrix((range(6),)), range(6))
        self.assertEqual(Matrix((x,) for x in range(6)), range(6))

    def test_getitem(self) -> None:
        self.assertEqual(Matrix((range(3), range(3, 6)))[4], 4)
        self.assertEqual(Matrix((range(6),))[4], 4)
        self.assertEqual(Matrix((x,) for x in range(6))[4], 4)

        self.assertIterableEqual(Matrix((range(3), range(3, 6)))[2:5], range(2, 5))
        self.assertIterableEqual(Matrix((range(6),))[2:5], range(2, 5))
        self.assertIterableEqual(Matrix((x,) for x in range(6))[2:5], range(2, 5))

        self.assertIterableEqual(Matrix((range(3), range(3, 6)))[::-1], reversed(range(6)))
        self.assertIterableEqual(Matrix((range(6),))[::-1], reversed(range(6)))
        self.assertIterableEqual(Matrix((x,) for x in range(6))[::-1], reversed(range(6)))

        self.assertEqual(Matrix((range(3), range(3, 6)))[1, 1], 4)
        self.assertEqual(Matrix((range(6),))[0, 4], 4)
        self.assertEqual(Matrix((x,) for x in range(6))[4, 0], 4)

        self.assertEqual(Matrix((range(3), range(3, 6)))[:, :], Matrix((range(3), range(3, 6))))
        self.assertEqual(Matrix((range(6),))[:, :], Matrix((range(6),)))
        self.assertEqual(Matrix((x,) for x in range(6))[:, :], Matrix((x,) for x in range(6)))

        self.assertEqual(Matrix((range(3), range(3, 6)))[:, :2], Matrix((range(2), range(3, 5))))
        self.assertEqual(Matrix((range(6),))[0, :], Matrix((range(6),)))
        self.assertEqual(Matrix((x,) for x in range(6))[:, 0], Matrix((x,) for x in range(6)))

    def test_len(self) -> None:
        self.assertEqual(len(Matrix((range(3), range(3, 6)))), 6)
        self.assertEqual(len(Matrix((range(6),))), 6)
        self.assertEqual(len(Matrix((x,) for x in range(6))), 6)

    def test_pos(self) -> None:
        self.assertEqual(+Matrix((range(3), range(3, 6))), Matrix((range(3), range(3, 6))))
        self.assertEqual(+Matrix((range(6),)), Matrix((range(6),)))
        self.assertEqual(+Matrix((x,) for x in range(6)), Matrix((x,) for x in range(6)))

    def test_neg(self) -> None:
        self.assertEqual(-Matrix((range(3), range(3, 6))), Matrix((range(0, -3, -1), range(-3, -6, -1))))
        self.assertEqual(-Matrix((range(6),)), Matrix((range(0, -6, -1),)))
        self.assertEqual(-Matrix((x,) for x in range(6)), Matrix((-x,) for x in range(6)))

    def test_add(self) -> None:
        self.assertEqual(Matrix((range(3), range(3, 6))) + Matrix((range(6, 9), range(9, 12))),
                         Matrix(((6, 8, 10), (12, 14, 16))))
        self.assertEqual(Matrix((range(5, -1, -1),)) + Matrix((range(6),)), Matrix((repeat(5, 6),)))
        self.assertEqual(Matrix((x,) for x in range(5, -1, -1)) + Matrix((x,) for x in range(6)),
                         Matrix((5,) for _ in range(6)))
        self.assertRaises(TypeError, add, row(range(5)), 5)
        self.assertRaises(DimensionError, add, row(range(5)), column(range(5)))
        self.assertRaises(DimensionError, add, row(range(5)), row(range(6)))

    def test_mul(self) -> None:
        self.assertEqual(Matrix((range(3), range(3, 6))) * 5, Matrix((range(0, 15, 5), range(15, 30, 5))))
        self.assertEqual(Matrix((range(5, -1, -1),)) * 5, row(range(25, -1, -5)))
        self.assertEqual(Matrix((x,) for x in range(5, -1, -1)) * 5, column(range(25, -1, -5)))

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
        self.assertEqual(5 * Matrix((range(5, -1, -1),)), row(range(25, -1, -5)))
        self.assertEqual(5 * Matrix((x,) for x in range(5, -1, -1)), column(range(25, -1, -5)))

    def test_matmul(self) -> None:
        self.assertEqual(Matrix((range(3), range(3, 6))) @ Matrix((range(6, 9), range(9, 12))), 145)
        self.assertEqual(Matrix((range(5, -1, -1),)) @ Matrix((range(6),)), 20)
        self.assertEqual(Matrix((x,) for x in range(5, -1, -1)) @ Matrix((x,) for x in range(6)), 20)
        self.assertRaises(DimensionError, matmul, row(range(5)), column(range(5)))
        self.assertRaises(DimensionError, matmul, row(range(5)), row(range(6)))


class UtilsTestCase(ExtendedTestCase):
    def test_transposed(self):
        self.assertEqual(transposed(Matrix((range(3), range(3, 6)))), Matrix(((0, 3), (1, 4), (2, 5))))
        self.assertEqual(transposed(Matrix((range(6),))), column(range(6)))
        self.assertEqual(transposed(Matrix((x,) for x in range(6))), row(range(6)))


if __name__ == '__main__':
    main()
