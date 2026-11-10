"""Dijkstra's shortest-path algorithm for a weighted undirected graph."""
import heapq

def dijkstra(graph, start):
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, node = heapq.heappop(queue)
        if current_distance != distances[node]:
            continue
        for neighbour, weight in graph[node].items():
            candidate = current_distance + weight
            if candidate < distances[neighbour]:
                distances[neighbour] = candidate
                previous[neighbour] = node
                heapq.heappush(queue, (candidate, neighbour))
    return distances, previous

def reconstruct_path(previous, start, end):
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()
    return path if path and path[0] == start else []

def shortest_path(graph, start, end):
    distances, previous = dijkstra(graph, start)
    return distances[end], reconstruct_path(previous, start, end)
