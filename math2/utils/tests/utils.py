from collections import Iterable, Sequence
from typing import Any
from unittest import TestCase


class ExtendedTestCase(TestCase):
    """ExtendedTestCase is the class for extended test cases"""

    def assertSequenceAlmostEqual(self, seq1: Sequence[Any], seq2: Sequence[Any]) -> None:
        """Checks if elements in both sequences are almost equal.

        :param seq1: the first sequence
        :param seq2: the second sequence
        :return: None
        """
        self.assertEqual(len(seq1), len(seq2))

        for v1, v2 in zip(seq1, seq2):
            self.assertAlmostEqual(v1, v2)

    def assertIterableEqual(self, it1: Iterable[Any], it2: Iterable[Any]) -> None:
        """Checks if elements in both iterables are almost equal.

        :param it1: the first iterable
        :param it2: the second iterable
        :return: None
        """
        self.assertSequenceEqual(tuple(it1), tuple(it2))

    def assertIterableAlmostEqual(self, it1: Iterable[Any], it2: Iterable[Any]) -> None:
        """Checks if elements in both iterables are almost equal.

        :param it1: the first iterable
        :param it2: the second iterable
        :return: None
        """
        self.assertSequenceAlmostEqual(tuple(it1), tuple(it2))
