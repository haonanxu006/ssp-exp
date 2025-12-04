from algorithms.residual_graph import ResidualGraph
import math

def ssp(graph, s, t, sp):
    total_flow = 0
    total_cost = 0

    while True:
        sp_result = sp(graph, s, t)
        if sp_result is None:
            break

        dist, prev_node, prev_edge = sp_result
        
        # find bottleneck
        flow = math.inf
        v = t
        while v != s:
            u = prev_node[v]
            e = graph.g[u][prev_edge[v]]
            flow = min(flow, e.cap)
            v = u

        # push flow
        v = t
        while v != s:
            u = prev_node[v]
            e = graph.g[u][prev_edge[v]]
            e.cap -= flow
            graph.g[v][e.rev].cap += flow
            v = u

        total_flow += flow
        total_cost += flow * dist[t]

    return total_flow, total_cost