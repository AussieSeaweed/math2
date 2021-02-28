from abc import ABC, abstractmethod


class Field(ABC):
    def __init__(self):
        self.particles = []

    @abstractmethod
    def intensity(self, v):
        ...

    @abstractmethod
    def potential(self, v):
        ...

    @classmethod
    @abstractmethod
    def force(cls, p1, p2):
        ...


# class ElectricField(Field):
#     def intensity(self, v):
#         return sum_(p.q / abs(r := v - p.p) ** 3 * r for p in self.particles) / (4 * pi * e0)
#
#     def potential(self, v):
#         return sum_(p.q / abs(v - p.p) for p in self.particles) / (4 * pi * e0)
#
#     @classmethod
#     def force(cls, p1, p2):
#         if isinstance(p2, Particle):
#             dr = p2.p - p1.p
#
#             return p1.q * p2.q / (4 * pi * e0 * abs(dr) ** 3) * dr
#         elif isinstance(p2, Vector):
#             dr = p2 - p1.p
#
#             return p1.q / (4 * pi * e0 * abs(dr) ** 2) * dr
#         else:
#             raise TypeError('Invalid type')
