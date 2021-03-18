from abc import ABC, abstractmethod
from collections import defaultdict, deque
from math import inf, isfinite


class SingleSourceTraverser(ABC):
    def __init__(self, graph, source):
        self.graph = graph
        self.source = source

        self._dists = defaultdict(lambda: inf)
        self._preds = defaultdict(lambda: None)

        self._traverse()

    def visited(self, node):
        return isfinite(self._dists[node])

    def distance(self, node):
        return self._dists[node]

    def path(self, node):
        if not self.visited(node):
            raise ValueError('The node is not reachable')

        path = []

        while node is not None:
            path.append(node)
            node = self._preds[node]

        return reversed(path)

    @abstractmethod
    def _traverse(self):
        pass


class DepthFirstSearcher(SingleSourceTraverser):
    def _traverse(self):
        self.__dfs(self.source, 0)

    def __dfs(self, node, dist):
        self._dists[node] = dist

        for edge in self.graph.edges(node):
            if not self.visited(other := edge.other(node)):
                self.__dfs(other, dist + 1)


class BreadthFirstSearcher(SingleSourceTraverser):
    def _traverse(self):
        self._dists[self.source] = 0
        queue = deque((self.source,))

        while queue:
            node = queue.popleft()

            for edge in self.graph.edges(node):
                if not self.visited(other := edge.other(node)):
                    self._dists[other] = self._dists[node] + 1
                    queue.append(other)
