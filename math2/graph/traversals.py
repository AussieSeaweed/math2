from abc import ABC, abstractmethod
from collections import deque


class Traverser(ABC):
    def __init__(self, graph, source):
        self.graph = graph
        self.source = source
        self._dists = {}

        self._traverse()

    def visited(self, node):
        return node in self._dists

    def distance(self, node):
        return self._dists[node] if self.visited(node) else None

    @abstractmethod
    def _traverse(self):
        pass


class DepthFirstSearcher(Traverser):
    def _traverse(self):
        self.__dfs(self.source, 0)

    def __dfs(self, node, dist):
        self._dists[node] = dist

        for edge in self.graph.edges(node):
            if not self.visited(other := edge.other(node)):
                self.__dfs(other, dist + 1)


class BreadthFirstSearcher(Traverser):
    def _traverse(self):
        self._dists[self.source] = 0
        queue = deque((self.source,))

        while queue:
            node = queue.popleft()

            for edge in self.graph.edges(node):
                if not self.visited(other := edge.other(node)):
                    self._dists[other] = self._dists[node] + 1
                    queue.append(other)
