from abc import ABC, abstractmethod

import numpy.typing as npt


class Field(ABC):
    @abstractmethod
    def intensity(self, v: npt.ArrayLike) -> npt.ArrayLike:
        ...

    @abstractmethod
    def potential(self, v: npt.ArrayLike) -> npt.ArrayLike:
        ...
