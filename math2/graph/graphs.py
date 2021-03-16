from abc import ABC, abstractmethod


class Graph(ABC):
    def __init__(self, representation):
        self._repr = representation

    def edges(self, from_=None, to=None):
        return self._repr.edges(from_, to)

    @abstractmethod
    def add(self, edge):
        pass


class DirectedGraph(Graph):
    def add(self, edge):
        self._repr.add(edge.u, edge.v, edge)


class UndirectedGraph(DirectedGraph):
    def add(self, edge):
        super().add(edge)

        self._repr.add(edge.v, edge.u, edge)
