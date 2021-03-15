from abc import ABC, abstractmethod
from functools import total_ordering

import numpy as np

from math2.econ.factors import fp


class Int(ABC):
    """Int is the abstract base class for all interests."""

    def __init__(self, rate):
        self.rate = rate

    @abstractmethod
    def to_factor(self, t=1):
        """Converts this interest to the factor at the given time period.

        :param t: The time period.
        :return: The converted factor.
        """
        pass

    @classmethod
    @abstractmethod
    def from_factor(cls, factor, t=1):
        """Converts the factor at a time period to an interest value.

        :param factor: The factor.
        :param t: The time period.
        :return: The converted interest value.
        """
        pass


@total_ordering
class SimpleInt(Int):
    """SimpleInt is the class for simple interests."""

    def to_factor(self, t=1):
        return 1 + self.rate * t

    @classmethod
    def from_factor(cls, factor, t=1):
        return SimpleInt((factor - 1) / t)

    def __eq__(self, other):
        if isinstance(other, SimpleInt):
            return self.rate == other.rate
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, SimpleInt):
            return self.rate < other.rate
        else:
            return NotImplemented


class CompInt(Int, ABC):
    """CompInt is the abstract base class for all compound interests."""

    @abstractmethod
    def to_ef(self):
        """Converts this interest value to an effective interest value.

        :return: The converted interest value.
        """
        pass

    @abstractmethod
    def to_cont(self):
        """Converts this interest value to a continuous interest value.

        :return: The converted interest value.
        """
        pass

    @abstractmethod
    def to_nom(self, sp_count):
        """Converts this interest value to a nominal interest value.

        :param sp_count: The number of subperiods of the converted interest value.
        :return: The converted interest value.
        """
        pass

    @abstractmethod
    def to_sp(self, sp_count):
        """Converts this interest value to a subperiod interest value.

        :param sp_count: The number of subperiods of the converted interest value.
        :return: The converted interest value.
        """
        pass

    @classmethod
    def from_factor(cls, factor, t=1):
        return EfInt(factor ** (1 / t) - 1)

    def __eq__(self, other):
        if isinstance(other, CompInt):
            return self.to_ef().rate == other.to_ef().rate
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, CompInt):
            return self.to_ef().rate < other.to_ef().rate
        else:
            return NotImplemented


@total_ordering
class EfInt(CompInt):
    """EfInt is the class for effective interests."""

    def to_ef(self):
        return self

    def to_cont(self):
        return ContInt(np.log(self.rate + 1))

    def to_nom(self, sp_count):
        return NomInt(sp_count * ((self.rate + 1) ** (1 / sp_count) - 1), sp_count)

    def to_sp(self, sp_count):
        return SPInt((self.rate + 1) ** (1 / sp_count) - 1, sp_count)

    def to_factor(self, t=1):
        return fp(self.rate, t)


class MulCompInt(CompInt, ABC):
    """MulCompInt is the abstract base class for all multiple compounding interests."""

    def __init__(self, rate, sp_count):
        super().__init__(rate)

        self.sp_count = sp_count

    @property
    def sp(self):
        """
        :return: The subperiod of this multiple compound interest value.
        """
        return 1 / self.sp_count


@total_ordering
class NomInt(MulCompInt):
    """NomInt is the class for nominal interests."""

    def to_ef(self):
        return EfInt(fp(self.rate / self.sp_count, self.sp_count) - 1)

    def to_cont(self):
        return self.to_ef().to_cont()

    def to_nom(self, sp_count=None):
        return self if sp_count is None else self.to_ef().to_nom(sp_count)

    def to_sp(self, sp_count=None):
        return SPInt(self.rate / self.sp_count, self.sp_count) if sp_count is None else self.to_ef().to_sp(sp_count)

    def to_factor(self, t=1):
        return fp(self.rate / self.sp_count, self.sp_count * t)


@total_ordering
class SPInt(MulCompInt):
    """SPInt is the class for sp interests."""

    def to_ef(self):
        return EfInt(fp(self.rate, self.sp_count) - 1)

    def to_cont(self):
        return self.to_ef().to_cont()

    def to_nom(self, sp_count=None):
        return NomInt(self.rate * self.sp_count, self.sp_count) if sp_count is None else self.to_ef().to_nom(sp_count)

    def to_sp(self, sp_count=None):
        return self if sp_count is None else self.to_ef().to_sp(sp_count)

    def to_factor(self, t=1):
        return fp(self.rate, self.sp_count * t)


@total_ordering
class ContInt(MulCompInt):
    """ContInt is the class for continuous interests."""

    def __init__(self, rate):
        super().__init__(rate, np.inf)

    def to_ef(self):
        return EfInt(np.exp(self.rate) - 1)

    def to_cont(self):
        return self

    def to_nom(self, sp_count):
        return self.to_ef().to_nom(sp_count)

    def to_sp(self, sp_count):
        return self.to_ef().to_sp(sp_count)

    def to_factor(self, t=1):
        return np.exp(self.rate) ** t
