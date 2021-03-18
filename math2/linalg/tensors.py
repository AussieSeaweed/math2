from collections.abc import MutableSequence


class Vector(MutableSequence):
    def __init__(self, it=()):
        self.__values = list(it)

    def insert(self, index, value):
        self.__values.insert(index, value)

    def __getitem__(self, i):
        return self.__values[i]

    def __setitem__(self, i, o):
        self.__values[i] = o

    def __delitem__(self, i):
        del self.__values[i]

    def __len__(self):
        return len(self.__values)
