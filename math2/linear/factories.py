from itertools import repeat

from auxiliary import default, flattened

from math2.linear.matrices import Matrix


def empty():
    return Matrix((), 0, 0)


def singleton(s):
    return Matrix((s,), 1, 1)


def row(seq):
    return Matrix(seq, 1, len(seq))


def col(seq):
    return Matrix(seq, len(seq), 1)


def rows(seqs):
    return Matrix(flattened(seqs), len(seqs), len(seqs[0]) if seqs else 0)


def cols(seqs):
    return rows(seqs) ** 'T'


def diag(seq):
    n = len(seq)

    return Matrix((scalar if r == c else 0 for r, scalar in enumerate(seq) for c in range(n)), n, n)


def zeros(m, n=None):
    n = default(n, m)

    return Matrix(repeat(0, m * n), m, n)


def ones(m, n=None):
    n = default(n, m)

    return Matrix(repeat(1, m * n), m, n)


def eye(m, n=None):
    n = default(n, m)

    return Matrix((int(r == c) for r in range(m) for c in range(n)), m, n)


def full(m, n, scalar=None):
    if scalar is None:
        scalar, n = n, scalar

    n = default(n, m)

    return Matrix((scalar for _ in range(m) for _ in range(n)), m, n)


def random(m, n=None):
    from random import random as factory
    n = default(n, m)

    return Matrix((factory() for _ in range(m) for _ in range(n)), m, n)


i = row((1, 0, 0))
j = row((0, 1, 0))
k = row((0, 0, 1))
