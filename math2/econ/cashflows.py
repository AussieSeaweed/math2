from collections.abc import Iterable
from functools import total_ordering
from itertools import accumulate
from math import inf
from typing import Any

from auxiliary import retain_iter, windowed

from math2.calc import newton
from math2.econ.ints import EfInt, Int
from math2.misc import interp


@total_ordering
class CashFlow:
    """CashFlow is the class for cash flows."""

    def __init__(self, time: float, amount: float):
        self.time = time
        self.amount = amount

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, CashFlow):
            return self.time == other.time
        else:
            return NotImplemented

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, CashFlow):
            return self.time < other.time
        else:
            return NotImplemented


def disc(cash_flow: CashFlow, interest: Int) -> CashFlow:
    """Discounts the cash flow from a copied value.

    :param cash_flow: The cash flow.
    :param interest: The interest at which is discounted.
    :return: The discounted copy of the cash flow.
    """
    return CashFlow(cash_flow.time, cash_flow.amount / interest.to_factor(cash_flow.time))


def npv(cash_flows: Iterable[CashFlow], interest: Int) -> float:
    """Calculates the net present value of the supplied cash flows at the interest.

    :param cash_flows: The cash flows.
    :param interest: The interest.
    :return: The net present value.
    """
    return sum(disc(cash_flow, interest).amount for cash_flow in cash_flows)


@retain_iter
def irr(cash_flows: Iterable[CashFlow], initial_guess: float) -> EfInt:
    """Calculates the internal rate of return using the initial guess.

    :param cash_flows: The cash flows.
    :param initial_guess: The initial guess.
    :return: The internal rate of return.
    """
    return EfInt(newton(lambda i: npv(cash_flows, EfInt(i)), initial_guess))


def payback_period(cash_flows: Iterable[CashFlow], cost: float) -> float:
    """Calculates the payback period of the cash flows.

    :param cash_flows: The cash flows.
    :param cost: The cost to pay back.
    :return: The payback period.
    """
    prefix_sums = tuple(accumulate(cash_flow.amount for cash_flow in sorted(cash_flows)))

    if cost <= 0 or prefix_sums and cost <= prefix_sums[0]:
        return 0
    else:
        for i, (x, y) in enumerate(windowed(prefix_sums, 2)):
            if y >= cost:
                return interp(cost, x, y, i, i + 1)
        else:
            return inf


def disc_payback_period(cash_flows: Iterable[CashFlow], cost: float, interest: Int) -> float:
    """Calculates the discounted payback period of the cash flows at the given interest value.

    :param cash_flows: The cash flows.
    :param cost: The cost to pay back.
    :param interest: The interest at which the cash flows are discounted.
    :return: The payback period.
    """
    return payback_period(map(lambda cash_flow: disc(cash_flow, interest), cash_flows), cost)
