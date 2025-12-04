from algorithms.ssp import ssp
from algorithms.bellman_ford import bellman_ford
from algorithms.residual_graph import ResidualGraph
import networkx as nx

print("Running SSP Bellman Ford...")

n = 4
s, t = 0, 3
g = ResidualGraph(n)

g.add_edge(0, 1, 3, 1)
g.add_edge(1, 3, 3, 1)

g.add_edge(0, 2, 2, 2)
g.add_edge(2, 3, 2, 2)

flow, cost = ssp(g, s, t, bellman_ford)
print(f"[SSP-BF] flow = {flow}, cost = {cost}")

G = nx.DiGraph()
G.add_edge(0, 1, capacity=3, weight=1)
G.add_edge(1, 3, capacity=3, weight=1)
G.add_edge(0, 2, capacity=2, weight=2)
G.add_edge(2, 3, capacity=2, weight=2)

flow_dict = nx.max_flow_min_cost(G, s, t)
cost_nx = nx.cost_of_flow(G, flow_dict)
flow_nx = sum(flow_dict[s].values())

print(f"[NetworkX] flow = {flow_nx}, cost = {cost_nx}")

assert flow == flow_nx
assert cost == cost_nx
print("Pass!")