from abc import ABC, abstractmethod
from collections.abc import Hashable, Iterator
from typing import Generic, overload

from math2.graph.typing import _E


class Representation(Generic[_E], ABC):
    @abstractmethod
    def add(self, from_: Hashable, to: Hashable, edge: _E) -> None:
        pass

    @overload
    def edges(self) -> Iterator[_E]: ...

    @overload
    def edges(self, from_: Hashable) -> Iterator[_E]: ...

    @overload
    def edges(self, from_: Hashable, to: Hashable) -> Iterator[_E]: ...

    @abstractmethod
    def edges(self, from_: Hashable = None, to: Hashable = None) -> Iterator[_E]:
        pass


class EdgeList(Representation[_E]):
    def __init__(self) -> None:
        self.__edges = list[_E]()

    def add(self, from_: Hashable, to: Hashable, edge: _E) -> None:
        self.__edges.append(edge)

    def edges(self, from_: Hashable = None, to: Hashable = None) -> Iterator[_E]:
        if from_ is None and to is None:
            return iter(self.__edges)
        elif to is None:
            return (edge for edge in self.__edges if from_ in edge.endpoints)
        else:
            return (edge for edge in self.__edges if from_ in edge.endpoints and to in edge.endpoints)


class AdjacencyMatrix(Representation[_E]):
    def __init__(self) -> None:
        self.__adj_matrix = dict[Hashable, dict[Hashable, list[_E]]]()

    def add(self, from_: Hashable, to: Hashable, edge: _E) -> None:
        if from_ not in self.__adj_matrix:
            self.__adj_matrix[from_] = {}

        if to not in self.__adj_matrix[from_]:
            self.__adj_matrix[from_][to] = []

        self.__adj_matrix[from_][to].append(edge)

    def edges(self, from_: Hashable = None, to: Hashable = None) -> Iterator[_E]:
        if from_ is None and to is None:
            edges = set()

            for adj_lists in self.__adj_matrix.values():
                for adj_list in adj_lists.values():
                    edges |= adj_list

            return iter(edges)
        elif to is None:
            edges = set()

            for adj_list in self.__adj_matrix[from_].values():
                edges |= adj_list

            return iter(edges)
        else:
            return iter(self.__adj_matrix[from_][to])


class AdjacencyList(Representation[_E]):
    def __init__(self) -> None:
        self.__adj_lists = dict[Hashable, list[_E]]()

    def add(self, from_: Hashable, to: Hashable, edge: _E) -> None:
        if from_ not in self.__adj_lists:
            self.__adj_lists[from_] = []

        self.__adj_lists[from_].append(edge)

    def edges(self, from_: Hashable = None, to: Hashable = None) -> Iterator[_E]:
        if from_ is None and to is None:
            edges = set()

            for adj_list in self.__adj_lists.values():
                edges |= adj_list

            return iter(edges)
        elif to is None:
            return iter(self.__adj_lists[from_])
        else:
            return (edge for edge in self.__adj_lists[from_] if to in edge.endpoints)
