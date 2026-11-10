# Mini-Courier Planner

A Python capstone prototype that prioritizes parcels, chooses a high-value set under a van capacity, calculates shortest paths, and creates an approximate delivery tour.

## Features
- Parcel sorting: earliest deadline first; ties are resolved by priority and parcel ID.
- 0/1 Knapsack dynamic programming: maximizes total parcel value without exceeding van capacity.
- Dijkstra's algorithm: computes shortest paths in a weighted, undirected delivery graph.
- Nearest-neighbour TSP approximation: builds a delivery tour and returns to the depot.
- Runtime measurements and charts.

## Requirements
- Python 3.9+
- matplotlib (only required to create charts)

## Run
From the project root:

```bash
python -m src.main
```

Run scalability benchmarks:

```bash
python -m src.benchmark
```

The program reads `datasets/parcels.csv` and `datasets/routes.csv`. It writes:
- `outputs/sample_output.json`
- `outputs/console_output.txt`
- `images/runtime_chart.png`
- `images/delivery_graph.png`

## Data format
`parcels.csv` contains parcel ID, weight, value, priority, deadline, and destination.
`routes.csv` contains an undirected weighted edge list. Distances are in kilometres.

## Project structure
```text
datasets/  sample parcel and route data
src/       modular Python implementation
images/    generated route and runtime charts
outputs/   sample program output and benchmark results
docs/      project report
```

## Algorithm notes and complexity
- Sorting: Python's Timsort, O(n log n).
- 0/1 Knapsack: O(nW) time and O(nW) space, where n is parcel count and W is integer capacity.
- Dijkstra with a binary heap: O((V + E) log V).
- Nearest-neighbour TSP: greedy approximation; this implementation runs Dijkstra for each next stop. It is not guaranteed to find the globally shortest tour.

## Assumptions and limitations
- All parcels in the sample are available at one depot.
- The graph is undirected and edge weights are non-negative kilometres.
- Parcel `value` is a simple priority/benefit score used by knapsack; it is not a currency amount.
- The van capacity is set to 20 kg by default.
- This is an educational prototype. The nearest-neighbour method is an approximation, not an exact TSP solver.
- The sample dataset and measured runtimes are illustrative; rerun on your own computer for your actual timing values.

## Submission
Review the report in `docs/Capstone_Project_Report.pdf`, run the application, and include your own name, roll number, course section, and screenshots if your instructor requires them.
