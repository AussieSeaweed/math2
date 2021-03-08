from typing import TypeVar

from auxiliary import SupportsLessThan

_T = TypeVar('_T')
_SLT = TypeVar('_SLT', bound=SupportsLessThan)
