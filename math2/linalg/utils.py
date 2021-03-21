from math import acos


def norm(m, p=2):
    return sum(s ** p for s in m) ** (1 / p)


def angle_between(u, v):
    return acos(u @ v / (abs(u) * abs(v)))


def unit(v):
    return v / abs(v)


def project(u, v):
    return u @ v / abs(v) * unit(v)
