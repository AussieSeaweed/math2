from abc import ABC, abstractmethod

from math2.analysis import dbl_quad, quad, tpl_quad


class Region(ABC):
    @abstractmethod
    def integral(self, f):
        pass


class Line(Region):
    def __init__(self, c, xlo, xhi):
        self.c = c
        self.xlo = xlo
        self.xhi = xhi

    def integral(self, f):
        return quad(lambda x: f(self.c(x)), self.xlo, self.xhi)


class Surface(Region):
    def __init__(self, s, xlo, xhi, ylo, yhi):
        self.s = s
        self.xlo = xlo
        self.xhi = xhi
        self.ylo = ylo
        self.yhi = yhi

    def integral(self, f):
        return dbl_quad(lambda x, y: f(self.s(x, y)), self.xlo, self.xhi, self.ylo, self.yhi)


class Volume(Region):
    def __init__(self, v, xlo, xhi, ylo, yhi, zlo, zhi):
        self.v = v
        self.xlo = xlo
        self.xhi = xhi
        self.ylo = ylo
        self.yhi = yhi
        self.zlo = zlo
        self.zhi = zhi

    def integral(self, f):
        return tpl_quad(lambda x, y, z: f(self.v(x, y, z)), self.xlo, self.xhi, self.ylo, self.yhi, self.zlo, self.zhi)
