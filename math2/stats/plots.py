from collections.abc import Iterable, Iterator

from math2.stats.analysis import interquartile_range, median
from math2.typing import _S


class BoxAndWhiskerPlot:
    def __init__(self, values: Iterable[_S], multiple: float = 1.5):
        self.values = tuple(values)
        self.multiple = multiple

    @property
    def boundaries(self) -> tuple[_S, _S]:
        mu = median(self.values)
        qr = interquartile_range(self.values)
        valid = tuple(x for x in self.values if mu - qr * self.multiple <= x <= mu + qr * self.multiple)

        return min(valid), max(valid)

    @property
    def outliers(self) -> Iterator[_S]:
        return (x for x in self.values if x < self.boundaries[0] or self.boundaries[1] < x)
