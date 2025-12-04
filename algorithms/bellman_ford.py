import math

def bellman_ford(graph, s, t):
    n = graph.n
    INF = math.inf

    dist = [INF] * n
    dist[s] = 0

    prev_node = [-1] * n
    prev_edge = [-1] * n

    # relax n - 1 times
    updated = True
    for _ in range(n - 1):
        if not updated:
            break
        updated = False
        # loop through all edges
        for u in range(n):
            if dist[u] == INF:
                continue
            for idx, e in enumerate(graph.g[u]):
                if e.cap > 0 and dist[e.to] > dist[u] + e.cost:
                    dist[e.to] = dist[u] + e.cost
                    prev_node[e.to] = u
                    prev_edge[e.to] = idx
                    updated = True

    # check negative cycle
    for u in range(n):
        if dist[u] == INF:
            continue
        for e in graph.g[u]:
            if e.cap > 0 and dist[e.to] > dist[u] + e.cost:
                raise RuntimeError("negative cycle detected")

    if dist[t] == INF:
        return None

    return dist, prev_node, prev_edge