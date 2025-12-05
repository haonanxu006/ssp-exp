import networkx as nx

class MultiCommodityFlowFF:
    """
    Input:
    - graph: NetworkX.DiGraph() -> networkx directed graph
    - commodities: Dict[str, (src, dst, demand)] -> commodity p to (source, sink, and demand)

    Output:
    - flow: Dict[str, Dict[(str, str), float]] -> used capacity on each edge for each commodity
    - throughput: Dict[str, float] -> sent/satisfied demand for each commodity
    """
    def __init__(self, G, commodities):
        self.G = G.copy()
        self.commodities = commodities

        # flow[p][(u,v)]: amount of flow of commodity p on edge (u, v), same as reverse capacity 
        self.flow = {p: {(u, v): 0.0 for u, v in G.edges()} for p in commodities}

        # throughput[p]: pushed/satisfied need for each commodity
        self.throughput = {p: 0 for p in commodities}

    def edge_used_cap(self, u, v):
        # compute the total capacities of edge (u, v) used by all commodities
        return sum(self.flow[p][(u, v)] for p in self.flow)

    def build_residual_graph(self, p):
        # builds a residual graph
        R = nx.DiGraph()
        R.add_nodes_from(self.G.nodes())

        # forward edges
        for u, v in self.G.edges():
            forward_cap = self.G[u][v]["capacity"] - self.edge_used_cap(u, v)
            if forward_cap > 0:
                R.add_edge(u, v, capacity=forward_cap, weight=1)

        # backward edges (per commodity)
        for u, v in self.G.edges():
            backward_cap = self.flow[p][(u, v)]
            if backward_cap > 0:
                # this undoes flow for commodity p only
                R.add_edge(v, u, capacity=backward_cap, weight=1)

        return R

    def find_path(self, p):
        # find a path from commodity p's source to sink
        s, t, _ = self.commodities[p]
        R = self.build_residual_graph(p)

        try:
            return nx.shortest_path(R, s, t, weight="weight") 
        except nx.NetworkXNoPath:
            return None

    def augment(self, p, path):
        _, _, demand = self.commodities[p]

        # compute bottleneck capacity of input path
        caps = []
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]

            if (u, v) in self.G.edges():
                # forward edge
                caps.append(self.G[u][v]["capacity"] - self.edge_used_cap(u, v))
            else:
                # backward edge
                caps.append(self.flow[p][(v, u)])

        # should not exceed remaining demand of p
        bottleneck = min(min(caps), demand - self.throughput[p])

        # apply augmentation
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]

            if (u, v) in self.G.edges(): 
                # forward: add to flow
                self.flow[p][(u, v)] += bottleneck
            else:  
                # backward: undo flow
                self.flow[p][(v, u)] -= bottleneck

        self.throughput[p] += bottleneck
        return bottleneck

    def run(self):
        order = list(self.commodities.keys())

        while True:
            moved = False

            # find augmenting path for each commodity 
            for p in order:
                # skip if p is satisfied
                _, _, demand = self.commodities[p]
                if self.throughput[p] == demand:
                    continue
                
                # find a path for commodity p
                path = self.find_path(p)
                if not path:
                    continue

                # augment
                sent = self.augment(p, path)
                if sent > 0:
                    moved = True

            if not moved:
                break

        return self.flow, self.throughput
