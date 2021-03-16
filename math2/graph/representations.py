from abc import ABC, abstractmethod
from collections import defaultdict
from functools import partial


class Representation(ABC):
    @abstractmethod
    def add(self, from_, to, edge):
        pass

    @abstractmethod
    def edges(self, from_=None, to=None):
        pass


class AdjacencyMatrix(Representation):
    def __init__(self):
        self.__adj_matrix = defaultdict(partial(defaultdict, list))

    def add(self, from_, to, edge):
        self.__adj_matrix[from_][to].append(edge)

    def edges(self, from_=None, to=None):
        if from_ is None and to is None:
            edges = set()

            for adj_lists in self.__adj_matrix.values():
                for adj_list in adj_lists.values():
                    edges |= set(adj_list)

            return iter(edges)
        elif from_ is None:
            edges = set()

            for adj_lists in self.__adj_matrix.values():
                edges |= set(adj_lists[to])

            return iter(edges)
        elif to is None:
            edges = set()

            for adj_list in self.__adj_matrix[from_].values():
                edges |= set(adj_list)

            return iter(edges)
        else:
            return iter(self.__adj_matrix[from_][to])


class AdjacencyLists(Representation):
    def __init__(self):
        self.__adj_lists = defaultdict(list)

    def add(self, from_, to, edge):
        self.__adj_lists[from_].append(edge)

    def edges(self, from_=None, to=None):
        if from_ is None and to is None:
            edges = set()

            for adj_list in self.__adj_lists.values():
                edges |= set(adj_list)

            return iter(edges)
        elif from_ is None:
            edges = set()

            for node, adj_list in self.__adj_lists.items():
                if node == to:
                    edges |= set(edge for edge in adj_list if (to, to) == edge.endpoints)
                else:
                    edges |= set(edge for edge in adj_list if to in edge.endpoints)

            return iter(edges)
        elif to is None:
            return iter(self.__adj_lists[from_])
        else:
            return (edge for edge in self.__adj_lists[from_] if to in edge.endpoints)
