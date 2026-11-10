"""CSV loading helpers for the Mini-Courier Planner."""
import csv
from pathlib import Path

def load_parcels(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def load_graph(path):
    graph = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            a, b, distance = row["from"], row["to"], float(row["distance_km"])
            graph.setdefault(a, {})[b] = distance
            graph.setdefault(b, {})[a] = distance
    return graph
