from functools import cache

from auxiliary import product


@cache
def factorial(x):
    return factorial(x - 1) if x else 1


def cyclic_permutations(n):
    return factorial(n - 1)


def permutations(n, r):
    return product(range(n, n - r, -1))


def combinations(n, r):
    return permutations(n, r) // factorial(r)


def partitions(n, kinds):
    return factorial(n) // product(factorial(kind) for kind in kinds)
