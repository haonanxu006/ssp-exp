class Edge:
    def __init__(self, to, cap, cost, rev):
        self.to = to
        self.cap = cap
        self.cost = cost
        self.rev = rev

class ResidualGraph:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, u, v, cap, cost):
        """
        edge u -> v with capacity cap, cost cost, and reverse edge
        """
        forward = Edge(v, cap, cost, len(self.g[v]))
        reverse = Edge(u, 0, -cost, len(self.g[u]))
        self.g[u].append(forward)
        self.g[v].append(reverse)