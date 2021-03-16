from abc import ABC


class Graph(ABC):
    def __init__(self, repr_):
        self._repr = repr_
        self._nodes = set()

    @property
    def nodes(self):
        return iter(self._nodes)

    def edges(self, from_=None, to=None):
        return self._repr.edges(from_, to)

    def add(self, edge):
        self._nodes.add(edge.u)
        self._nodes.add(edge.v)


class DirectedGraph(Graph):
    def add(self, edge):
        super().add(edge)

        self._repr.add(edge.u, edge.v, edge)


class UndirectedGraph(DirectedGraph):
    def add(self, edge):
        super().add(edge)

        self._repr.add(edge.v, edge.u, edge)
