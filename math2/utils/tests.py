from collections import Iterable, Sequence
from typing import Any, Optional, Type, TypeVar
from unittest import TestCase

_T = TypeVar('_T')


class ExtendedTestCase(TestCase):
    """ExtendedTestCase is the class for extended test cases"""

    def assertIterableEqual(self, it1: Iterable[_T], it2: Iterable[_T], msg: Any = ...,
                            it_type: Optional[Type[Iterable[_T]]] = None) -> None:
        """An equality assertion for ordered iterables (like lists and tuples).

        :param it1: The first iterable to compare.
        :param it2: The second iterable to compare.
        :param msg: Optional message to use on failure instead of a list of differences.
        :param it_type: The expected datatype of the iterables, or None if no datatype should be enforced.
        :return: None
        """
        if it_type is not None:
            self.assertIsInstance(it1, it_type, msg)
            self.assertIsInstance(it2, it_type, msg)

        self.assertSequenceEqual(tuple(it1), tuple(it2), msg)

    def assertSequenceAlmostEqual(self, seq1: Sequence[float], seq2: Sequence[float], places: Optional[int] = None,
                                  msg: Any = ..., delta: Optional[float] = None,
                                  seq_type: Optional[Type[Sequence[float]]] = None) -> None:
        """An equality assertion for ordered sequences (like lists and tuples). Fail if the any two corresponding
           objects are unequal as determined by their difference rounded to the given number of decimal places (default
           7) and comparing to zero, or by comparing that the difference between the two objects is more than the given
           delta.

           Note that decimal places (from zero) are usually not the same as significant digits (measured from the most
           significant digit).

           If the two objects compare equal then they will automatically compare almost equal.

        :param seq1: The first sequence to compare.
        :param seq2: The second sequence to compare.
        :param places: The places to enforce.
        :param msg: Optional message to use on failure instead of a list of differences.
        :param delta: The delta to enforce.
        :param seq_type: The expected datatype of the sequences, or None if no datatype should be enforced.
        :return: None
        """
        if seq_type is not None:
            self.assertIsInstance(seq1, seq_type, msg)
            self.assertIsInstance(seq2, seq_type, msg)

        self.assertEqual(len(seq1), len(seq2), msg)

        for v1, v2 in zip(seq1, seq2):
            self.assertAlmostEqual(v1, v2, places, msg, delta)

    def assertIterableAlmostEqual(self, it1: Iterable[float], it2: Iterable[float], places: Optional[int] = None,
                                  msg: Any = ..., delta: Optional[float] = None,
                                  it_type: Optional[Type[Iterable[float]]] = None) -> None:
        """An equality assertion for ordered iterables (like lists and tuples). Fail if the any two corresponding
           objects are unequal as determined by their difference rounded to the given number of decimal places (default
           7) and comparing to zero, or by comparing that the difference between the two objects is more than the given
           delta.

           Note that decimal places (from zero) are usually not the same as significant digits (measured from the most
           significant digit).

           If the two objects compare equal then they will automatically compare almost equal.

        :param it1: The first iterable to compare.
        :param it2: The second iterable to compare.
        :param places: The places to enforce.
        :param msg: Optional message to use on failure instead of a list of differences.
        :param delta: The delta to enforce.
        :param it_type: The expected datatype of the iterables, or None if no datatype should be enforced.
        :return: None
        """
        if it_type is not None:
            self.assertIsInstance(it1, it_type, msg)
            self.assertIsInstance(it2, it_type, msg)

        self.assertSequenceAlmostEqual(tuple(it1), tuple(it2), places, msg, delta)
