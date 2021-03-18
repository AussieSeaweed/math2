from math2.graph import AdjacencyLists, BreadthFirstSearch, Edge

N, M, A, B = map(int, input().split())
graph = AdjacencyLists()

for _ in range(M):
    graph.add(Edge(*map(int, input().split())))

dfs = BreadthFirstSearch(graph, A)

print('GO SHAHIR!' if dfs.visited(B) else 'NO SHAHIR!')
