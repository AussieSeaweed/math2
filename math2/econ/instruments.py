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
