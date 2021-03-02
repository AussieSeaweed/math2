from enum import Enum
from functools import cached_property, total_ordering
from typing import Any


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
        :return: The index of the enum element
        """
        values: list[OrderedEnum] = list(type(self))

        return values.index(self)
