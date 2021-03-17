from abc import ABC, abstractmethod
from collections.abc import MutableSequence, Sequence
from itertools import accumulate
from operator import add, sub

from auxiliary import windowed


def _psa(arr, merge):
    return list(accumulate(arr, merge))


def _da(arr, separate):
    return [arr[0]] + [separate(y, x) for x, y in windowed(arr, 2)]


def _originate(f):
    def wrapper(ea, *args, **kwargs):
        ea.__revert__()
        ret = f(ea, *args, **kwargs)
        ea.__convert__()

        return ret

    return wrapper


class ExtendedSequence(Sequence, ABC):
    def __init__(self, merge=add, separate=sub):
        self._merge = merge
        self._separate = separate


class ExtendedMutableSequence(ExtendedSequence, MutableSequence, ABC):
    pass


class ExtendedArray(ExtendedMutableSequence):
    def __init__(self, it, merge=add, separate=sub):
        super().__init__(merge, separate)

        self._arr = list(it)

        self.__convert__()

    @_originate
    def insert(self, index, value):
        self._arr.insert(index, value)

    @_originate
    def __getitem__(self, i):
        return self._arr[i]

    @_originate
    def __setitem__(self, i, o):
        self._arr[i] = o

    @_originate
    def __delitem__(self, i):
        del self._arr[i]

    def __len__(self):
        return len(self._arr)

    @abstractmethod
    def __convert__(self):
        pass

    @abstractmethod
    def __revert__(self):
        pass


class PrefixSumArray(ExtendedArray):
    def __convert__(self):
        self._arr = _psa(self._arr, self._merge)

    def __revert__(self):
        self._arr = _da(self._arr, self._separate)


class DifferenceArray(ExtendedArray):
    def __convert__(self):
        self._arr = _da(self._arr, self._separate)

    def __revert__(self):
        self._arr = _psa(self._arr, self._merge)


class BinaryIndexedTree(ExtendedMutableSequence):
    def insert(self, index, value):
        pass

    def __getitem__(self, i):
        pass

    def __setitem__(self, i, o):
        pass

    def __delitem__(self, i):
        pass

    def __len__(self):
        pass


a = DifferenceArray(range(1, 1000000))

print(list(a))
