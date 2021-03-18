from abc import ABC, abstractmethod
from collections import defaultdict, deque
from math import inf

from math2.graph.exceptions import NegativeCycleError


class SingleSourceTraversal(ABC):
    def __init__(self, graph, source):
        self.graph = graph
        self.source = source

        self._preds = defaultdict(lambda: None)

        self._traverse()

    def predecessor(self, node):
        return self._preds[node]

    def visited(self, node):
        return node == self.source or self._preds[node] is not None

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


class DepthFirstSearch(SingleSourceTraversal):
    def _dfs(self, node):
        for edge in self.graph.edges(node):
            if not self.visited(other := edge.other(node)):
                self._preds[other] = node

                self._dfs(other)

    def _traverse(self):
        self._dfs(self.source)


class SingleSourceShortestPath(SingleSourceTraversal, ABC):
    def __init__(self, graph, source):
        self._dists = defaultdict(lambda: inf)

        super().__init__(graph, source)

    def distance(self, node):
        return self._dists[node]


class BreadthFirstSearch(SingleSourceShortestPath):
    def _traverse(self):
        self._dists[self.source] = 0

        queue = deque((self.source,))

        while queue:
            node = queue.popleft()

            for edge in self.graph.edges(node):
                if not self.visited(other := edge.other(node)):
                    self._dists[other] = self._dists[node] + 1
                    self._preds[other] = node

                    queue.append(other)


class ShortestPathFaster(SingleSourceShortestPath):
    def _traverse(self):
        self._dists[self.source] = 0

        queue = deque((self.source,))
        queued = {self.source}

        while queue:
            node = queue.popleft()
            queued.remove(node)

            for edge in self.graph.edges(node):
                other = edge.other(node)

                if self._dists[other] > self._dists[node] + edge.weight:
                    self._dists[other] = self._dists[node] + edge.weight
                    self._preds[other] = node

                    if other not in queued:
                        queue.append(other)
                        queued.add(other)


class BellmanFord(SingleSourceShortestPath):
    def _traverse(self):
        self._dists[self.source] = 0

        for _ in range(self.graph.node_count - 1):
            for edge in self.graph.edges():
                if self._dists[edge.u] > self._dists[edge.v] + edge.weight:
                    self._dists[edge.u] = self._dists[edge.v] + edge.weight
                    self._preds[edge.u] = edge.v

                if not edge.directed and self._dists[edge.v] > self._dists[edge.u] + edge.weight:
                    self._dists[edge.v] = self._dists[edge.u] + edge.weight
                    self._preds[edge.v] = edge.u
        else:
            for edge in self.graph.edges():
                if self._dists[edge.u] > self._dists[edge.v] + edge.weight or (
                        not edge.directed and self._dists[edge.v] > self._dists[edge.u] + edge.weight):
                    raise NegativeCycleError('The graph contains a negative-weight cycle')
