from __future__ import annotations

from typing import Any, Protocol, TypeVar, runtime_checkable


@runtime_checkable
class SupportsLessThan(Protocol):
    """SupportsLessThan is the protocol for types that support the less than comparison operator."""

    def __lt__(self, other: Any) -> bool: ...


@runtime_checkable
class SupportsMul(Protocol):
    """SupportsMul is the protocol for types that support the __mul__ operator."""

    def __mul__(self: _SM, other: Any) -> _SM: ...


@runtime_checkable
class Scalar(Protocol):
    """Scalar is the protocol for types that support scalar operations."""

    def __pos__(self: _S) -> _S: ...

    def __neg__(self: _S) -> _S: ...

    def __add__(self: _S, other: Any) -> _S: ...

    def __radd__(self: _S, other: Any) -> _S: ...

    def __sub__(self: _S, other: Any) -> _S: ...

    def __rsub__(self: _S, other: Any) -> _S: ...

    def __mul__(self: _S, other: Any) -> _S: ...

    def __rmul__(self: _S, other: Any) -> _S: ...

    def __truediv__(self: _S, other: Any) -> _S: ...

    def __rtruediv__(self: _S, other: Any) -> _S: ...

    def __pow__(self: _S, other: Any) -> _S: ...

    def __rpow__(self: _S, other: Any) -> _S: ...


_T = TypeVar('_T')
_SLT = TypeVar('_SLT', bound=SupportsLessThan)
_SM = TypeVar('_SM', bound=SupportsMul)
_S = TypeVar('_S', bound=Scalar)
