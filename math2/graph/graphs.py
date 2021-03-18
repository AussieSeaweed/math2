from abc import ABC, abstractmethod
from collections import defaultdict
from functools import partial

from auxiliary import default


class Edge:
    def __init__(self, u, v, *, weight=None, capacity=None):
        self.u = u
        self.v = v

        self.weight = weight
        self.capacity = capacity

        self.flow = 0

    def invert(self):
        return Edge(self.v, self.u, weight=self.weight, capacity=self.capacity)

    def match(self, u, v):
        return default(u, self.u) == self.u and default(v, self.v) == self.v

    def other(self, vertex):
        if vertex == self.u:
            return self.v
        elif vertex == self.v:
            return self.u
        else:
            raise ValueError('The vertex is not one of the endpoints')

    def residual_capacity(self, vertex):
        if vertex == self.u:
            return self.flow
        elif vertex == self.v:
            return self.capacity - self.flow
        else:
            raise ValueError('The vertex is not one of the endpoints')

    def add_residual_capacity(self, vertex, delta):
        if vertex == self.u:
            self.flow -= delta
        elif vertex == self.v:
            self.flow += delta
        else:
            raise ValueError('The vertex is not one of the endpoints')


class Graph(ABC):
    def __init__(self):
        self.__nodes = set()

    @property
    def nodes(self):
        return iter(self.__nodes)

    @property
    def node_count(self):
        return len(self.__nodes)

    def add(self, edge, *, directed=False):
        self.__nodes.add(edge.u)
        self.__nodes.add(edge.v)

    @abstractmethod
    def edges(self, from_=None, to=None):
        pass


class EdgeList(Graph):
    def __init__(self):
        super().__init__()

        self.__edges = []

    def add(self, edge, *, directed=False):
        super().add(edge, directed=directed)

        self.__edges.append(edge)

        if not directed:
            self.__edges.append(edge.invert())

    def edges(self, from_=None, to=None):
        return (edge for edge in self.__edges if edge.match(from_, to))


class AdjacencyMatrix(Graph):
    def __init__(self):
        super().__init__()

        self.__matrix = defaultdict(partial(defaultdict, list))

    def add(self, edge, *, directed=False):
        super().add(edge, directed=directed)

        self.__matrix[edge.u][edge.v].append(edge)

        if not edge.directed:
            self.__matrix[edge.v][edge.u].append(edge.invert())

    def edges(self, from_=None, to=None):
        edges = []

        if from_ is None and to is None:
            for adj_lists in self.__matrix.values():
                for adj_list in adj_lists:
                    edges.extend(adj_list)
        elif from_ is None:
            for adj_lists in self.__matrix.values():
                edges.extend(adj_lists[to])
        elif to is None:
            for adj_list in self.__matrix[from_].values():
                edges.extend(adj_list)
        else:
            edges = self.__matrix[from_][to]

        return iter(edges)


class AdjacencyLists(Graph):
    def __init__(self):
        super().__init__()

        self.__lists = defaultdict(list)

    def add(self, edge, *, directed=False):
        super().add(edge, directed=directed)

        self.__lists[edge.u].append(edge)

        if not edge.directed:
            self.__lists[edge.v].append(edge.inverted)

    def edges(self, from_=None, to=None):
        if from_ is None and to is None:
            edges = []

            for adj_list in self.__lists.values():
                edges.extend(adj_list)

            return iter(edges)
        elif from_ is None:
            return (edge for edge in self.edges() if edge.match(None, to))
        elif to is None:
            return iter(self.__lists[from_])
        else:
            return (edge for edge in self.edges(from_) if edge.match(from_, to))
