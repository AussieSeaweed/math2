from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from enum import Enum
from itertools import chain
from typing import Optional

from auxiliary import iindex, retain_iter

from math2.econ.cashflows import CashFlow
from math2.econ.factors import af, ap, fa, fp, pa
from math2.econ.interests import CompoundInterest
from math2.misc import frange


class Instrument(ABC):
    """Instrument is the abstract base class for all financial instruments."""

    @abstractmethod
    def cash_flows(self, interest: CompoundInterest) -> Iterator[CashFlow]:
        """Calculates the cash flows of this instrument at the given interest value.

        :param interest: The interest value.
        :return: The cash flows.
        """
        pass

    @abstractmethod
    def present_worth(self, interest: CompoundInterest) -> float:
        """Calculates the present worth of this instrument at the given interest value.

        :param interest: The interest value.
        :return: The present worth.
        """
        pass

    @abstractmethod
    def annual_worth(self, interest: CompoundInterest) -> float:
        """Calculates the annual worth of this instrument at the given interest value.

        :param interest: The interest value.
        :return: The annual worth.
        """
        pass


class Bond(Instrument):
    """Bond is the class for bonds."""

    def __init__(self, face: float, coupon: float, period_count: float, maturity: float):
        self.face = face
        self.coupon = coupon
        self.period_count = period_count
        self.maturity = maturity

    @property
    def period(self) -> float:
        """
        :return: The period of this bond.
        """
        return 1 / self.period_count

    def cash_flows(self, interest: Optional[CompoundInterest] = None) -> Iterator[CashFlow]:
        return chain((CashFlow(t, self.coupon) for t in frange(self.period, self.maturity + self.period, self.period)),
                     (CashFlow(self.maturity, self.face),))

    def present_worth(self, interest: CompoundInterest) -> float:
        return self.coupon * pa(interest.to_subperiod(self.period_count).rate, self.maturity * self.period_count) \
               + self.face / interest.to_factor(self.maturity)

    def annual_worth(self, interest: CompoundInterest) -> float:
        return self.present_worth(interest) * ap(interest.to_effective().rate, self.maturity)

    @classmethod
    def from_rate(cls, face: float, rate: float, period_count: float, maturity: float) -> Bond:
        """Creates the bond from the coupon rate.

        :param face: The face value.
        :param rate: The coupon rate.
        :param period_count: The period count.
        :param maturity: The maturity of the bond.
        :return: The created bond.
        """
        return Bond(face, face * rate / period_count, period_count, maturity)


class Mortgage(Instrument):
    """Mortgage is the class for mortgages."""

    def __init__(self, principal: float, frequency: float = 12, amortization: float = 25):
        self.principal = principal
        self.frequency = frequency
        self.amortization = amortization

    def cash_flows(self, interest: CompoundInterest) -> Iterator[CashFlow]:
        payment = self.payment(interest)

        return (CashFlow(t, payment) for t in frange(0, self.amortization, 1 / self.frequency))

    def present_worth(self, interest: Optional[CompoundInterest] = None) -> float:
        return 0

    def annual_worth(self, interest: Optional[CompoundInterest] = None) -> float:
        return 0

    def payment(self, interest: CompoundInterest) -> float:
        """Calculates the payment value with respect to the given interest value.

        :param interest: The interest value.
        :return: The payment.
        """
        return self.principal * ap(interest.to_subperiod(self.frequency).rate, self.frequency * self.amortization)

    def pay(self, interest: CompoundInterest, term: float, payment: Optional[float] = None) -> Mortgage:
        """Creates a new mortgage instance assuming payments were made.

        :param interest: The interest value.
        :param term: The term during which payments were made.
        :param payment: The optional payment made, defaults to payment with respect to the interest.
        :return: The next mortgage instance.
        """
        if payment is None:
            return self.pay(interest, term, self.payment(interest))
        else:
            return Mortgage(
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

    def __init__(self, initial: float, annuity: float, final: float, life: float):
        self.initial = initial
        self.annuity = annuity
        self.final = final
        self.life = life

    def cash_flows(self, interest: Optional[CompoundInterest] = None) -> Iterator[CashFlow]:
        return chain((CashFlow(0, self.initial),), (CashFlow(t + 1, self.annuity) for t in frange(self.life)),
                     (CashFlow(self.life, self.final),))

    def present_worth(self, interest: CompoundInterest) -> float:
        rate = interest.to_effective().rate

        return self.initial + self.annuity * pa(rate, self.life) + self.final * fp(rate, self.life)

    def annual_worth(self, interest: CompoundInterest) -> float:
        rate = interest.to_effective().rate

        return self.initial * ap(rate, self.life) + self.annuity + self.final * af(rate, self.life)

    def rep_present_worth(self, interest: CompoundInterest, total_life: float) -> float:
        """Calculates the repeated present worth of this project given total life.

        :param interest: The interest value.
        :param total_life: The total life during which the project is repeated.
        :return: The repeated present worth of this project.
        """
        present_worth = self.present_worth(interest)

        return sum(present_worth * interest.to_factor(t) for t in frange(0, total_life, self.life))


class Relationship(Enum):
    """Relationship is the enum class for all relationships of alternative projects."""
    INDEPENDENT = 0
    MUTUALLY_EXCLUSIVE = 1
    RELATED = 2


@retain_iter
def relationship(values: Iterable[float], budget: float) -> Relationship:
    """Determines the relationship of values with respect to the budget.

    :param values: The values.
    :param budget: The budget.
    :return: The relationship.
    """
    if sum(values) <= budget:
        return Relationship.INDEPENDENT
    elif sum(sorted(values)[:2]) <= budget:
        return Relationship.RELATED
    else:
        return Relationship.MUTUALLY_EXCLUSIVE


def related_combinations(values: Iterable[float], budget: float) -> Iterator[Iterator[int]]:
    """Gets the combinations of the related values given their values and the budget.

    :param values: The values of the projects.
    :param budget: The budget.
    :return: The combinations of possible projects that can be chosen.
    """
    if values := tuple(values):
        i = len(values) - 1
        chosen = related_combinations(values[:i], budget - values[i]) if values[i] <= budget else ()
        skipped = related_combinations(values[:i], budget)

        return chain((chain(sub_combination, [i]) for sub_combination in chosen), skipped)
    else:
        return iter((iter(()),))


def from_table(table: Iterable[Iterable[float]], marr: float) -> int:  # TODO ACCEPT irrs
    """Selects the project with respect to the given table of internal rate of returns and marr.

    :param table: The table of internal rate of returns.
    :param marr: The minimum acceptable rate of return.
    :return: The best project.
    """
    x = 0

    for i, row in enumerate(table):
        if i and iindex(row, x) > marr:
            x = i

    return x
