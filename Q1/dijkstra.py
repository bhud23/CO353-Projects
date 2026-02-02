import heapq
from math import inf

def dijkstra(graph, source):
    """
    Dijkstra's algorithm for a digraph represented as graph[u] -> {v: weight, ...}

    Returns:
    - dist: dict mapping node -> shortest distance from source
    - prev: dict mapping node -> previous node on the shortest path (for path reconstruction)
    """
    # Collect all nodes (keys + neighbors) so dist is well-defined for every node present.
    nodes = set(graph.keys())
    for u, nbrs in graph.items():
        nodes.update(nbrs.keys())

    dist = {node: inf for node in nodes}
    prev = {node: None for node in nodes}
    dist[source] = 0

    # Priority queue of (distance_so_far, node)
    pq = [(0, source)]

    while pq:
        d_u, u = heapq.heappop(pq)
        if d_u != dist.get(u, inf):
            continue

        # if u has no outgoing edges, graph.get(u, {}) gives empty dict.
        for v, w_uv in graph.get(u, {}).items():
            alt = d_u + w_uv
            if alt < dist.get(v, inf):
                dist[v] = alt
                prev[v] = u
                heapq.heappush(pq, (alt, v))

    return dist, prev



def shortest_path(prev, s, t):
    """
    Reconstruct shortest path from s to t using the prev map
    returns a list of nodes or [] if unreachable
    """
    path = []
    cur = t
    while cur is not None:
        path.append(cur)
        if cur == s:
            path.reverse()
            return path
        cur = prev.get(cur)
    return []