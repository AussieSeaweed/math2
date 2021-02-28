from __future__ import annotations

from abc import ABC, abstractmethod
from math import exp, inf, log
from typing import Optional

from math2.economics.factors import fp


class Interest(ABC):
    """Interest is the abstract base class for all interests."""

    def __init__(self, r: float):
        self.r = r

    @abstractmethod
    def __call__(self, t: float) -> float:
        ...


class SimpleInterest(Interest):
    """SimpleInterest is the class for simple interests."""

    def __call__(self, t: float) -> float:
        return 1 + self.r * t


class CompoundInterest(Interest, ABC):
    """CompoundInterest is the abstract base class for all compound interests."""

    @abstractmethod
    def to_effective(self) -> EffectiveInterest:
        """Converts this interest value to an effective interest value.

        :return: the converted interest value
        """
        ...

    @abstractmethod
    def to_continuous(self) -> ContinuousInterest:
        """Converts this interest value to a continuous interest value.

        :return: the converted interest value
        """
        ...

    @abstractmethod
    def to_nominal(self, n: float) -> NominalInterest:
        """Converts this interest value to a nominal interest value.

        :return: the converted interest value
        """
        ...

    @abstractmethod
    def to_subperiod(self, n: float) -> SubperiodInterest:
        """Converts this interest value to a subperiod interest value.

        :return: the converted interest value
        """
        ...


class EffectiveInterest(CompoundInterest):
    """EffectiveInterest is the class for effective interests."""

    def __call__(self, t: float) -> float:
        return fp(self.r, t)

    def to_effective(self) -> EffectiveInterest:
        return self

    def to_continuous(self) -> ContinuousInterest:
        return ContinuousInterest(log(self.r + 1))

    def to_nominal(self, n: float) -> NominalInterest:
        return NominalInterest(n * ((self.r + 1) ** (1 / n) - 1), n)

    def to_subperiod(self, n: float) -> SubperiodInterest:
        return SubperiodInterest((self.r + 1) ** (1 / n) - 1, n)


class MultipleCompoundInterest(CompoundInterest, ABC):
    """MultipleCompoundInterest is the abstract base class for all multiple compounding interests."""

    def __init__(self, r: float, n: float):
        super().__init__(r)

        self.n = n


class NominalInterest(MultipleCompoundInterest):
    """NominalInterest is the class for nominal interests."""

    def __call__(self, t: float) -> float:
        return fp(self.r / self.n, self.n * t)

    def to_effective(self) -> EffectiveInterest:
        return EffectiveInterest(fp(self.r / self.n, self.n) - 1)

    def to_continuous(self) -> ContinuousInterest:
        return self.to_effective().to_continuous()

    def to_nominal(self, n: Optional[float] = None) -> NominalInterest:
        return self if n is None else self.to_effective().to_nominal(n)

    def to_subperiod(self, n: Optional[float] = None) -> SubperiodInterest:
        return SubperiodInterest(self.r / self.n, self.n) if n is None else self.to_effective().to_subperiod(n)


class SubperiodInterest(MultipleCompoundInterest):
    """SubperiodInterest is the class for subperiod interests."""

    def __call__(self, t: float) -> float:
        return fp(self.r, self.n * t)

    def to_effective(self) -> EffectiveInterest:
        return EffectiveInterest(fp(self.r, self.n) - 1)

    def to_continuous(self) -> ContinuousInterest:
        return self.to_effective().to_continuous()

    def to_nominal(self, n: Optional[float] = None) -> NominalInterest:
        return NominalInterest(self.r * self.n, self.n) if n is None else self.to_effective().to_nominal(n)

    def to_subperiod(self, n: Optional[float] = None) -> SubperiodInterest:
        return self if n is None else self.to_effective().to_subperiod(n)


class ContinuousInterest(MultipleCompoundInterest):
    """ContinuousInterest is the class for continuous interests."""

    def __init__(self, r: float):
        super().__init__(r, inf)

    def __call__(self, t: float) -> float:
        return exp(self.r) ** t

    def to_effective(self) -> EffectiveInterest:
        return EffectiveInterest(exp(self.r) - 1)

    def to_continuous(self) -> ContinuousInterest:
        return self

    def to_nominal(self, n: float) -> NominalInterest:
        return self.to_effective().to_nominal(n)

    def to_subperiod(self, n: float) -> SubperiodInterest:
        return self.to_effective().to_subperiod(n)
