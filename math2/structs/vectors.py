from collections import MutableSequence
from typing import Iterable, overload


class Vector(MutableSequence[float]):
    @overload
    def __getitem__(self, i: int) -> float:
        ...

    @overload
    def __getitem__(self, s: slice) -> MutableSequence[float]:
        ...

    def __getitem__(self, i: int) -> float:
        pass

    @overload
    def __setitem__(self, i: int, o: float) -> None:
        ...

    @overload
    def __setitem__(self, s: slice, o: Iterable[float]) -> None:
        ...

    def __setitem__(self, i: int, o: float) -> None:
        pass

    @overload
    def __delitem__(self, i: int) -> None:
        ...

    @overload
    def __delitem__(self, i: slice) -> None:
        ...

    def __delitem__(self, i: int) -> None:
        pass

    def __len__(self) -> int:
        pass

    def insert(self, index: int, value: float) -> None:
        pass
