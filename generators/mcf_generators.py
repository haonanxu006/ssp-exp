import random
import networkx as nx

def generate_random_commodities(G, num_commodities=3, demand_min=5, demand_max=20):
    """
    Input:
    - NetworkX.DiGraph()
    - number of commodities
    - range of demand

    Output:
    - commodities: Dict[str, (src, dst, demand)]
    """
    nodes = list(G.nodes())
    commodities = {}
    attempts = 0
    i = 1

    while len(commodities) < num_commodities and attempts < num_commodities * 20:
        attempts += 1
        s, t = random.sample(nodes, 2)
        # it's possible that G has no path from s to t -> retry
        if not nx.has_path(G, s, t):
            continue
        demand = random.randint(demand_min, demand_max)
        commodities[f"K{i}"] = (s, t, demand)
        i += 1

    
    if len(commodities) == 0:
        return None

    return commodities

def generate_random_graph(num_nodes=10, edge_prob=0.3, cap_min=5, cap_max=20):
    """
    Input: 
    - number of nodes
    - edge probability
    - capacity range

    Output:
    - NetworkX.DiGraph()
    """
    G = nx.DiGraph()
    nodes = [f"v{i}" for i in range(num_nodes)]

    for u in nodes:
        for v in nodes:
            if u == v:
                continue
            if random.random() < edge_prob:
                cap = random.randint(cap_min, cap_max)
                G.add_edge(u, v, capacity=cap)

    # happens when edge_prob is too low
    if G.number_of_edges() == 0:
        return None

    # ensure G is fully connected
    UG = G.to_undirected()
    if not nx.is_connected(UG):
        return None

    return G