from collections.abc import Hashable
from typing import Any, Protocol, TypeVar


class Scalar(Protocol):
    def __lt__(self, other: Any) -> bool: ...

    def __add__(self, other: Any) -> Any: ...


_T = TypeVar('_T')
_S = TypeVar('_S', bound=Scalar)
_H = TypeVar('_H', bound=Hashable)
