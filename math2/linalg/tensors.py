from collections.abc import MutableSequence
from functools import partial
from itertools import starmap
from operator import add, div, mul, neg, pos, sub


class Vector(MutableSequence):
    def __init__(self, it=()):
        self.__values = list(it)

    def insert(self, index, value):
        self.__values.insert(index, value)

    def __pos__(self):
        return Vector(map(pos, self))

    def __neg__(self):
        return Vector(map(neg, self))

    def __add__(self, other):
        try:
            if len(self) == len(other):
                return Vector(starmap(add, zip(self, other)))
            else:
                raise ValueError('Invalid lengths')
        except TypeError:
            return NotImplemented

    def __sub__(self, other):
        try:
            if len(self) == len(other):
                return Vector(starmap(sub, zip(self, other)))
            else:
                raise ValueError('Invalid lengths')
        except TypeError:
            return NotImplemented

    def __mul__(self, other):
        return Vector(map(partial(mul, other), self))

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return Vector(map(partial(div, other), self))

    def __matmul__(self, other):
        try:
            if len(self) == len(other):
                return sum(map(mul, zip(self, other)))
            else:
                raise ValueError('Invalid lengths')
        except TypeError:
            return NotImplemented

    def __getitem__(self, i):
        return self.__values[i]

    def __setitem__(self, i, o):
        self.__values[i] = o

    def __delitem__(self, i):
        del self.__values[i]

    def __len__(self):
        return len(self.__values)
