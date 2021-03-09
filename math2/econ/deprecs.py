from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from typing import Optional

from auxiliary import ilen, retain_iter

from math2.misc import series_sum


class Deprec(ABC):
    """Deprec is the abstract base class for all depreciations."""

    def __init__(self, basis: float, salvage: float, life: int):
        self.basis = basis
        self.salvage = salvage
        self.life = life

    def cap_gain(self, market: float) -> float:
        """Obtains the capital gain with respect to the market value.

        :param market: The market value.
        :return: The capital gain.
        """
        return max(0.0, market - self.basis)

    def recap_deprec(self, market: float) -> float:
        """Obtains the recaptured depreciation with respect to the market value.

        :param market: The market value.
        :return: The recaptured depreciation.
        """
        return max(0.0, min(self.basis, market) - self.salvage)

    def loss_on_disp(self, market: float) -> float:
        """Obtains the loss on disposal with respect to the market value.

        :param market: The market value.
        :return: The loss on disposal.
        """
        return max(0.0, self.salvage - market)

    @property
    def books(self) -> Iterator[float]:
        """Calculates the book values throughout its life.

        :return: The book values.
        """
        return (self.book(t) for t in range(self.life + 1))

    @abstractmethod
    def book(self, t: int) -> float:
        """The book value at time t.

        :param t: The time.
        :return: The book value.
        """
        pass

    @abstractmethod
    def amount(self, t: int) -> float:
        """The positive loss of the depreciation at time t.

        :param t: The time.
        :return: The loss.
        """
        pass


class StrLineDeprec(Deprec):
    """StrLineDeprec is the class for straight line depreciations."""

    def book(self, t: int) -> float:
        return self.basis - self.amount() * t

    def amount(self, t: Optional[int] = None) -> float:
        return (self.basis - self.salvage) / self.life


class DeclBalDeprec(Deprec):
    """DeclBalDeprec is the class for declining balance depreciations."""

    @property
    def rate(self) -> float:
        return 1 - (self.salvage / self.basis) ** (1 / self.life)

    def book(self, t: int) -> float:
        return self.basis * (1 - self.rate) ** t

    def amount(self, t: int) -> float:
        return self.book(t - 1) * self.rate

    @classmethod
    def from_rate(cls, basis: float, life: int, rate: float) -> DeclBalDeprec:
        """Constructs the declining balance depreciation from salvage value.

        :param basis: The basis.
        :param life: The life.
        :param rate: The depreciation rate.
        :return: The declining balance depreciation.
        """
        return DeclBalDeprec(basis, basis * (1 - rate) ** life, life)


class DblDeclBalDeprec(Deprec):
    """DblDeclBalDeprec is the class for double declining balance depreciations."""

    def __init__(self, basis: float, salvage: float, life: int, floor: bool = False):
        super().__init__(basis, salvage, life)

        self.floor = floor

    @property
    def rate(self) -> float:
        return 2 / self.life

    def book(self, t: int) -> float:
        book = self.basis * (1 - self.rate) ** t

        return max(self.salvage, book) if self.floor else book

    def amount(self, t: int) -> float:
        return self.book(t - 1) * self.rate


class SYDDeprec(Deprec):
    """SYDDeprec is the class for sum-of-years'-digits depreciations."""

    @property
    def syd(self) -> int:
        """
        :return: The sum of the years' digits.
        """
        return series_sum(self.life)

    def book(self, t: int) -> float:
        return self.basis - (self.syd - series_sum(self.life - t)) / self.syd * (self.basis - self.salvage)

    def amount(self, t: int) -> float:
        return (self.life - t + 1) / self.syd * (self.basis - self.salvage)


class UPDeprec(Deprec):
    """UPDeprec is the class for units of production depreciations."""

    @retain_iter
    def __init__(self, basis: float, salvage: float, prods: Iterable[float]):
        super().__init__(basis, salvage, ilen(prods))

        self.prods = list(prods)

    @property
    def lifetime_prod(self) -> float:
        """
        :return: The lifetime production.
        """
        return sum(self.prods)

    def book(self, t: int) -> float:
        return self.basis - sum(self.prods[:t]) / self.lifetime_prod * (self.basis - self.salvage)

    def amount(self, t: int) -> float:
        return self.prods[t - 1] / self.lifetime_prod * (self.basis - self.salvage)
