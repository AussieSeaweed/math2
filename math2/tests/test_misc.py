from unittest import main

from auxiliary import ExtendedTestCase

from math2.misc import bind, frange, interp, prod


class MiscTestCase(ExtendedTestCase):
    def test_bind(self) -> None:
        self.assertEqual(bind(1, 0, 2), 1)
        self.assertEqual(bind(-100, 0, 2), 0)
        self.assertEqual(bind(100, 0, 2), 2)
        self.assertRaises(ValueError, bind, 100, 2, 0)

    def test_prod(self) -> None:
        self.assertEqual(prod(range(6)), 0)
        self.assertEqual(prod(range(1, 6)), 120)
        self.assertEqual(prod(range(1, 6), 1), 120)
        self.assertEqual(prod((), 1), 1)
        self.assertRaises(ValueError, prod, ())

    def test_frange(self) -> None:
        self.assertIterableAlmostEqual(frange(5), (0, 1, 2, 3, 4))
        self.assertIterableAlmostEqual(frange(1, 5), (1, 2, 3, 4))
        self.assertIterableAlmostEqual(frange(1, 5, 0.5), (1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5))

    def test_interp(self) -> None:
        self.assertAlmostEqual(interp(1, 0, 2, 0, 3), 1.5)
        self.assertAlmostEqual(interp(1, 0, 1, 0, 3), 3)
        self.assertAlmostEqual(interp(2, 0, 1, 0, 6), 12)


if __name__ == '__main__':
    main()
