"""Scalability benchmark for sorting, knapsack, and graph routing."""
from pathlib import Path
import random, time, csv
from .sorting import sort_parcels
from .knapsack import select_parcels
from .dijkstra import dijkstra

ROOT = Path(__file__).resolve().parents[1]

def benchmark():
    random.seed(7)
    rows = []
    for n in [10, 30, 60, 100]:
        parcels = []
        for i in range(n):
            parcels.append({
                "parcel_id": f"P{i}", "weight_kg": random.randint(1, 10),
                "value": random.randint(10, 100), "priority": random.choice(["HIGH","MEDIUM","LOW"]),
                "deadline": f"{random.randint(8,17):02d}:{random.choice([0,15,30,45]):02d}"
            })
        t = time.perf_counter(); sort_parcels(parcels); sort_s = time.perf_counter()-t
        t = time.perf_counter(); select_parcels(parcels, 40); knap_s = time.perf_counter()-t

        # Sparse connected graph: chain plus random forward edges.
        graph = {f"N{i}": {} for i in range(n)}
        for i in range(n-1):
            w = random.randint(1, 20)
            graph[f"N{i}"][f"N{i+1}"] = w
            graph[f"N{i+1}"][f"N{i}"] = w
        for _ in range(n):
            a, b = sorted(random.sample(range(n), 2))
            if b-a > 1:
                w = random.randint(1, 20)
                graph[f"N{a}"][f"N{b}"] = w
                graph[f"N{b}"][f"N{a}"] = w
        t = time.perf_counter(); dijkstra(graph, "N0"); dij_s = time.perf_counter()-t
        rows.append({"input_size": n, "sorting_seconds": sort_s,
                     "knapsack_seconds": knap_s, "dijkstra_seconds": dij_s})

    out = ROOT / "outputs" / "benchmark_results.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)
    return rows

if __name__ == "__main__":
    results = benchmark()
    for row in results: print(row)
