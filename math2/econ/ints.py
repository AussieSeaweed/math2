from __future__ import annotations

from abc import ABC, abstractmethod
from math import exp, inf, log
from typing import Optional

from math2.econ.factors import fp


class Int(ABC):
    """Int is the abstract base class for all interests."""

    def __init__(self, rate: float):
        self.rate = rate

    @abstractmethod
    def to_factor(self, time: float) -> float:
        """Converts this interest to the factor at the given time period.

        :param time: The time period.
        :return: The converted factor.
        """
        pass

    @classmethod
    @abstractmethod
    def from_factor(cls, factor: float, time: float) -> Int:
        """Converts the factor at a time period to an interest value.

        :param factor: The factor.
        :param time: The time period.
        :return: The converted interest value.
        """
        pass


class SimpleInt(Int):
    """SimpleInt is the class for simple interests."""

    def to_factor(self, time: float) -> float:
        return 1 + self.rate * time

    @classmethod
    def from_factor(cls, factor: float, time: float) -> SimpleInt:
        return SimpleInt((factor - 1) / time)


class CompInt(Int, ABC):
    """CompInt is the abstract base class for all compound interests."""

    @abstractmethod
    def to_ef(self) -> EfInt:
        """Converts this interest value to an effective interest value.

        :return: The converted interest value.
        """
        pass

    @abstractmethod
    def to_cont(self) -> ContInt:
        """Converts this interest value to a continuous interest value.

        :return: The converted interest value.
        """
        pass

    @abstractmethod
    def to_nom(self, sp_count: float) -> NomInt:
        """Converts this interest value to a nominal interest value.

        :param sp_count: The number of subperiods of the converted interest value.
        :return: The converted interest value.
        """
        pass

    @abstractmethod
    def to_sp(self, sp_count: float) -> SPInt:
        """Converts this interest value to a subperiod interest value.

        :param sp_count: The number of subperiods of the converted interest value.
        :return: The converted interest value.
        """
        pass

    @classmethod
    def from_factor(cls, factor: float, time: float) -> CompInt:
        return EfInt(factor ** (1 / time) - 1)


class EfInt(CompInt):
    """EfInt is the class for effective interests."""

    def to_factor(self, time: float) -> float:
        return fp(self.rate, time)

    def to_ef(self) -> EfInt:
        return self

    def to_cont(self) -> ContInt:
        return ContInt(log(self.rate + 1))

    def to_nom(self, sp_count: float) -> NomInt:
        return NomInt(sp_count * ((self.rate + 1) ** (1 / sp_count) - 1), sp_count)

    def to_sp(self, sp_count: float) -> SPInt:
        return SPInt((self.rate + 1) ** (1 / sp_count) - 1, sp_count)


class MulCompInt(CompInt, ABC):
    """MulCompInt is the abstract base class for all multiple compounding interests."""

    def __init__(self, rate: float, sp_count: float):
        super().__init__(rate)

        self.sp_count = sp_count

    @property
    def sp(self) -> float:
        """
        :return: The subperiod of this multiple compound interest value.
        """
        return 1 / self.sp_count


class NomInt(MulCompInt):
    """NomInt is the class for nominal interests."""

    def to_factor(self, time: float) -> float:
        return fp(self.rate / self.sp_count, self.sp_count * time)

    def to_ef(self) -> EfInt:
        return EfInt(fp(self.rate / self.sp_count, self.sp_count) - 1)

    def to_cont(self) -> ContInt:
        return self.to_ef().to_cont()

    def to_nom(self, sp_count: Optional[float] = None) -> NomInt:
        return self if sp_count is None else self.to_ef().to_nom(sp_count)

    def to_sp(self, sp_count: Optional[float] = None) -> SPInt:
        if sp_count is None:
            return SPInt(self.rate / self.sp_count, self.sp_count)
        else:
            return self.to_ef().to_sp(sp_count)


class SPInt(MulCompInt):
    """SPInt is the class for subperiod interests."""

    def to_factor(self, time: float) -> float:
        return fp(self.rate, self.sp_count * time)

    def to_ef(self) -> EfInt:
        return EfInt(fp(self.rate, self.sp_count) - 1)

    def to_cont(self) -> ContInt:
        return self.to_ef().to_cont()

    def to_nom(self, sp_count: Optional[float] = None) -> NomInt:
        if sp_count is None:
            return NomInt(self.rate * self.sp_count, self.sp_count)
        else:
            return self.to_ef().to_nom(sp_count)

    def to_sp(self, sp_count: Optional[float] = None) -> SPInt:
        return self if sp_count is None else self.to_ef().to_sp(sp_count)


class ContInt(MulCompInt):
    """ContInt is the class for continuous interests."""

    def __init__(self, rate: float):
        super().__init__(rate, inf)

    def to_factor(self, time: float) -> float:
        return exp(self.rate) ** time

    def to_ef(self) -> EfInt:
        return EfInt(exp(self.rate) - 1)

    def to_cont(self) -> ContInt:
        return self

    def to_nom(self, sp_count: float) -> NomInt:
        return self.to_ef().to_nom(sp_count)

    def to_sp(self, sp_count: float) -> SPInt:
        return self.to_ef().to_sp(sp_count)