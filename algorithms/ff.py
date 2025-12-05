import networkx as nx

class FordFulkerson:
    def __init__(self, G, source, sink):
        """
        """
        self.G = G.copy()
        self.s = source
        self.t = sink

        self.flow = {(u, v): 0 for (u, v) in self.G.edges()}
        self.augment_count = 0

    def build_residual_graph(self):
        R = nx.DiGraph()

        # forward edges
        for (u, v) in self.G.edges():
            rc = self.G[u][v]["capacity"] - self.flow[(u, v)]
            if rc > 0:
                R.add_edge(u, v, capacity=rc)

        # reverse edges 
        for (u, v) in self.G.edges():
            f = self.flow[(u, v)]
            if f > 0:
                R.add_edge(v, u, capacity=f)

        return R

    def find_path(self):
        R = self.build_residual_graph()

        if self.s not in R.nodes or self.t not in R.nodes:
            return None

        try:
            path = nx.shortest_path(R, self.s, self.t)
            return path
        except nx.NetworkXNoPath:
            return None

    def augment(self, path):
        # find bottleneck
        capacities = []
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]

            if (u, v) in self.G.edges():
                # forward edge
                capacities.append(self.G[u][v]["capacity"] - self.flow[(u, v)])
            else:
                # reverse edge
                capacities.append(self.flow[(v, u)])

        bottleneck = min(capacities)

        # apply augmentation
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]

            if (u, v) in self.G.edges(): 
                # forward
                self.flow[(u, v)] += bottleneck
            else:  
                # reverse
                self.flow[(v, u)] -= bottleneck

        self.augment_count += 1
        return bottleneck

    def run(self):
        while True:
            path = self.find_path()
            if not path:
                break

            sent = self.augment(path)
            if sent <= 0:
                break

        # add up flow of each outflow edge from source
        total_flow = sum(
            self.flow[(self.s, v)]
            for (u, v) in self.flow
            if u == self.s
        )

        return self.flow, total_flow, self.augment_count
