import pulp

class MultiCommodityFlowLP:
    """
    Input: 
    - graph: NetworkX.DiGraph() -> networkx directed graph
    - commodities: Dict[str, (src, dst, demand)] -> commodity p to (source, sink, and demand)

    Output:
    - flow: Dict[str, Dict[(str, str), float]] -> used capacity on each edge for each commodity
    - throughput: Dict[str, float] -> sent/satisfied demand for each commodity

    Constraints:
    1. used capacity (flow) by commodity p on edge (u, v) >= 0
    2. used capacity (flow) by commodity p on edge (u, v) <= edge capacity
    3. total flow of commdity p <= its demand (0 <= throuhput(p) <= demand)
    4. inflow(p) == outflow(p) of p for each node (except source and sink)
        - source: outflow(p) - inflow(p) = throughput(p)
        - sink: inflow(p) - outflow(p) = throughput(p)

    Objective:
    - maximize throughput of commodity p
    """
    def __init__(self, G, commodities):
        self.G = G.copy()
        self.commodities = commodities

    def solve(self):
        nodes = list(self.G.nodes())
        edges = list(self.G.edges())

        prob = pulp.LpProblem("MultiCommodityFlow", pulp.LpMaximize)

        # constraint 1
        flow = {
            p: {
                (u, v): pulp.LpVariable(f"f_{p}_{u}_{v}", lowBound=0)
                for (u, v) in edges
            }
            for p in self.commodities
        }

        # constraint 2
        for (u, v) in edges:
            cap = self.G[u][v]["capacity"]
            prob += pulp.lpSum(flow[p][(u, v)] for p in self.commodities) <= cap

        # constraint 3
        throughput = {
            p: pulp.LpVariable(f"theta_{p}", lowBound=0)
            for p in self.commodities
        }
        for p, (_, _, demand) in self.commodities.items():
            prob += throughput[p] <= demand

        # constraint 4
        for p, (s, t, demand) in self.commodities.items():
            for node in nodes:
                outflow = pulp.lpSum(
                    flow[p][(node, j)]
                    for (_node, j) in edges if _node == node
                )
                inflow = pulp.lpSum(
                    flow[p][(i, node)]
                    for (i, _node) in edges if _node == node
                )

                if node == s:
                    prob += outflow - inflow == throughput[p]
                elif node == t:
                    prob += inflow - outflow == throughput[p]
                else:
                    prob += outflow - inflow == 0

        # objective
        prob += pulp.lpSum(throughput[p] for p in self.commodities)

        prob.solve(pulp.PULP_CBC_CMD(msg=False))

        flow_result = {
            p: {(u, v): flow[p][(u, v)].value() for (u, v) in edges}
            for p in self.commodities
        }

        throughput_result = {p: throughput[p].value() for p in self.commodities}

        return flow_result, throughput_result