from auxiliary import default

from math2.linalg.matrices import Matrix


def singleton(s):
    return Matrix(((s,),))


def row(v):
    return Matrix((v,))


def column(v):
    return Matrix((s,) for s in v)


def diagonal(v):
    return Matrix((v[r] if r == c else 0 for c in range(len(v))) for r in range(len(v)))


def zeros(m, n=None):
    return Matrix((0 for _ in range(default(n, m))) for _ in range(m))


def ones(m, n=None):
    return Matrix((1 for _ in range(default(n, m))) for _ in range(m))


def identity(m, n=None):
    return Matrix((int(r == c) for c in range(default(n, m))) for r in range(m))


i = row((1, 0, 0))
j = row((0, 1, 0))
k = row((0, 0, 1))
