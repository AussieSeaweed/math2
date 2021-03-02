from __future__ import annotations

from abc import ABC, abstractmethod
from functools import cached_property
from math import exp, inf, log
from typing import Optional

from math2.economics.factors import fp


class Interest(ABC):
    """Interest is the abstract base class for all interests."""

    def __init__(self, rate: float):
        self.rate = rate

    @abstractmethod
    def to_factor(self, time: float) -> float:
        """Converts this interest to the factor at the given time period.

        :param time: The time period
        :return: The converted factor
        """
        ...

    @classmethod
    @abstractmethod
    def from_factor(cls, factor: float, time: float) -> Interest:
        """Converts the factor at a time period to an interest value.

        :param factor: The factor
        :param time: The time period
        :return: The converted interest value
        """
        ...


class SimpleInterest(Interest):
    """SimpleInterest is the class for simple interests."""

    def to_factor(self, time: float) -> float:
        return 1 + self.rate * time

    @classmethod
    def from_factor(cls, factor: float, time: float) -> SimpleInterest:
        return SimpleInterest((factor - 1) / time)


class CompoundInterest(Interest, ABC):
    """CompoundInterest is the abstract base class for all compound interests."""

    @abstractmethod
    def to_effective(self) -> EffectiveInterest:
        """Converts this interest value to an effective interest value.

        :return: The converted interest value
        """
        ...

    @abstractmethod
    def to_continuous(self) -> ContinuousInterest:
        """Converts this interest value to a continuous interest value.

        :return: The converted interest value
        """
        ...

    @abstractmethod
    def to_nominal(self, subperiod_count: float) -> NominalInterest:
        """Converts this interest value to a nominal interest value.

        :param subperiod_count: The number of subperiods of the converted interest value
        :return: The converted interest value
        """
        ...

    @abstractmethod
    def to_subperiod(self, subperiod_count: float) -> SubperiodInterest:
        """Converts this interest value to a subperiod interest value.

        :param subperiod_count: The number of subperiods of the converted interest value
        :return: The converted interest value
        """
        ...

    @classmethod
    def from_factor(cls, factor: float, time: float) -> CompoundInterest:
        return EffectiveInterest(factor ** (1 / time) - 1)


class EffectiveInterest(CompoundInterest):
    """EffectiveInterest is the class for effective interests."""

    def to_factor(self, time: float) -> float:
        return fp(self.rate, time)

    def to_effective(self) -> EffectiveInterest:
        return self

    def to_continuous(self) -> ContinuousInterest:
        return ContinuousInterest(log(self.rate + 1))

    def to_nominal(self, subperiod_count: float) -> NominalInterest:
        return NominalInterest(subperiod_count * ((self.rate + 1) ** (1 / subperiod_count) - 1), subperiod_count)

    def to_subperiod(self, subperiod_count: float) -> SubperiodInterest:
        return SubperiodInterest((self.rate + 1) ** (1 / subperiod_count) - 1, subperiod_count)


class MultipleCompoundInterest(CompoundInterest, ABC):
    """MultipleCompoundInterest is the abstract base class for all multiple compounding interests."""

    def __init__(self, rate: float, subperiod_count: float):
        super().__init__(rate)

        self.subperiod_count = subperiod_count

    @cached_property
    def subperiod(self) -> float:
        return 1 / self.subperiod_count


class NominalInterest(MultipleCompoundInterest):
    """NominalInterest is the class for nominal interests."""

    def to_factor(self, time: float) -> float:
        return fp(self.rate / self.subperiod_count, self.subperiod_count * time)

    def to_effective(self) -> EffectiveInterest:
        return EffectiveInterest(fp(self.rate / self.subperiod_count, self.subperiod_count) - 1)

    def to_continuous(self) -> ContinuousInterest:
        return self.to_effective().to_continuous()

    def to_nominal(self, subperiod_count: Optional[float] = None) -> NominalInterest:
        return self if subperiod_count is None else self.to_effective().to_nominal(subperiod_count)

    def to_subperiod(self, subperiod_count: Optional[float] = None) -> SubperiodInterest:
        if subperiod_count is None:
            return SubperiodInterest(self.rate / self.subperiod_count, self.subperiod_count)
        else:
            return self.to_effective().to_subperiod(subperiod_count)


class SubperiodInterest(MultipleCompoundInterest):
    """SubperiodInterest is the class for subperiod interests."""

    def to_factor(self, time: float) -> float:
        return fp(self.rate, self.subperiod_count * time)

    def to_effective(self) -> EffectiveInterest:
        return EffectiveInterest(fp(self.rate, self.subperiod_count) - 1)

    def to_continuous(self) -> ContinuousInterest:
        return self.to_effective().to_continuous()

    def to_nominal(self, subperiod_count: Optional[float] = None) -> NominalInterest:
        if subperiod_count is None:
            return NominalInterest(self.rate * self.subperiod_count, self.subperiod_count)
        else:
            return self.to_effective().to_nominal(subperiod_count)

    def to_subperiod(self, subperiod_count: Optional[float] = None) -> SubperiodInterest:
        return self if subperiod_count is None else self.to_effective().to_subperiod(subperiod_count)


class ContinuousInterest(MultipleCompoundInterest):
    """ContinuousInterest is the class for continuous interests."""

    def __init__(self, rate: float):
        super().__init__(rate, inf)

    def to_factor(self, time: float) -> float:
        return exp(self.rate) ** time

    def to_effective(self) -> EffectiveInterest:
        return EffectiveInterest(exp(self.rate) - 1)

    def to_continuous(self) -> ContinuousInterest:
        return self

    def to_nominal(self, subperiod_count: float) -> NominalInterest:
        return self.to_effective().to_nominal(subperiod_count)

    def to_subperiod(self, subperiod_count: float) -> SubperiodInterest:
        return self.to_effective().to_subperiod(subperiod_count)
