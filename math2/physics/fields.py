from abc import ABC, abstractmethod
from collections import MutableSequence
from math import pi
from typing import Union

from auxiliary.utils import sum_

from math2.constants import e0
from math2.data import Vector
from math2.physics.particles import Particle


class Field(ABC):
    def __init__(self) -> None:
        self.particles: MutableSequence[Particle] = []

    @abstractmethod
    def intensity(self, v: Vector) -> Vector:
        pass

    @abstractmethod
    def potential(self, v: Vector) -> float:
        pass

    @classmethod
    @abstractmethod
    def force(cls, p1: Particle, p2: Union[Particle, Vector]) -> Vector:
        pass


class ElectricField(Field):
    def intensity(self, v: Vector) -> Vector:
        return sum_(p.q / abs(r := v - p.p) ** 3 * r for p in self.particles) / (4 * pi * e0)

    def potential(self, v: Vector) -> float:
        return sum_(p.q / abs(v - p.p) for p in self.particles) / (4 * pi * e0)

    @classmethod
    def force(cls, p1: Particle, p2: Union[Particle, Vector]) -> Vector:
        if isinstance(p2, Particle):
            dr = p2.p - p1.p

            return p1.q * p2.q / (4 * pi * e0 * abs(dr) ** 3) * dr
        elif isinstance(p2, Vector):
            dr = p2 - p1.p

            return p1.q / (4 * pi * e0 * abs(dr) ** 2) * dr
        else:
            raise TypeError('Invalid type')
