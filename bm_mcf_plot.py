import time
import statistics
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from algorithms.ff_mcf import MultiCommodityFlowFF
from algorithms.lp_mcf import MultiCommodityFlowLP
from generators.mcf_generators import generate_random_commodities, generate_random_graph


def run_one_instance(num_nodes, num_commodities,
                     edge_prob, cap_min, cap_max,
                     demand_min, demand_max):
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


def benchmark_and_collect(num_nodes, num_commodities,
                          edge_prob, cap_min, cap_max,
                          demand_min, demand_max,
                          trials=5):
    records = []

    for i in range(trials):
        lp_time, ff_time, lp_total, ff_total = run_one_instance(
            num_nodes, num_commodities,
            edge_prob, cap_min, cap_max,
            demand_min, demand_max,
        )

        records.append({
            "nodes": num_nodes,
            "algo": "LP",
            "runtime": lp_time,
            "gap": 0,
            "ff_flow": ff_total,
            "lp_flow": lp_total,
        })

        records.append({
            "nodes": num_nodes,
            "algo": "FF",
            "runtime": ff_time,
            "gap": lp_total - ff_total,
            "ff_flow": ff_total,
            "lp_flow": lp_total,
        })

        print(
            f"[n={num_nodes}] trial {i+1}/{trials} — "
            f"LP={lp_time:.4f}s, FF={ff_time:.4f}s, "
            f"gap={lp_total-ff_total:.1f}"
        )

    return records


def plot_results(df):
    plt.figure(figsize=(8, 6))
    ax = sns.lineplot(
        data=df,
        x="nodes",
        y="runtime",
        hue="algo",
        marker="o",
        errorbar="sd"
    )
    handles, labels = ax.get_legend_handles_labels()
    label_map = {
        "LP": "LP",
        "FF": "FF"
    }
    new_labels = [label_map.get(l, l) for l in labels]
    ax.legend(handles, new_labels)

    plt.title("Runtime vs Graph Size")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Runtime (seconds)")
    plt.savefig("plots/mcf.png", dpi=300, bbox_inches="tight")
    plt.show()

def make_gap_table(df):
    summary = (
        df[df["algo"] == "FF"]
        .groupby("nodes")
        .agg(
            avg_lp_flow=("lp_flow", "mean"),
            avg_ff_flow=("ff_flow", "mean"),
            avg_gap=("gap", "mean"),
            zero_gap_rate=("gap", lambda x: (x == 0).mean()),
        )
        .reset_index()
    )
    return summary

if __name__ == "__main__":
    random.seed(42)

    nodes_list = [20, 30, 40, 50, 60]
    cfg = [(n, int(0.3 * n)) for n in nodes_list]

    all_records = []

    for num_nodes, num_commodities in cfg:
        print(f"\n=== Nodes={num_nodes}, Commodities={num_commodities} ===")
        records = benchmark_and_collect(
            num_nodes=num_nodes,
            num_commodities=num_commodities,
            edge_prob=0.2,
            cap_min=1,
            cap_max=10,
            demand_min=5,
            demand_max=20,
            trials=30,
        )
        all_records.extend(records)

    df = pd.DataFrame(all_records)
    df.to_csv("results/results_mcf.csv", index=False)

    summary = make_gap_table(df)
    summary.to_csv("results/mcf_gap_summary_table.csv", index=False)
    print(summary.round(3))

    plot_results(df)
