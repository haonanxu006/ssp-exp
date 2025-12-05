import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from generators.mcf_generators import generate_layered_graph_heavytail
from algorithms.ff import FordFulkerson
from algorithms.ff_scaling import FordFulkersonScaling

def run(
    widths,
    layers,
    trials,
    small_low,
    small_high,
    big_low,
    big_high,
    big_ratio
):
    records = []

    for w in widths:
        for it in range(trials):
            G, s, t = generate_layered_graph_heavytail(
                n_layers=layers,
                width=w,
                small_low=small_low,
                small_high=small_high,
                big_low=big_low,
                big_high=big_high,
                big_ratio=big_ratio
            )

            # FF
            ff = FordFulkerson(G, s, t)
            start = time.perf_counter()
            _, total_ff, aug_ff = ff.run()
            t_ff = time.perf_counter() - start

            # FF-scaling
            sc = FordFulkersonScaling(G, s, t)
            start = time.perf_counter()
            _, total_sc, aug_sc = sc.run()
            t_sc = time.perf_counter() - start

            records.append({
                "width": w,
                "layers": layers,
                "algo": "FF",
                "runtime": t_ff,
                "augment": aug_ff,
                "flow": total_ff
            })
            records.append({
                "width": w,
                "layers": layers,
                "algo": "FF-scaling",
                "runtime": t_sc,
                "augment": aug_sc,
                "flow": total_sc
            })

            print(f"[width={w}] Trial {it+1}/{trials}: FF={t_ff:.4f}s, SC={t_sc:.4f}s")

    df = pd.DataFrame(records)
    df.to_csv("results/results_ff_sc_heavytail.csv", index=False)
    print("\nSaved to results_ff_sc_heavytail.csv\n")
    return df


def plot(df):
    plt.figure(figsize=(8, 6))
    sns.lineplot(data=df, x="width", y="runtime", hue="algo", marker="o")
    plt.title("FF vs FF-scaling Runtime (Heavy-Tail)")
    plt.ylabel("Runtime (seconds)")
    plt.savefig("plots/ff_vs_sc_heavytail_runtime.png")
    plt.show()

    plt.figure(figsize=(8, 6))
    sns.lineplot(data=df, x="width", y="augment", hue="algo", marker="o")
    plt.title("FF vs FF-scaling Augment Count (Heavy-Tail)")
    plt.ylabel("Augmentations")
    plt.savefig("plots/ff_vs_sc_heavytail_augment.png")
    plt.show()


if __name__ == "__main__":
    df = run(
        widths=[10, 20, 40, 80],
        layers=4,
        trials=5,
        small_low=1,
        small_high=20,
        big_low=500,
        big_high=2000,
        big_ratio=0.1
    )

    plot(df)
