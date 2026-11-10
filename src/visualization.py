"""Optional charts for route and runtime visualization."""
import matplotlib.pyplot as plt

def save_runtime_chart(results, output_path):
    labels = list(results.keys())
    values = [results[k] * 1000 for k in labels]  # milliseconds
    plt.figure(figsize=(8, 4.5))
    plt.bar(labels, values)
    plt.ylabel("Execution time (milliseconds)")
    plt.title("Mini-Courier Planner: module runtime")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()

def save_route_graph(graph, route, output_path):
    # Deterministic circular layout without requiring NetworkX.
    import math
    nodes = sorted(graph)
    positions = {}
    for i, node in enumerate(nodes):
        angle = 2 * math.pi * i / max(1, len(nodes))
        positions[node] = (math.cos(angle), math.sin(angle))
    plt.figure(figsize=(7, 6))
    for a, neighbours in graph.items():
        for b, weight in neighbours.items():
            if a < b:
                x1, y1 = positions[a]; x2, y2 = positions[b]
                plt.plot([x1, x2], [y1, y2], linewidth=1, alpha=0.45)
                plt.text((x1+x2)/2, (y1+y2)/2, str(weight), fontsize=7)
    for node, (x, y) in positions.items():
        plt.scatter([x], [y], s=500)
        plt.text(x, y, node, ha="center", va="center", fontsize=8, color="white")
    plt.title("Delivery network (edge labels are kilometres)")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()
