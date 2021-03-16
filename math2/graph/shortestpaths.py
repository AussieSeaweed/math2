from abc import ABC
from collections import deque

from math2.graph.traversals import SingleSourceTraverser, MultipleSourceTraverser


class SingleSourceShortestPath(SingleSourceTraverser, ABC):
    pass


class BellmanFord(SingleSourceShortestPath):
    def _traverse(self):
        self._dists[self.source] = 0

        for node in range(len(self.graph.nodes) - 1):
            self._iterate()

    def _iterate(self):
        pass


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

                if self._dists[self.source] + edge.weight < self._dists[other]:
                    self._dists[other] = self._dists[self.source] + edge.weight

                    if other in queued:
                        queue.append(other)


class MultipleSourceShortestPath(MultipleSourceTraverser, ABC):
    pass
