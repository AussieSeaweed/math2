from abc import ABC, abstractmethod

from math2.economics.ints import EfInt
from math2.miscellaneous import series_sum


class Deprec(ABC):
    """Deprec is the abstract base class for all depreciations."""

    def __init__(self, basis, salvage, life):
        self.basis = basis
        self.salvage = salvage
        self.life = life

    def cap_gain(self, market):
        """Obtains the capital gain with respect to the market value.

        :param market: The market value.
        :return: The capital gain.
        """
        return max(0, market - self.basis)

    def recap_deprec(self, market):
        """Obtains the recaptured depreciation with respect to the market value.

        :param market: The market value.
        :return: The recaptured depreciation.
        """
        return max(0, min(self.basis, market) - self.salvage)

    def loss_on_disp(self, market):
        """Obtains the loss on disposal with respect to the market value.

        :param market: The market value.
        :return: The loss on disposal.
        """
        return max(0, self.salvage - market)

    @property
    def books(self):
        """Calculates the book values throughout its life.

        :return: The book values.
        """
        return (self.book(t) for t in range(self.life + 1))

    @abstractmethod
    def book(self, t):
        """The book value at time t.

        :param t: The time.
        :return: The book value.
        """
        pass

    @abstractmethod
    def amount(self, t):
        """The positive loss of the depreciation at time t.

        :param t: The time.
        :return: The loss.
        """
        pass


class StrLineDeprec(Deprec):
    """StrLineDeprec is the class for straight line depreciations."""

    def book(self, t):
        return self.basis - self.amount() * t

    def amount(self, t=None):
        return (self.basis - self.salvage) / self.life


class DeclBalDeprec(Deprec):
    """DeclBalDeprec is the class for declining balance depreciations."""

    @property
    def int(self):
        return EfInt(1 - (self.salvage / self.basis) ** (1 / self.life))

    def book(self, t):
        return self.basis * (1 - self.int.to_ef().rate) ** t

    def amount(self, t):
        return self.book(t - 1) * self.int.rate

    @classmethod
    def from_rate(cls, basis, life, rate):
        """Constructs the declining balance depreciation from salvage value.

        :param basis: The basis.
        :param life: The life.
        :param rate: The depreciation rate.
        :return: The declining balance depreciation.
        """
        return DeclBalDeprec(basis, basis * (1 - rate.to_ef().rate) ** life, life)


class DblDeclBalDeprec(DeclBalDeprec):
    """DblDeclBalDeprec is the class for double declining balance depreciations."""

    def __init__(self, basis, salvage, life, floor=False):
        super().__init__(basis, salvage, life)

        self.floor = floor

    @property
    def int(self):
        return EfInt(2 / self.life)

    def book(self, t):
        return max(self.salvage, super().book(t)) if self.floor else super().book(t)


class SYDDeprec(Deprec):
    """SYDDeprec is the class for sum-of-years'-digits depreciations."""

    @property
    def syd(self):
        """
        :return: The sum of the years' digits.
        """
        return series_sum(self.life)

    def book(self, t):
        return self.basis - (self.syd - series_sum(self.life - t)) / self.syd * (self.basis - self.salvage)

    def amount(self, t):
        return (self.life - t + 1) / self.syd * (self.basis - self.salvage)


class UPDeprec(Deprec):
    """UPDeprec is the class for units of production depreciations."""

    def __init__(self, basis, salvage, prods):
        super().__init__(basis, salvage, len(prods))

        self.prods = list(prods)

    @property
    def lifetime_prod(self):
        """
        :return: The lifetime production.
        """
        return sum(self.prods)

    def book(self, t):
        return self.basis - sum(self.prods[:t]) / self.lifetime_prod * (self.basis - self.salvage)

    def amount(self, t):
        return self.prods[t - 1] / self.lifetime_prod * (self.basis - self.salvage)
