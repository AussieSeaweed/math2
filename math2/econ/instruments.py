from __future__ import annotations

from abc import ABC
from functools import cached_property
from typing import Optional, overload

from math2.econ.factors import ap, fa, fp, pa, pf
from math2.econ.interests import CompoundInterest


class Instrument(ABC):
    ...


class Bond(Instrument):
    def __init__(self, face: float, payment: float, period_count: float, maturity: float):
        self.face = face
        self.payment = payment
        self.period_count = period_count
        self.maturity = maturity

    @cached_property
    def period(self) -> float:
        return 1 / self.period_count

    def present_worth(self, yield_: float) -> float:
        return self.payment * pa(yield_ / self.period_count, self.maturity * self.period_count) + self.face \
               * pf(yield_ / self.period_count, self.maturity * self.period_count)

    @classmethod
    def from_rate(cls, face: float, rate: float, period_count: float, maturity: float) -> Bond:
        return Bond(face, face * rate / period_count, period_count, maturity)


class Mortgage(Instrument):
    def __init__(self, principal: float, term: float, amortization: float):
        self.principal = principal
        self.term = term
        self.amortization = amortization

    def payment(self, interest: CompoundInterest) -> float:
        return self.principal * ap(interest.to_subperiod(12).rate, self.amortization * 12)

    @overload
    def pay(self, interest: CompoundInterest) -> Mortgage:
        ...

    @overload
    def pay(self, interest: CompoundInterest, payment: float) -> Mortgage:
        ...

    def pay(self, interest: CompoundInterest, payment: Optional[float] = None) -> Mortgage:
        if payment is None:
            return Mortgage(self.principal * fp(interest.to_subperiod(12).rate, self.term * 12)
                            - self.payment(interest) * fa(interest.to_subperiod(12).rate, self.term * 12), self.term,
                            self.amortization - self.term)
        else:
            return Mortgage(self.principal * fp(interest.to_subperiod(12).rate, self.term * 12) - payment
                            * fa(interest.to_subperiod(12).rate, self.term * 12), self.term,
                            self.amortization - self.term)

    @classmethod
    def from_down(cls, value: float, down: float, term: float, amortization: float) -> Mortgage:
        return cls(value - down, term, amortization)

    @classmethod
    def from_dtv(cls, value: float, dtv: float, term: float, amortization: float) -> Mortgage:
        return cls.from_down(value, value * dtv, term, amortization)

    @classmethod
    def from_ltv(cls, value: float, ltv: float, term: float, amortization: float) -> Mortgage:
        return cls(value * ltv, term, amortization)


class Project:
    def __init__(self, first: float, salvage: float, a_benefit: float, a_cost: float, life: float):
        self.first = first
        self.salvage = salvage
        self.a_benefit = a_benefit
        self.a_cost = a_cost
        self.life = life

    def present_worth(self, marr: float) -> float:
        return -self.first + self.salvage * fp(marr, self.life) + (self.a_benefit - self.a_cost) * pa(marr, self.life)

    def repeated_present_worth(self, marr: float, total_life: float) -> float:
        present_worth = self.present_worth(marr)

        return sum(present_worth * pf(marr, n) for n in frange(0, total_life, self.life))

    def annual_worth(self, marr: float) -> float:
        return -self.first * ap(marr, self.life) + self.salvage * af(marr, self.life) + self.a_benefit - self.a_cost

    def acceptable_present(self, marr: float) -> bool:
        return self.present_worth(marr) > 0

    def acceptable_repeated_present(self, marr: float, total_life: float) -> bool:
        return self.repeated_present_worth(marr, total_life) > 0

    def acceptable_annual(self, marr: float) -> bool:
        return self.annual_worth(marr) > 0


class SimpleProject:
    def __init__(self, fc: float, a_savings: float, life: float):
        self.fc = fc
        self.a_savings = a_savings
        self.life = life

    @property
    def cash_flows(self) -> Iterator[float]:
        return chain([self.fc], [self.a_savings for _ in frange(self.life)])

    @property
    def irr(self) -> float:
        return irr(self.cash_flows, 0.1)
