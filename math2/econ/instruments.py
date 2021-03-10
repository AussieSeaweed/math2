from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from enum import Enum
from itertools import chain
from typing import Any, Optional

from auxiliary import default, iindex, ilen, retain_iter

from math2.consts import EPS
from math2.econ.cashflows import CashFlow, irr
from math2.econ.factors import ap, fa
from math2.econ.ints import CompInt, EfInt
from math2.misc import frange


class Instrument(ABC):
    """Instrument is the abstract base class for all financial instruments."""

    @property
    @abstractmethod
    def cash_flows(self) -> Iterator[CashFlow]:
        """
        :return: The cash flows of this instrument.
        """
        pass


class Bond(Instrument):
    """Bond is the class for bonds."""

    def __init__(self, face: float, coupon: float, frequency: float, maturity: float):
        self.face = face
        self.coupon = coupon
        self.frequency = frequency
        self.maturity = maturity

    @property
    def cash_flows(self) -> Iterator[CashFlow]:
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

    def __init__(self, principal: float, int_: CompInt, freq: float = 12, term: float = 5, amort: float = 25):
        self.principal = principal
        self.int = int_
        self.freq = freq
        self.term = term
        self.amort = amort

    @property
    def cash_flows(self) -> Iterator[CashFlow]:
        return chain(
            (CashFlow(0, -self.principal),),
            (CashFlow(t, self.payment) for t in frange(1 / self.freq, self.amort + EPS, 1 / self.freq)),
        )

    @property
    def payment(self) -> float:
        """
        :return: The mortgage payment.
        """
        return self.principal * ap(self.int.to_sp(self.freq).rate, self.freq * self.amort)

    def pay(self, term: Optional[float] = None, payment: Optional[float] = None) -> Mortgage:
        """Creates a new mortgage instance assuming payments were made.

        :param term: The term during which payments were made.
        :param payment: The optional payment made, defaults to payment with respect to the interest.
        :return: The next mortgage instance.
        """
        term = default(term, self.term)
        payment = default(payment, self.payment)

        return Mortgage(
            self.principal * self.int.to_factor(term) - payment * fa(self.int.to_sp(self.freq).rate, term * self.freq),
            self.int, self.freq, self.term, self.amort - term,
        )

    @classmethod
    def from_down(cls, value: float, down: float, int_: CompInt, freq: float = 12, term: float = 5,
                  amort: float = 25) -> Mortgage:
        """Constructs the mortgage instance from the down payment value.

        :param value: The total value.
        :param down: The down payment.
        :param int_: The interest rate.
        :param freq: The frequency of payments, defaults to 12.
        :param term: The term, defaults = 5.
        :param amort: The amortization of the mortgage, defaults to 25.
        :return: The constructed mortgage instance.
        """
        return cls(value - down, int_, freq, term, amort)

    @classmethod
    def from_dtv(cls, value: float, dtv: float, int_: CompInt, freq: float = 12, term: float = 5,
                 amort: float = 25) -> Mortgage:
        """Constructs the mortgage instance from the down payment to value percentage.

        :param value: The total value.
        :param dtv: The down payment to value percentage.
        :param int_: The interest rate.
        :param freq: The frequency of payments, defaults to 12.
        :param term: The term, defaults = 5.
        :param amort: The amortization of the mortgage, defaults to 25.
        :return: The constructed mortgage instance.
        """
        return cls.from_down(value, value * dtv, int_, freq, term, amort)

    @classmethod
    def from_ltv(cls, value: float, ltv: float, int_: CompInt, freq: float = 12, term: float = 5,
                 amort: float = 25) -> Mortgage:
        """Constructs the mortgage instance from the loan payment to value percentage.

        :param value: The total value.
        :param ltv: The loan payment to value percentage.
        :param int_: The interest rate.
        :param freq: The frequency of payments, defaults to 12.
        :param term: The term, defaults = 5.
        :param amort: The amortization of the mortgage, defaults to 25.
        :return: The constructed mortgage instance.
        """
        return cls(value * ltv, int_, freq, term, amort)


class Project(Instrument):
    """Project is the class for projects."""

    def __init__(self, initial: float, annuity: float, final: float, life: float):
        self.initial = initial
        self.annuity = annuity
        self.final = final
        self.life = life

    def __sub__(self, other: Any) -> Project:
        if isinstance(other, Project):
            return Project(
                self.initial - other.initial, self.annuity - other.annuity, self.final - other.final, self.life)
        else:
            return NotImplemented

    @property
    def cash_flows(self) -> Iterator[CashFlow]:
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

        return chain((chain(sub_combination, (i,)) for sub_combination in chosen), skipped)
    else:
        return iter((iter(()),))


def de_facto_marr(costs: Iterable[float], irrs: Iterable[CompInt], budget: float) -> CompInt:
    """Calculates the de factor marr of the given projects based on costs and irrs.

    :param costs: The costs.
    :param irrs: The internal rate of returns.
    :param budget: The budget.
    :return: The de factor marr.
    """
    costs = tuple(costs)
    irrs = tuple(irrs)
    indices = sorted(range(ilen(costs)), key=irrs.__getitem__, reverse=True)

    cost_sum = 0.0
    marr: CompInt = EfInt(0)

    for i in indices:
        cost_sum += costs[i]

        if cost_sum > budget:
            break

        marr = irrs[i]

    return marr


def select(irrs: Iterable[CompInt], table: Iterable[Iterable[CompInt]], marr: CompInt) -> Optional[int]:
    """Selects the project with respect to the given table of internal rate of returns and marr.

    :param irrs: The irr values of the choices (sorted by their initial cost).
    :param table: The table of internal rate of returns.
    :param marr: The minimum acceptable rate of return.
    :return: The best project.
    """
    try:
        x = next(i for i, irr_ in enumerate(irrs) if irr_ > marr)
    except StopIteration:
        return None

    for i, row in enumerate(table):
        if i > x and iindex(row, x) > marr:
            x = i

    return x


def irr_table(projects: Iterable[Project], init_guess: CompInt) -> Iterator[Iterator[EfInt]]:
    """Creates the irr table from the projects.

    :param projects: The projects.
    :param init_guess: The initial guess.
    :return: The irr table.
    """
    projects = tuple(projects)

    return ((irr((x - y).cash_flows, init_guess) for y in projects[:projects.index(x)]) for x in projects)
