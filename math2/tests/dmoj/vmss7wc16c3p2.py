from math2.graph import AdjacencyLists, BreadthFirstSearcher, Edge, UndirectedGraph

N, M, A, B = map(int, input().split())
graph = UndirectedGraph(AdjacencyLists())

for _ in range(M):
    graph.add(Edge(*map(int, input().split())))

dfs = BreadthFirstSearcher(graph, A)

print('GO SHAHIR!' if dfs.visited(B) else 'NO SHAHIR!')
