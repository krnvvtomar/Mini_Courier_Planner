"""Nearest-neighbour approximation for a delivery tour."""
from .dijkstra import dijkstra, reconstruct_path

def nearest_neighbour_tour(graph, depot, destinations):
    """
    Greedy TSP approximation:
    repeatedly visit the nearest unvisited destination, then return to depot.
    Shortest-path distances are used between stops.
    """
    remaining = set(destinations)
    current = depot
    stop_order = [depot]
    total_distance = 0
    legs = []

    while remaining:
        distances, previous = dijkstra(graph, current)
        next_stop = min(remaining, key=lambda node: (distances[node], node))
        leg_distance = distances[next_stop]
        path = reconstruct_path(previous, current, next_stop)
        if leg_distance == float("inf"):
            raise ValueError(f"No route from {current} to {next_stop}")
        legs.append({"from": current, "to": next_stop, "distance_km": leg_distance, "path": path})
        total_distance += leg_distance
        stop_order.append(next_stop)
        remaining.remove(next_stop)
        current = next_stop

    distances, previous = dijkstra(graph, current)
    return_distance = distances[depot]
    return_path = reconstruct_path(previous, current, depot)
    if return_distance == float("inf"):
        raise ValueError(f"No return route from {current} to {depot}")
    legs.append({"from": current, "to": depot, "distance_km": return_distance, "path": return_path})
    total_distance += return_distance
    stop_order.append(depot)

    return {"stop_order": stop_order, "total_distance_km": total_distance, "legs": legs}
