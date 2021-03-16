from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Hashable
from typing import Any

from math2.graph import Graph
from math2.graph.edges import Edge


class Traverser(ABC):
    def __init__(self, graph: Graph[Edge[Any]], source: Hashable):
        self.graph = graph
        self.source = source

        self._traverse()

    @abstractmethod
    def visited(self, node: Hashable) -> bool:
        pass

    @abstractmethod
    def _traverse(self) -> None:
        pass


class DepthFirstSearcher(Traverser):
    def __init__(self, graph: Graph[Edge[Any]], source: Hashable):
        super().__init__(graph, source)

        self.__reached: set[Hashable]

    def visited(self, node: Hashable) -> bool:
        return node in self.__reached

    def _traverse(self) -> None:
        self.__reached = set()

        self.__dfs(self.source)

    def __dfs(self, node: Hashable) -> None:
        self.__reached.add(node)

        for edge in self.graph.edges(node):
            if not self.visited(other := edge.other(node)):
                self.__dfs(other)


class BreadthFirstSearcher(Traverser):
    def __init__(self, graph: Graph[Edge[Any]], source: Hashable):
        super().__init__(graph, source)

        self.__dists: dict[Hashable, int]

    def visited(self, node: Hashable) -> bool:
        return node in self.__dists

    def distance(self, node: Hashable) -> int:
        try:
            return self.__dists[node]
        except KeyError:
            raise ValueError('The node not is not reached')

    def _traverse(self) -> None:
        self.__dists = {self.source: 0}
        queue = deque((self.source,))

        while queue:
            node = queue.popleft()

            for edge in self.graph.edges(node):
                if not self.visited(other := edge.other(node)):
                    self.__dists[other] = self.__dists[node] + 1
                    queue.append(other)
