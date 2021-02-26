from math2.data import Vector


class Particle:
    def __init__(self, *, p: Vector = Vector(), q: float = 0):
        self.p = p
        self.q = q
