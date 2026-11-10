"""Integrated Mini-Courier Planner application."""
from pathlib import Path
import json
import time
from .data_loader import load_parcels, load_graph
from .sorting import sort_parcels
from .knapsack import select_parcels
from .dijkstra import shortest_path
from .tsp import nearest_neighbour_tour
from .visualization import save_runtime_chart, save_route_graph

ROOT = Path(__file__).resolve().parents[1]

def run_planner(capacity=20, make_charts=True):
    parcels = load_parcels(ROOT / "datasets" / "parcels.csv")
    graph = load_graph(ROOT / "datasets" / "routes.csv")
    timings = {}

    t0 = time.perf_counter()
    prioritized = sort_parcels(parcels)
    timings["Sorting"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    selected, packing = select_parcels(prioritized, capacity)
    timings["Knapsack DP"] = time.perf_counter() - t0

    depot = "DEPOT"
    # Dijkstra example: show shortest route to first selected delivery point.
    if selected:
        t0 = time.perf_counter()
        first_destination = selected[0]["destination"]
        distance, path = shortest_path(graph, depot, first_destination)
        timings["Dijkstra"] = time.perf_counter() - t0
    else:
        first_destination, distance, path = None, 0, []

    destinations = sorted({p["destination"] for p in selected})
    t0 = time.perf_counter()
    tour = nearest_neighbour_tour(graph, depot, destinations) if destinations else {
        "stop_order": [depot], "total_distance_km": 0, "legs": []
    }
    timings["Nearest-neighbour TSP"] = time.perf_counter() - t0

    result = {
        "prioritized_parcels": prioritized,
        "selected_parcels": selected,
        "packing": {k: v for k, v in packing.items() if k != "dp_table"},
        "dijkstra_example": {"destination": first_destination, "distance_km": distance, "path": path},
        "delivery_tour": tour,
        "runtime_seconds": timings,
    }

    output_dir = ROOT / "outputs"
    output_dir.mkdir(exist_ok=True)
    (output_dir / "sample_output.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    with open(output_dir / "console_output.txt", "w", encoding="utf-8") as f:
        f.write(format_result(result))
    if make_charts:
        save_runtime_chart(timings, ROOT / "images" / "runtime_chart.png")
        save_route_graph(graph, tour, ROOT / "images" / "delivery_graph.png")
    return result

def format_result(result):
    lines = [
        "=" * 60,
        "              MINI-COURIER PLANNER",
        "=" * 60,
        "\n1. PARCEL PRIORITIZATION (earliest deadline first)",
    ]
    for p in result["prioritized_parcels"]:
        lines.append(f'{p["parcel_id"]}: {p["priority"]}, deadline {p["deadline"]}, '
                     f'{p["weight_kg"]} kg, destination {p["destination"]}')
    lines.append("\n2. OPTIMAL PACKING (0/1 Knapsack DP)")
    for p in result["selected_parcels"]:
        lines.append(f'{p["parcel_id"]} -> {p["destination"]} ({p["weight_kg"]} kg)')
    pack = result["packing"]
    lines.append(f'Total weight: {pack["used_capacity_kg"]}/{pack["capacity_kg"]} kg')
    lines.append(f'Total parcel value: {pack["total_value"]}')
    d = result["dijkstra_example"]
    lines.append("\n3. DIJKSTRA SHORTEST-PATH EXAMPLE")
    lines.append(f'To {d["destination"]}: {d["distance_km"]} km | Path: {" -> ".join(d["path"])}')
    tour = result["delivery_tour"]
    lines.append("\n4. NEAREST-NEIGHBOUR DELIVERY TOUR")
    lines.append(" -> ".join(tour["stop_order"]))
    lines.append(f'Total tour distance (including return to depot): {tour["total_distance_km"]} km')
    lines.append("\n5. MODULE RUNTIMES")
    for name, seconds in result["runtime_seconds"].items():
        lines.append(f"{name}: {seconds*1000:.4f} ms")
    lines.append("\nNote: Runtime values depend on the computer and current system load.")
    return "\n".join(lines)

if __name__ == "__main__":
    result = run_planner()
    print(format_result(result))
