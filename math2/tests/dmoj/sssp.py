from math import isinf

from math2.graph import EdgeList, Edge, BellmanFord

N, M = map(int, input().split())

graph = EdgeList()

for _ in range(M):
    u, v, w = map(int, input().split())

    graph.add(Edge(u, v, weight=w))

spf = BellmanFord(graph, 1)

for i in range(1, N + 1):
    dist = spf.distance(i)

    print(-1 if isinf(dist) else dist)
