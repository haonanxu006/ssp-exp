import networkx as nx
import math

class FordFulkersonScaling:
    def __init__(self, G: nx.DiGraph, source, sink):
        """
        """
        self.G = G.copy()
        self.s = source
        self.t = sink

        self.flow = {(u, v): 0 for (u, v) in self.G.edges()}
        self.augment_count = 0

    def build_residual_graph(self, delta):
        R = nx.DiGraph()

        # forward edges
        for (u, v) in self.G.edges():
            rc = self.G[u][v]["capacity"] - self.flow[(u, v)]
            # only consider cap >= delta
            if rc >= delta:
                R.add_edge(u, v, capacity=rc)

        # reverse edges
        for (u, v) in self.G.edges():
            f = self.flow[(u, v)]
            # only consider cap >= delta
            if f >= delta:
                R.add_edge(v, u, capacity=f)

        return R

    def find_path(self, delta):
        R = self.build_residual_graph(delta)

        if self.s not in R.nodes or self.t not in R.nodes:
            return None

        try:
            return nx.shortest_path(R, self.s, self.t)
        except nx.NetworkXNoPath:
            return None

    def augment(self, path):
        bottleneck = math.inf

        # find bottleneck
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]

            if (u, v) in self.G.edges():
                # forward 
                cap = self.G[u][v]["capacity"] - self.flow[(u, v)]
            else:
                # reverse
                cap = self.flow[(v, u)]

            bottleneck = min(bottleneck, cap)

        # apply augmentation
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]

            if (u, v) in self.G.edges():
                # forward
                self.flow[(u, v)] += bottleneck
            else:
                # backward
                self.flow[(v, u)] -= bottleneck

        self.augment_count += 1
        return bottleneck

    def run(self):
        # find max capacity
        max_cap = max(self.G[u][v]["capacity"] for (u, v) in self.G.edges())

        # highest power of 2 ≤ max_cap
        delta = 1
        while delta <= max_cap:
            delta <<= 1
        delta >>= 1

        # scaling loop
        while delta >= 1:
            while True:
                path = self.find_path(delta)
                if path is None:
                    break
                self.augment(path)
            delta //= 2

        total_flow = sum(
            self.flow[(self.s, v)]
            for (u, v) in self.flow
            if u == self.s
        )

        return self.flow, total_flow, self.augment_count
