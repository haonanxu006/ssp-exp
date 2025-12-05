# Experiments of Ford Fulkerson Variants

## Multi-Commodity Flow Benchmark #1

This benchmark compares LP-based MCF and modified FF-based MCF

### Required packages

networkx, pulp

### Run the benchmark

`python bm_mcf.py`

### Configurable parameters

Configuration list: `[(num_nodes, num_commodities)]`

| Parameter                  | Meaning                                   |
| -------------------------- | ----------------------------------------- |
| `num_nodes`                | Number of graph nodes                     |
| `num_commodities`          | Number of commodities                     |
| `edge_prob`                | Probability of edge creation              |
| `cap_min`, `cap_max`       | Capacity range for edges                  |
| `demand_min`, `demand_max` | Demand range for commodities              |
| `trials`                   | Number of random trials per configuration |

### Metrics

| Metric              | Meaning                                |
| ------------------- | -------------------------------------- |
| **Avg LP time**     | Average LP solver runtime              |
| **Avg FF time**     | Average FF-based runtime               |
| **Speedup (LP/FF)** | Runtime ratio                          |
| **Avg gap**         | Average optimality gap                 |
| **Min / Max gap**   | Observed gap range                     |
| **Zero-gap rate**   | Fraction of trials where FF matched LP |
