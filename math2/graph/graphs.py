from abc import ABC, abstractmethod
from collections.abc import Hashable, Iterator
from typing import Generic, overload

from math2.graph.representations import Representation
from math2.graph.typing import _E


class Graph(Generic[_E], ABC):
    def __init__(self, representation: Representation[_E]):
        self._repr = representation

    @overload
    def edges(self) -> Iterator[_E]: ...

    @overload
    def edges(self, from_: Hashable) -> Iterator[_E]: ...

    @overload
    def edges(self, from_: Hashable, to: Hashable) -> Iterator[_E]: ...

    def edges(self, from_: Hashable = None, to: Hashable = None) -> Iterator[_E]:
        return self._repr.edges(from_, to)

    @abstractmethod
    def add(self, edge: _E) -> None:
        pass


class DirectedGraph(Graph[_E]):
    def add(self, edge: _E) -> None:
        self._repr.add(edge.u, edge.v, edge)


class UndirectedGraph(DirectedGraph[_E]):
    def add(self, edge: _E) -> None:
        super().add(edge)

        self._repr.add(edge.v, edge.u, edge)
