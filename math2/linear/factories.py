from collections.abc import Sequence
from typing import Optional

from auxiliary import default

from math2.linear.matrices import Matrix


def singleton(s: float) -> Matrix:
    return Matrix(((s,),))


def row(seq: Sequence[float]) -> Matrix:
    return Matrix((seq,))


def column(seq: Sequence[float]) -> Matrix:
    return Matrix((s,) for s in seq)


def diagonal(seq: Sequence[float]) -> Matrix:
    return Matrix((seq[r] if r == c else 0 for c in range(len(seq))) for r in range(len(seq)))


def zeros(m: int, n: Optional[int] = None) -> Matrix:
    return Matrix((0 for _ in range(default(n, m))) for _ in range(m))


def ones(m: int, n: Optional[int] = None) -> Matrix:
    return Matrix((1 for _ in range(default(n, m))) for _ in range(m))


def identity(m: int, n: Optional[int] = None) -> Matrix:
    return Matrix((int(r == c) for c in range(default(n, m))) for r in range(m))


def random(m: int, n: Optional[int] = None) -> Matrix:
    from random import random as factory

    return Matrix((factory() for _ in range(default(n, m))) for _ in range(m))


i = row((1, 0, 0))
j = row((0, 1, 0))
k = row((0, 0, 1))
