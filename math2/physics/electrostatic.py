from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from math import pi

from auxiliary import sum_

from math2.calculus import Region
from math2.linear import Vector
from math2.physics.consts import e0


class ElectrostaticField:
    def __init__(self) -> None:
        self.charges = list[Charge]()

    def intensity(self, location: Vector) -> Vector:
        return sum_((charge.intensity(location) for charge in self.charges))

    def force(self, charge: DiscreteCharge) -> Vector:
        return self.intensity(charge.location) * charge.value


class Charge(ABC):
    @abstractmethod
    def intensity(self, location: Vector) -> Vector:
        pass


class DiscreteCharge(Charge):
    def __init__(self, location: Vector, value: float):
        self.location = location
        self.value = value

    def intensity(self, location: Vector) -> Vector:
        r = location - self.location

        return self.value / (4 * pi * e0 * abs(r) ** 2) * r.unit


class ContinuousCharge(Charge):
    def __init__(self, region: Region, density: Callable[[Vector], float]):
        self.region = region
        self.density = density

    def intensity(self, location: Vector) -> Vector:
        raise NotImplementedError  # TODO


class Dipole(Charge):
    def __init__(self, location: Vector, displacement: Vector, value: float):
        self.location = location
        self.displacement = displacement
        self.value = value

    @property
    def moment(self) -> Vector:
        return self.value * self.displacement

    def intensity(self, location: Vector) -> Vector:
        r = location - self.location

        return (3 * r @ self.moment / abs(r) ** 2 * r - self.moment) / (4 * pi * e0 * abs(r) ** 3)
