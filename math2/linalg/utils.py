from auxiliary import default

from math2.linalg.matrices import Matrix


def singleton(scalar):
    return Matrix(((scalar,),))


def row(vector):
    return Matrix((vector,))


def column(vector):
    return Matrix((scalar,) for scalar in vector)


def diagonal(values):
    return Matrix((values[r] if r == c else 0 for c in range(len(values))) for r in range(len(values)))


def zeros(m, n=None):
    return Matrix((0 for _ in range(default(n, m))) for _ in range(m))


def ones(m, n=None):
    return Matrix((1 for _ in range(default(n, m))) for _ in range(m))


def identity(m, n=None):
    return Matrix((int(r == c) for c in range(default(n, m))) for r in range(m))


i = row((1, 0, 0))
j = row((0, 1, 0))
k = row((0, 0, 1))
