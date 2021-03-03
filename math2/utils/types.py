from abc import abstractmethod
from collections import Callable
from enum import Enum
from functools import cached_property, total_ordering
from typing import Any, Protocol, TypeVar, runtime_checkable

_T = TypeVar('_T')
_F = TypeVar('_F', bound=Callable[..., Any])


@total_ordering
class OrderedEnum(Enum):
    """OrderedEnum is the enum class for all ordered enums."""

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.index < other.index
        else:
            return NotImplemented

    @cached_property
    def index(self) -> int:
        """
        :return: The index of the enum element.
        """
        values: list[OrderedEnum] = list(type(self))

        return values.index(self)


@runtime_checkable
class SupportsLessThan(Protocol):
    """SupportsLessThan is the protocol for types that support less than comparison operators."""

    @abstractmethod
    def __lt__(self: _T, other: _T) -> bool:
        ...


@runtime_checkable
class SupportsMul(Protocol):
    """SupportsMul is the protocol for types that support multiplication operators."""

    @abstractmethod
    def __mul__(self: _T, other: _T) -> _T:
        ...
