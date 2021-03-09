from collections.abc import Iterable, Iterator
from functools import total_ordering
from itertools import accumulate
from math import inf
from typing import Any, Optional

from auxiliary import SupportsLessThan, iindex, ilen, retain_iter, windowed

from math2.calc import newton
from math2.econ.factors import ap
from math2.econ.ints import CompInt, EfInt, Int
from math2.misc import interp


@total_ordering
class CashFlow(SupportsLessThan):
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
    return CashFlow(0, cash_flow.amount / interest.to_factor(cash_flow.time))


def payback(cash_flows: Iterable[CashFlow], cost: float) -> float:
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


def disc_payback(cash_flows: Iterable[CashFlow], cost: float, interest: Int) -> float:
    """Calculates the discounted payback period of the cash flows at the given interest value.

    :param cash_flows: The cash flows.
    :param cost: The cost to pay back.
    :param interest: The interest at which the cash flows are discounted.
    :return: The payback period.
    """
    return payback(map(lambda cash_flow: disc(cash_flow, interest), cash_flows), cost)


def pw(cash_flows: Iterable[CashFlow], i: CompInt) -> float:
    """Calculates the present worth of the supplied cash flows at the interest.

    :param cash_flows: The cash flows.
    :param i: The interest.
    :return: The present worth.
    """
    return sum(disc(cash_flow, i).amount for cash_flow in cash_flows)


@retain_iter
def rpw(cash_flows: Iterable[CashFlow], i: CompInt, total_life: float) -> float:
    """Calculates the repeated present worth of the supplied cash flows at the interest and at the total life.

    :param cash_flows: The cash flows.
    :param i: The interest.
    :param total_life: The total life.
    :return: The repeated present worth.
    """
    life = max(cash_flow.time for cash_flow in cash_flows)
    ret = 0.0

    while max(cash_flow.time for cash_flow in cash_flows) <= total_life:
        ret += pw(cash_flows, i)

        for cash_flow in cash_flows:
            cash_flow.time += life
    else:
        ret += pw((cash_flow for cash_flow in cash_flows if cash_flow.time <= total_life), i)

    return ret


@retain_iter
def aw(cash_flows: Iterable[CashFlow], i: CompInt) -> float:
    """Calculates the annual worth of the supplied cash flows at the interest.

    :param cash_flows: The cash flows.
    :param i: The interest.
    :return: The annual worth.
    """
    return pw(cash_flows, i) * ap(i.to_ef().rate, max(cash_flow.time for cash_flow in cash_flows))


@retain_iter
def irr(cash_flows: Iterable[CashFlow], init_guess: CompInt) -> EfInt:
    """Calculates the internal rate of return using the initial guess.

    :param cash_flows: The cash flows.
    :param init_guess: The initial guess.
    :return: The internal rate of return.
    """
    return EfInt(newton(lambda i: pw(cash_flows, EfInt(i)), init_guess.to_ef().rate))


def de_facto_marr(costs: Iterable[float], irrs: Iterable[float], budget: float) -> float:
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
    marr = 0.0

    for i in indices:
        cost_sum += costs[i]

        if cost_sum > budget:
            break

        marr = irrs[i]

    return marr


def select(irrs: Iterable[float], table: Iterable[Iterable[float]], marr: float) -> Optional[int]:
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
