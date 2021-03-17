from collections import deque

from math2.graph.traversals import SingleSourceTraverser


class ShortestPathFaster(SingleSourceTraverser):
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
