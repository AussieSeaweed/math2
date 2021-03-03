from collections import Iterable, Iterator, Sequence
from enum import Enum
from functools import reduce
from itertools import chain
from typing import Optional

from math2.calc import newton
from math2.econ.factors import pf
from math2.misc import interpolate
from math2.ntheory import lcm


class Relationship(Enum):
    INDEPENDENT = 0
    MUTUALLY_EXCLUSIVE = 1
    RELATED_BUT_NOT_MUTUALLY_EXCLUSIVE = 2


def relationship(values: Iterable[float], budget: float) -> Relationship:
    if isinstance(values, Sequence):
        if sum(values) <= budget:
            return Relationship.INDEPENDENT
        elif len(values := sorted(values)) >= 2 and values[0] + values[1] > budget:
            return Relationship.MUTUALLY_EXCLUSIVE
        else:
            return Relationship.RELATED_BUT_NOT_MUTUALLY_EXCLUSIVE
    else:
        return relationship(tuple(values), budget)


def combinations(values: Iterable[float], budget: float) -> Iterator[Iterator[int]]:
    if isinstance(values, Sequence):
        if values and values[-1] <= budget:
            i = len(values) - 1

            return chain((chain([i], combination) for combination in combinations(values[:i], budget - values[i])),
                         combinations(values[:-1], budget))
        else:
            return iter([iter(())])
    else:
        return combinations(tuple(values), budget)


def eval_mex_rpw(projects: Iterable[Project], marr: float) -> Optional[Project]:
    projects = tuple(projects)
    total_life = reduce(lcm, (project.life for project in projects))
    choice = max(projects, key=lambda project: project.repeated_present_worth(marr, total_life))

    return choice if choice.acceptable_repeated_present(marr, total_life) else None


def eval_mex_pw(projects: Iterable[Project], marr: float) -> Optional[Project]:
    choice = max(projects, key=lambda project: project.present_worth(marr))

    return choice if choice.acceptable_present(marr) else None


def eval_mex_aw(projects: Iterable[Project], marr: float) -> Optional[Project]:
    choice = max(projects, key=lambda project: project.annual_worth(marr))

    return choice if choice.acceptable_annual(marr) else None


def npv(cash_flows: Iterable[float], i: float) -> float:
    return sum(cash_flow * pf(i, n) for n, cash_flow in enumerate(cash_flows))


def irr(cash_flows: Iterable[float], guess: float) -> float:
    cash_flows = tuple(cash_flows)

    return newton(lambda i: npv(cash_flows, i), guess)


def acceptable_irr(cash_flows: Iterable[float], guess: float, marr: float) -> bool:
    return irr(cash_flows, guess) > marr


def payback_period(fc: float, cash_flows: Iterable[float]) -> float:
    cash_flows = tuple(cash_flows)

    try:
        i = next(i for i in range(len(cash_flows)) if sum(cash_flows[:i]) >= fc)

        if i == 0:
            return i
        else:
            return interpolate(fc, cash_flows[i - 1], cash_flows[i], i - 1, i)
    except StopIteration:
        raise ValueError('Cannot pay back')


def disc_payback_period(fc: float, cash_flows: Iterable[float], marr: float) -> float:
    return payback_period(fc, (cash_flow * pf(marr, n) for n, cash_flow in enumerate(cash_flows)))


def from_table(tbl: Iterable[Sequence[float]], marr: float) -> int:
    tbl = tuple(map(tuple, tbl))
    x = 0

    for i in range(1, len(tbl)):
        if tbl[i][x] > marr:
            x = i

    return x
