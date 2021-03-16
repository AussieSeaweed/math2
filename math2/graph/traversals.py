from abc import ABC, abstractmethod
from collections import deque


class Traverser(ABC):
    def __init__(self, graph, source):
        self.graph = graph
        self.source = source

        self._traverse()

    @abstractmethod
    def visited(self, node):
        pass

    @abstractmethod
    def _traverse(self):
        pass


class DepthFirstSearcher(Traverser):
    def __init__(self, graph, source):
        self.__reached = set()

        super().__init__(graph, source)

    def visited(self, node):
        return node in self.__reached

    def _traverse(self):
        self.__dfs(self.source)

    def __dfs(self, node):
        self.__reached.add(node)

        for edge in self.graph.edges(node):
            if not self.visited(other := edge.other(node)):
                self.__dfs(other)


class BreadthFirstSearcher(Traverser):
    def __init__(self, graph, source):
        self.__dists = {}

        super().__init__(graph, source)

    def visited(self, node):
        return node in self.__dists

    def distance(self, node):
        try:
            return self.__dists[node]
        except KeyError:
            raise ValueError('The node not is not reached')

    def _traverse(self):
        self.__dists[self.source] = 0
        queue = deque((self.source,))

        while queue:
            node = queue.popleft()

            for edge in self.graph.edges(node):
                if not self.visited(other := edge.other(node)):
                    self.__dists[other] = self.__dists[node] + 1
                    queue.append(other)
