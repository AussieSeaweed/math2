from abc import ABC, abstractmethod
from collections.abc import Callable

from math2.calculus.typing import _I
from math2.linear import Vector


class Region(ABC):
    @abstractmethod
    def integral(self, f: Callable[[Vector], _I]) -> _I:
        pass
