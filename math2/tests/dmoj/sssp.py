from math import isinf

from math2.graph import AdjacencyLists, Edge, ShortestPathFaster

N, M = map(int, input().split())

graph = AdjacencyLists()

for _ in range(M):
    u, v, w = map(int, input().split())

    graph.add(Edge(u, v, weight=w))

spf = ShortestPathFaster(graph, 1)

for i in range(1, N + 1):
    dist = spf.distance(i)

    print(-1 if isinf(dist) else dist)
