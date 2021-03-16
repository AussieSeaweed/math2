from math2.graph import AdjacencyList, DepthFirstSearcher, Edge, UndirectedGraph

N, M, A, B = map(int, input().split())
graph = UndirectedGraph(AdjacencyList[Edge[int]]())

for _ in range(M):
    graph.add(Edge(*map(int, input().split())))

dfs = DepthFirstSearcher(graph, A)

print('GO SHAHIR!' if dfs.visited(B) else 'NO SHAHIR!')
