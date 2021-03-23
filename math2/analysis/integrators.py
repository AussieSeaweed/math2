from abc import ABC, abstractmethod
from collections.abc import Callable
from functools import partial
from itertools import chain

from auxiliary import windowed

from math2.misc import frange


class Integrator(ABC):
    def dbl_quad(self, f, xlo, xhi, ylo, yhi, steps):
        return self.quad(lambda x: self.quad(
            lambda y: f(x, y),
            ylo(x) if isinstance(ylo, Callable) else ylo,
            yhi(x) if isinstance(yhi, Callable) else yhi,
            steps,
        ), xlo, xhi, steps)

    def tpl_quad(self, f, xlo, xhi, ylo, yhi, zlo, zhi, steps):
        return self.quad(lambda x: self.dbl_quad(
            lambda y, z: f(x, y, z),
            ylo(x) if isinstance(ylo, Callable) else ylo,
            yhi(x) if isinstance(yhi, Callable) else yhi,
            partial(zlo, x) if isinstance(zlo, Callable) else zlo,
            partial(zhi, x) if isinstance(zhi, Callable) else zhi,
            steps,
        ), xlo, xhi, steps)

    @abstractmethod
    def quad(self, f, xlo, xhi, steps):
        pass


class MidpointIntegrator(Integrator):
    def quad(self, f, xlo, xhi, steps):
        return sum(
            (b - a) * f((a + b) / 2)
            for a, b in windowed(chain(frange(xlo, xhi, (xhi - xlo) / steps), (xhi,)), 2)
        )


class TrapezoidIntegrator(Integrator):
    def quad(self, f, xlo, xhi, steps):
        return sum(
            (b - a) * (f(a) + f(b)) / 2
            for a, b in windowed(chain(frange(xlo, xhi, (xhi - xlo) / steps), (xhi,)), 2)
        )


class SimpsonIntegrator(Integrator):
    def quad(self, f, xlo, xhi, steps):
        return sum(
            (b - a) * (f(a) + 4 * f((a + b) / 2) + f(b)) / 6
            for a, b in windowed(chain(frange(xlo, xhi, (xhi - xlo) / steps), (xhi,)), 2)
        )


def quad(f, xlo, xhi):
    import scipy.integrate

    return scipy.integrate.quad(f, xlo, xhi)[0]


def dbl_quad(f, xlo, xhi, ylo, yhi):
    import scipy.integrate

    return scipy.integrate.dblquad(lambda x, y: f(y, x), xlo, xhi, ylo, yhi)[0]


def tpl_quad(f, xlo, xhi, ylo, yhi, zlo, zhi):
    import scipy.integrate

    return scipy.integrate.tplquad(lambda x, y, z: f(z, y, x), xlo, xhi, ylo, yhi, zlo, zhi)[0]
