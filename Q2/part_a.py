import sys
from collections import defaultdict 
import heapq


class SegTree:

    def __init__(self, size, input_arcs):
        self.size = size

        # List of adjacent neighbours for each node
        self.adj_list = defaultdict(list)
        self.nodes = set()

        # Fill adj_list with the trivial 0 weights
        self.build_zero_weight_edges(1, size)

        self.build_edges(input_arcs)

    # build the adjacency list 
    def build_edges(self, input_arcs):
        for arc in input_arcs:
            node_out, interval, weight = arc
            self.adj_list[(node_out, node_out)].append((interval, weight))

    def build_zero_weight_edges(self, left, right):
        self.nodes.add((left, right))
        if left == right:
            return
        else:
            mid = (left + right) // 2

            self.adj_list[(left, right)].append(((left, mid), 0))
            self.adj_list[(left, right)].append(((mid + 1, right), 0))

            self.build_zero_weight_edges(left, mid)
            self.build_zero_weight_edges(mid + 1, right)

    def modified_dijkstra(self, root):
        # distance dictionary for each node
        dist = defaultdict(lambda: float('inf'))
        dist[(root, root)] = 0
        # print(dist)

        # visited dictionary for which nodes we finalized
        # visited = {k: False for k in self.nodes}
        # print(visited)

        # priority queue, each tuple is (distance, interval_node)
        pq = [(0, (root, root))]
        while pq:
            # current distance and interval of the closest node
            cur_dist, cur_int = heapq.heappop(pq)
            
            # stale entry (don't need visited dict anymore)
            if cur_dist != dist[cur_int]: 
                continue

            # finalize it if we haven't
            # if not visited[cur_int]: 
            #     visited[cur_int] = True
            #     dist[cur_int] = min(cur_dist, dist[cur_int])

                # int_n is interval_neighbour 
            for int_n, weight in self.adj_list[cur_int]:
                new_dist = cur_dist + weight
                if new_dist < dist[int_n]:
                    dist[int_n] = new_dist
                    heapq.heappush(pq, (new_dist, int_n))

        
        # print solution
        ans = []
        for i in range(1, self.size + 1):
            v = dist[(i,i)]
            ans.append(v if v != float('inf') else -1)
        
        print(*ans)

if __name__ == "__main__":
    n, q, s = 0, 0, 0

    if sys.stdin is not None:
        input_arcs = []

        # read lines to generate graph G
        for i, line in enumerate(sys.stdin):
            # first line are paramters n, q, s (number of nodes, number of lines, starting root node)
            if i == 0:
                params = line.split()
                n = int(params[0])
                q = int(params[1])
                s = int(params[2])
                continue
            elif q < i:
                break

            arcs = line.split()
            v = int(arcs[0])
            l = int(arcs[1])
            r = int(arcs[2])
            c = int(arcs[3])
            input_arcs.append((v, (l, r), c))

    # Build the segment tree
    seg_tree = SegTree(n, input_arcs)
    seg_tree.modified_dijkstra(s)
