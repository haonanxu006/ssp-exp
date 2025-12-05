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

def generate_layered_graph(n_layers, width, cap_low=1, cap_high=20):
    """
    Generate a layered directed graph

    Input:
    - number of layers (>= 1)
    - number of nodes per layer
    - capacity range

    Output:
    - NetworkX.DiGraph
    - source 
    - sink 
    """
    G = nx.DiGraph()

    layers = [
        [f"L{L}_{i}" for i in range(width)]
        for L in range(n_layers)
    ]

    s = "s"
    t = "t"

    # add source and sink
    G.add_node(s)
    G.add_node(t)
    for layer in layers:
        for node in layer:
            G.add_node(node)

    # connect source to first layer
    for node in layers[0]:
        cap = random.randint(cap_low, cap_high)
        G.add_edge(s, node, capacity=cap)

    # connect intermediate layers
    for l in range(n_layers - 1):
        for u in layers[l]:
            for v in layers[l+1]:
                cap = random.randint(cap_low, cap_high)
                G.add_edge(u, v, capacity=cap)

    # connect last layer to sink
    for node in layers[-1]:
        cap = random.randint(cap_low, cap_high)
        G.add_edge(node, t, capacity=cap)

    return G, s, t

def generate_layered_graph_heavytail(
    n_layers, width,
    small_low=1, small_high=20,
    big_low=500, big_high=2000,
    big_ratio=0.1
):
    """
    Generate a heavy-tail layered graph

    Input:
    - number of layers (>= 1)
    - number of nodes per layer
    - small capacity range
    - big capacity range
    - big ratio

    Output:
    - NetworkX.DiGraph
    - source 
    - sink 
    """

    G = nx.DiGraph()

    def random_cap():
        if random.random() < big_ratio:
            return random.randint(big_low, big_high)
        return random.randint(small_low, small_high)

    s = "s"
    t = "t"
    G.add_node(s)
    G.add_node(t)

    layers = []
    for L in range(n_layers):
        layer_nodes = [f"L{L}_{i}" for i in range(width)]
        layers.append(layer_nodes)
        G.add_nodes_from(layer_nodes)

    # connect source to first layer
    for node in layers[0]:
        G.add_edge(s, node, capacity=random_cap())

    # connect intermediate layers
    for l in range(n_layers - 1):
        for u in layers[l]:
            for v in layers[l + 1]:
                G.add_edge(u, v, capacity=random_cap())

    # connect last layer to sink
    for node in layers[-1]:
        G.add_edge(node, t, capacity=random_cap())

    return G, s, t
