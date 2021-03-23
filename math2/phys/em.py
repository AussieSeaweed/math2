from abc import ABC, abstractmethod
from math import pi

from math2.linear import unit
from math2.phys.consts import e0


class ElectromagneticField:
    def __init__(self):
        self.charges = []

    def intensity(self, loc):
        pass


class Charge(ABC):
    @abstractmethod
    def intensity(self, loc):
        pass


class PointCharge(Charge):
    def __init__(self, loc, value):
        self.loc = loc
        self.value = value

    def intensity(self, loc):
        r = loc - self.loc

        return self.value / (4 * pi * e0 * abs(r) ** 2) * unit(r)


class LineCharge(Charge):
    pass


class PlaneCharge(Charge):
    pass


class VolumeCharge(Charge):
    pass
