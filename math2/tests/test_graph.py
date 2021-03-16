from itertools import chain
from random import choice
from unittest import main

from auxiliary import ExtendedTestCase

from math2.graph import (AdjacencyLists, AdjacencyMatrix, BreadthFirstSearcher, DepthFirstSearcher, DirectedGraph, Edge,
                         UndirectedGraph)


class TraversalTestCase(ExtendedTestCase):
    MONTE_CARLO_NODE_COUNT = 100
    MONTE_CARLO_EDGE_COUNT = 100

    def test_monte_carlo(self):
        nodes = range(self.MONTE_CARLO_NODE_COUNT)

        directed_graphs = [DirectedGraph(AdjacencyMatrix()), DirectedGraph(AdjacencyLists())]
        undirected_graphs = [UndirectedGraph(AdjacencyMatrix()), UndirectedGraph(AdjacencyLists())]

        for _ in range(self.MONTE_CARLO_EDGE_COUNT):
            u, v = choice(nodes), choice(nodes)

            for graph in directed_graphs:
                graph.add(Edge(u, v))
                graph.add(Edge(v, u))

            for graph in undirected_graphs:
                graph.add(Edge(u, v))

        for source in nodes:
            visited = None
            distances = None

            for graph in chain(directed_graphs, undirected_graphs):
                dfs = DepthFirstSearcher(graph, source)
                bfs = BreadthFirstSearcher(graph, source)

                if visited is None:
                    visited = tuple(dfs.visited(node) for node in nodes)
                else:
                    self.assertIterableEqual(visited, (dfs.visited(node) for node in nodes))
                    self.assertIterableEqual(visited, (bfs.visited(node) for node in nodes))

                if distances is None:
                    distances = tuple(bfs.distance(node) for node in nodes)
                else:
                    self.assertIterableEqual(distances, (bfs.distance(node) for node in nodes))

    def test_visited(self):
        graph = UndirectedGraph(AdjacencyLists())

        for edge in (Edge(1, 2), Edge(2, 3), Edge(2, 5), Edge(5, 1), Edge(3, 4), Edge(4, 5)):
            graph.add(edge)

        self.assertFalse(DepthFirstSearcher(graph, 1).visited(6))

        graph.add(Edge(4, 6))

        self.assertTrue(DepthFirstSearcher(graph, 1).visited(6))


if __name__ == '__main__':
    main()
