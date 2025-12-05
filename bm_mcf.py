import time
import statistics
import random
from algorithms.ff_mcf import MultiCommodityFlowFF
from algorithms.lp_mcf import MultiCommodityFlowLP
from generators.mcf_generators import generate_random_commodities, generate_random_graph

def run_one_instance(num_nodes, num_commodities, edge_prob, cap_min, cap_max, demand_min, demand_max):
    # guarantee one valid graph and one valid commodities
    while True:
        G = generate_random_graph(
            num_nodes=num_nodes,
            edge_prob=edge_prob,
            cap_min=cap_min,
            cap_max=cap_max,
        )
        if G is None:
            continue
        
        commodities = generate_random_commodities(
            G,
            num_commodities=num_commodities,
            demand_min=demand_min,
            demand_max=demand_max,
        )
        if commodities is None:
            continue

        break

    # LP
    lp = MultiCommodityFlowLP(G, commodities)
    t0 = time.perf_counter()
    _, lp_tp = lp.solve()
    t1 = time.perf_counter()
    lp_time = t1 - t0
    lp_total = sum(lp_tp[p] for p in commodities)

    # FF
    h = MultiCommodityFlowFF(G, commodities)
    t2 = time.perf_counter()
    _, ff_tp = h.run()
    t3 = time.perf_counter()
    ff_time = t3 - t2
    ff_total = sum(ff_tp[p] for p in commodities)

    return lp_time, ff_time, lp_total, ff_total

def benchmark(num_nodes, num_commodities, edge_prob=0.3, cap_min=5, cap_max=20, demand_min=5, demand_max=20, trials=5):
    print(f"=== Benchmark: Nodes={num_nodes}, Commodities={num_commodities} ===")
    
    lp_times = []
    ff_times = []
    gaps = []
    zero_gap_count = 0

    for i in range(trials):
        lp_time, ff_time, lp_total, ff_total = run_one_instance(
            num_nodes, num_commodities, edge_prob, cap_min, cap_max, demand_min, demand_max
        )

        lp_times.append(lp_time)
        ff_times.append(ff_time)
        gaps.append(lp_total - ff_total)

        if (lp_total == ff_total):
            zero_gap_count += 1

        print(
            f"  trial {i+1}/{trials} — LP: {lp_time:.4f}s, "
            f"Modified FF: {ff_time:.4f}s, "
            f"LP={lp_total:.1f}, FF={ff_total:.1f}, "
            f"gap={lp_total-ff_total:.1f}"
        )
    
    print("\n=== Summary ===")
    print(f"Avg LP time         : {statistics.mean(lp_times):.4f} s")
    print(f"Avg FF time         : {statistics.mean(ff_times):.4f} s")
    print(f"Speedup (LP/FF)     : {statistics.mean(lp_times)/statistics.mean(ff_times):.1f} x")
    print(f"Avg gap             : {statistics.mean(gaps):.3f}")
    print(f"Min/Max gap         : {min(gaps):.3f} / {max(gaps):.3f}")
    print(f"Zero-gap rate       : {zero_gap_count/trials:.2f}")
    print("==========================================\n")

if __name__ == "__main__":
    random.seed(42)

    cfg = [
        (8, 3),
        (10, 4),
        (12, 5),
        (14, 10),
    ]

    for num_nodes, num_commodities in cfg:
        benchmark(
            num_nodes=num_nodes,
            num_commodities=num_commodities,
            edge_prob=0.05,
            cap_min=5, 
            cap_max=20, 
            demand_min=5, 
            demand_max=20,
            trials=5,
        )



    