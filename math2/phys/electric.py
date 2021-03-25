from abc import ABC, abstractmethod
from math import pi

from math2.linear import unit, zeros
from math2.phys.consts import e0


class ElectricField:
    def __init__(self):
        self.charges = []

    def intensity(self, loc):
        return sum((charge.intensity(loc) for charge in self.charges), start=zeros(*loc.dims))

    def force(self, pt_charge):
        return self.intensity(pt_charge.loc) * pt_charge.value


class Charge(ABC):
    @abstractmethod
    def intensity(self, loc):
        pass


class DiscreteCharge(Charge):
    def __init__(self, loc, value):
        self.loc = loc
        self.value = value

    def intensity(self, loc):
        r = loc - self.loc

        return self.value / (4 * pi * e0 * abs(r) ** 2) * unit(r)


class ContinuousCharge(Charge):
    def __init__(self, region, density):
        self.region = region
        self.density = density

    def intensity(self, loc):
        return self.region.integral(lambda v: DiscreteCharge(v, self.density).intensity(loc))


class Dipole(Charge):
    def __init__(self, loc, disp, value):
        self.loc = loc
        self.disp = disp
        self.value = value

    @property
    def moment(self):
        return self.value * self.disp

    def intensity(self, loc):
        r = loc - self.loc

        return (3 * r @ self.moment / abs(r) ** 2 * r - self.moment) / (4 * pi * e0 * abs(r) ** 3)
