from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TypeVar

from auxiliary import sum_, windowed

from math2.linear import Tensor
from math2.misc import linspace

_T = TypeVar('_T', float, Tensor)


class Integrator(ABC):
    @abstractmethod
    def approx(self, f: Callable[[float], _T], a: float, b: float) -> _T:
        pass


class MidpointIntegrator(Integrator):
    def approx(self, f: Callable[[float], _T], a: float, b: float) -> _T:
        return (b - a) * f((a + b) / 2)


class TrapezoidIntegrator(Integrator):
    def approx(self, f: Callable[[float], _T], a: float, b: float) -> _T:
        return (b - a) * (f(a) + f(b)) / 2


class SimpsonIntegrator(Integrator):
    def approx(self, f: Callable[[float], _T], a: float, b: float) -> _T:
        return (b - a) * (f(a) + 4 * f((a + b) / 2) + f(b)) / 6


def integrate(
        f: Callable[[float], _T],
        xlo: float,
        xhi: float,
        *,
        steps: int,
        integrator: Integrator = SimpsonIntegrator(),
) -> _T:
    return sum_(integrator.approx(f, a, b) for a, b in windowed(linspace(xlo, xhi, steps), 2))


def double_integrate(
        f: Callable[[float, float], _T],
        xlo: float,
        xhi: float,
        ylo: Callable[[float], float],
        yhi: Callable[[float], float],
        *,
        steps: int,
        integrator: Integrator = SimpsonIntegrator(),
) -> _T:
    return integrate(lambda x: integrate(
        lambda y: f(x, y),
        ylo(x),
        yhi(x),
        steps=steps,
        integrator=integrator,
    ), xlo, xhi, steps=steps, integrator=integrator)


def triple_integrate(
        f: Callable[[float, float, float], _T],
        xlo: float,
        xhi: float,
        ylo: Callable[[float], float],
        yhi: Callable[[float], float],
        zlo: Callable[[float, float], float],
        zhi: Callable[[float, float], float],
        *,
        steps: int,
        integrator: Integrator = SimpsonIntegrator(),
) -> _T:
    return integrate(lambda x: double_integrate(
        lambda y, z: f(x, y, z),
        ylo(x),
        yhi(x),
        lambda y: zlo(x, y),
        lambda y: zhi(x, y),
        steps=steps,
        integrator=integrator,
    ), xlo, xhi, steps=steps, integrator=integrator)
