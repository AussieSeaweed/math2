from itertools import chain
from typing import Optional, cast
from unittest import main

from math2.utils import ExtendedTestCase, chunk, const, default, get, iter_equal, next_or_none, rotate, trim, window


class UtilsTestCase(ExtendedTestCase):
    def test_chunk(self) -> None:
        self.assert2DIterableEqual(chunk(range(7), 3), (range(3), range(3, 6), range(6, 7)))
        self.assert2DIterableEqual(chunk(range(5), 2), (range(2), range(2, 4), range(4, 5)))
        self.assert2DIterableEqual(chunk(range(5), 1), (range(1), range(1, 2), range(2, 3), range(3, 4), range(4, 5)))
        self.assert2DIterableEqual(chunk(range(5), 1), (range(1), range(1, 2), range(2, 3), range(3, 4), range(4, 5)))

    def test_window(self) -> None:
        self.assert2DIterableEqual(window(range(6), 3), (range(3), range(1, 4), range(2, 5), range(3, 6)))
        self.assert2DIterableEqual(window(range(6), 6), (range(6),))
        self.assert2DIterableEqual(window(range(6), 7), ())
        self.assert2DIterableEqual(window(range(6), 0), ((), (), (), (), (), (), ()))

    def test_trim(self) -> None:
        self.assertIterableEqual(trim(range(10), 0), range(10))
        self.assertIterableEqual(trim(range(10), 0.1), range(1, 9))
        self.assertIterableEqual(trim(range(5), 0.1), range(5))
        self.assertIterableEqual(trim(range(10), 0.5), ())
        self.assertIterableEqual(trim(iter((1, 2, 3)), 1 / 3), (2,))

    def test_rotate(self) -> None:
        self.assertIterableEqual(rotate(range(6), -1), chain((5,), range(5)))
        self.assertIterableEqual(rotate(range(6), 0), range(6))
        self.assertIterableEqual(rotate(range(6), 2), chain(range(2, 6), range(2)))

    def test_const(self) -> None:
        self.assertTrue(const((1, 1, 1)))
        self.assertTrue(const(()))
        self.assertTrue(const(((1, 1), (1, 1))))
        self.assertFalse(const(range(10)))

    def test_iter_equal(self) -> None:
        self.assertTrue(iter_equal(range(6), range(6)))
        self.assertTrue(iter_equal([0, 1, 2], (0, 1, 2)))
        self.assertTrue(iter_equal((), []))
        self.assertFalse(iter_equal(range(7), range(6)))
        self.assertFalse(iter_equal(range(1, 7), range(6)))
        self.assertFalse(iter_equal((), (0,)))

    def test_next_or_none(self) -> None:
        self.assertEqual(next_or_none(iter(range(3))), 0)
        self.assertEqual(next_or_none(iter(())), None)

    def test_default(self) -> None:
        self.assertEqual(default(300, 100), 300)
        self.assertEqual(default(cast(Optional[int], None), 100), 100)

    def test_get(self) -> None:
        self.assertEqual(get(300), 300)
        self.assertRaises(ValueError, get, None)


if __name__ == '__main__':
    main()
