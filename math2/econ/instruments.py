from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from enum import Enum
from itertools import chain
from typing import Optional

from auxiliary import retain_iter

from math2.consts import EPS
from math2.econ.cashflows import CashFlow
from math2.econ.factors import ap, fa
from math2.econ.ints import CompInt
from math2.misc import frange


class Instrument(ABC):
    """Instrument is the abstract base class for all financial instruments."""

    @abstractmethod
    def cash_flows(self, interest: CompInt) -> Iterator[CashFlow]:
        """Calculates the cash flows of this instrument at the given interest value.

        :param interest: The interest value.
        :return: The cash flows.
        """
        pass


class Bond(Instrument):
    """Bond is the class for bonds."""

    def __init__(self, face: float, coupon: float, frequency: float, maturity: float):
        self.face = face
        self.coupon = coupon
        self.frequency = frequency
        self.maturity = maturity

    def cash_flows(self, interest: Optional[CompInt] = None) -> Iterator[CashFlow]:
        period = 1 / self.frequency

        return chain(
            (CashFlow(t, self.coupon) for t in frange(period, self.maturity + EPS, period)),
            (CashFlow(self.maturity, self.face),),
        )

    @classmethod
    def from_rate(cls, face: float, rate: float, frequency: float, maturity: float) -> Bond:
        """Creates the bond from the coupon rate.

        :param face: The face value.
        :param rate: The coupon rate.
        :param frequency: The period count.
        :param maturity: The maturity of the bond.
        :return: The created bond.
        """
        return Bond(face, face * rate / frequency, frequency, maturity)


class Mortgage(Instrument):
    """Mortgage is the class for mortgages."""

    def __init__(self, principal: float, frequency: float = 12, amortization: float = 25):
        self.principal = principal
        self.frequency = frequency
        self.amortization = amortization

    def cash_flows(self, interest: CompInt) -> Iterator[CashFlow]:
        payment = self.payment(interest)
        subperiod = 1 / self.frequency

        return chain((CashFlow(0, -self.principal),),
                     (CashFlow(t, payment) for t in frange(subperiod, self.amortization + EPS, subperiod)))

    def payment(self, interest: CompInt) -> float:
        """Calculates the payment value with respect to the given interest value.

        :param interest: The interest value.
        :return: The payment.
        """
        return self.principal * ap(interest.to_subperiod(self.frequency).rate, self.frequency * self.amortization)

    def pay(self, term: int, interest: CompInt, payment: Optional[float] = None) -> Mortgage:
        """Creates a new mortgage instance assuming payments were made.

        :param interest: The interest value.
        :param term: The term during which payments were made.
        :param payment: The optional payment made, defaults to payment with respect to the interest.
        :return: The next mortgage instance.
        """
        return self.pay(term, interest, self.payment(interest)) if payment is None else Mortgage(
            self.principal * interest.to_factor(term) - payment
            * fa(interest.to_subperiod(self.frequency).rate, term * self.frequency),
            self.frequency, self.amortization - term,
        )

    @classmethod
    def from_down(cls, value: float, down: float, frequency: float = 12, amortization: float = 25) -> Mortgage:
        """Constructs the mortgage instance from the down payment value.

        :param value: The total value.
        :param down: The down payment.
        :param frequency: The frequency of payments, defaults to 12.
        :param amortization: The amortization of the mortgage, defaults to 25.
        :return: The constructed mortgage instance.
        """
        return cls(value - down, frequency, amortization)

    @classmethod
    def from_dtv(cls, value: float, dtv: float, frequency: float = 12, amortization: float = 25) -> Mortgage:
        """Constructs the mortgage instance from the down payment to value percentage.

        :param value: The total value.
        :param dtv: The down payment to value percentage.
        :param frequency: The frequency of payments, defaults to 12.
        :param amortization: The amortization of the mortgage, defaults to 25.
        :return: The constructed mortgage instance.
        """
        return cls.from_down(value, value * dtv, frequency, amortization)

    @classmethod
    def from_ltv(cls, value: float, ltv: float, frequency: float = 12, amortization: float = 25) -> Mortgage:
        """Constructs the mortgage instance from the loan payment to value percentage.

        :param value: The total value.
        :param ltv: The loan payment to value percentage.
        :param frequency: The frequency of payments, defaults to 12.
        :param amortization: The amortization of the mortgage, defaults to 25.
        :return: The constructed mortgage instance.
        """
        return cls(value * ltv, frequency, amortization)


class Project(Instrument):
    """Project is the class for projects."""

    def __init__(self, initial: float, final: float, annuity: float, life: float):
        self.initial = initial
        self.final = final
        self.annuity = annuity
        self.life = life

    def cash_flows(self, interest: Optional[CompInt] = None) -> Iterator[CashFlow]:
        return chain((CashFlow(0, self.initial),), (CashFlow(t, self.annuity) for t in frange(1, self.life + EPS)),
                     (CashFlow(self.life, self.final),))


class Rel(Enum):
    """Relationship is the enum class for all relationships of alternative projects."""
    INDEP = 0
    MEX = 1
    REL = 2


@retain_iter
def rel(values: Iterable[float], budget: float) -> Rel:
    """Determines the relationship of values with respect to the budget.

    :param values: The values.
    :param budget: The budget.
    :return: The relationship.
    """
    if sum(values) <= budget:
        return Rel.INDEP
    elif sum(sorted(values)[:2]) <= budget:
        return Rel.REL
    else:
        return Rel.MEX


def rel_combinations(values: Iterable[float], budget: float) -> Iterator[Iterator[int]]:
    """Gets the combinations of the related values given their values and the budget.

    :param values: The values of the projects.
    :param budget: The budget.
    :return: The combinations of possible projects that can be chosen.
    """
    if values := tuple(values):
        i = len(values) - 1
        chosen = rel_combinations(values[:i], budget - values[i]) if values[i] <= budget else ()
        skipped = rel_combinations(values[:i], budget)

        return chain((chain(sub_combination, [i]) for sub_combination in chosen), skipped)
    else:
        return iter((iter(()),))
