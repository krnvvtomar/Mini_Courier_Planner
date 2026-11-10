# Mini-Courier Planner — Capstone Project Report

## 1. Problem Statement
The project develops a prototype courier-planning system. Given parcels, a carrying-capacity limit, and a weighted delivery network, the application prioritizes parcels, chooses a valuable feasible parcel set, calculates shortest paths, and estimates an overall delivery tour.

## 2. Objectives
1. Prioritize parcels by delivery deadline and priority.
2. Select parcels without exceeding vehicle capacity.
3. Find shortest paths in a weighted graph.
4. Generate an approximate tour through selected delivery points.
5. measure algorithm execution time and discuss complexity.

## 3. System Design
The application is divided into modules: `sorting.py`, `knapsack.py`, `dijkstra.py`, `tsp.py`, `data_loader.py`, `visualization.py`, `benchmark.py`, and `main.py`. Parcel and road data are stored separately as CSV files.

## 4. Methodology
### 4.1 Parcel Sorting
Parcels are sorted by ascending deadline. For equal deadlines, HIGH priority precedes MEDIUM and LOW. Parcel ID is used as a deterministic final tie-breaker. Python's built-in Timsort has O(n log n) worst-case time complexity.

### 4.2 Package Selection: 0/1 Knapsack
Each parcel has an integer weight and a value score. Dynamic programming computes the maximum value possible for each prefix of parcels and each capacity from zero to W. Time and space complexity are O(nW). Each parcel is selected at most once.

### 4.3 Shortest Path: Dijkstra
The road network is represented as an adjacency dictionary. Each road is an undirected edge with a non-negative distance. Dijkstra's algorithm uses a min-priority queue and has O((V+E) log V) complexity with a binary heap.

### 4.4 Overall Tour: Nearest-Neighbour TSP
Starting at DEPOT, the algorithm repeatedly visits the nearest unvisited delivery point using shortest-path distances, then returns to the depot. This is a greedy approximation and does not guarantee the optimal TSP tour.

## 5. Sample Data and Test Setup
The included sample has eight parcels and eight delivery points (A-H), with a 20 kg default van capacity. The route dataset is a weighted undirected graph with distances in kilometres. The benchmark generates synthetic parcel lists and connected graphs with input sizes 10, 30, 60, and 100.

## 6. Results
Run `python -m src.main` to generate the final parcel selection, Dijkstra path, approximate delivery tour, and module timings. Run `python -m src.benchmark` to produce `outputs/benchmark_results.csv`. Runtime values vary by hardware and system load; use the measurements produced on the submission computer in the final discussion.

## 7. Complexity Summary
| Component | Algorithm | Time complexity |
|---|---|---|
| Sorting | Timsort | O(n log n) |
| Packing | 0/1 Knapsack DP | O(nW) |
| Shortest path | Dijkstra + binary heap | O((V+E) log V) |
| Tour | Repeated Dijkstra + nearest neighbour | O(k(V+E)log V + k²) approximately, for k delivery points |

## 8. Conclusion
The prototype demonstrates how sorting, dynamic programming, graph algorithms, and an approximation technique can be integrated into one application. It provides an understandable baseline for courier planning. The greedy tour can be improved in future work using 2-opt, genetic algorithms, or more advanced vehicle-routing methods.

## 9. Future Scope
- Support one-way roads, traffic and time-dependent travel costs.
- Add multiple vehicles and multiple depots.
- Include delivery time windows and service durations.
- Compare nearest-neighbour with 2-opt and exact solutions on small graphs.
- Use live map data and a database instead of sample CSV files.
