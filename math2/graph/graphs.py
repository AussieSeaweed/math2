from abc import ABC, abstractmethod
from collections import defaultdict
from functools import partial
from itertools import chain


class Edge:
    def __init__(self, u, v, *, directed=False, weight=None, flow=None, capacity=None):
        self.u = u
        self.v = v

        self.directed = directed
        self.weight = weight
        self.flow = flow
        self.capacity = capacity

    @property
    def endpoints(self):
        return self.u, self.v

    def match(self, u, v):
        if u is None and v is None:
            return True
        elif u is None:
            return v == self.v or (not self.directed and v == self.u)
        elif v is None:
            return u == self.u or (not self.directed and u == self.v)
        else:
            return (u, v) == self.endpoints or (not self.directed and (v, u) == self.endpoints)

    def other(self, vertex):
        if vertex == self.u:
            return self.v
        elif vertex == self.v:
            return self.u
        else:
            raise ValueError('The vertex is not one of the endpoints')


class Graph(ABC):
    def __init__(self):
        self.__nodes = set()

    @property
    def nodes(self):
        return iter(self.__nodes)

    def add(self, edge):
        self.__nodes.add(edge.u)
        self.__nodes.add(edge.v)

    @abstractmethod
    def edges(self, from_=None, to=None):
        pass


class EdgeList(Graph):
    def __init__(self):
        super().__init__()

        self.__edge_list = []

    def add(self, edge):
        super().add(edge)

        self.__edge_list.append(edge)

    def edges(self, from_=None, to=None):
        return iter({edge for edge in self.__edge_list if edge.match(from_, to)})


class AdjacencyMatrix(Graph):
    def __init__(self):
        super().__init__()

        self.__adj_matrix = defaultdict(partial(defaultdict, list))

    def add(self, edge):
        super().add(edge)

        self.__adj_matrix[edge.u][edge.v].append(edge)

        if not edge.directed:
            self.__adj_matrix[edge.v][edge.u].append(edge)

    def edges(self, from_=None, to=None):
        edges = set()

        if from_ is None and to is None:
            for adj_lists in self.__adj_matrix.values():
                for adj_list in adj_lists.values():
                    edges |= set(adj_list)
        elif from_ is None:
            for adj_lists in self.__adj_matrix.values():
                edges |= set(adj_lists[to])
        elif to is None:
            for adj_list in self.__adj_matrix[from_].values():
                edges |= set(adj_list)
        else:
            edges = self.__adj_matrix[from_][to]

        return iter(edges)


class AdjacencyLists(Graph):
    def __init__(self):
        super().__init__()

        self.__adj_lists = defaultdict(list)

    def add(self, edge):
        super().add(edge)

        self.__adj_lists[edge.u].append(edge)

        if not edge.directed:
            self.__adj_lists[edge.v].append(edge)

    def edges(self, from_=None, to=None):
        if from_ is None and to is None:
            return iter(set(chain(*(self.edges(node) for node in self.nodes))))
        elif from_ is None:
            return (edge for edge in self.edges() if edge.match(None, to))
        elif to is None:
            return iter(self.__adj_lists[from_])
        else:
            return (edge for edge in self.__adj_lists[from_] if to in edge.endpoints)
