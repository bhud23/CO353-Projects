import sys
import heapq
# test using diff <(cat tests/X | python Q1.py) <(cat tests/X)

def find_cheapest_walks (G, s, t, q):
    """
    Produces q cheapest walks on weighted digraph G from nodes s to t
    """
    
    # setup
    answers = []
    dist_list = {}
    mh = [] # min heap - i use the heapq module which implements a min heap on top of a list
    heapq.heappush(mh, [0, s])

    nodes = set(G.keys())
    for v, nbrs in G.items():
        nodes.update(nbrs.keys())
    nodes.add(s)
    nodes.add(t)

    dist_list = {node: [] for node in nodes}

    while mh and len(answers) < q:
        d, v = heapq.heappop(mh) # returns a list first element is distance next is node label

        # if we already have q walks from cur[1] then skip the rest, for efficieny
        if len(dist_list[v]) == q:
            
            continue
    
        dist_list[v].append(d)

        if v == t:
            answers.append(str(d))

            if len(answers) == q:
                break

        for u, w in G.get(v, {}).items():# iterate thru edges connected to current node v
            if len(dist_list[u]) < q: # we can push more edges
                heapq.heappush(mh, (d + int(w), u))

    return answers


if __name__ == "__main__":
    n, m, q = -1, -1, -1
    s, t = -1, -1

    # we will represent the graph as a dict of nodes coupled with another dict of nodes and weights representing in-node and weight of that edge
    G = {}

    if sys.stdin is not None:
        # read lines to generate graph G
        for i, line in enumerate(sys.stdin):

            # first line are paramters n, m, q
            if i == 0:
                params = line.strip().split(" ")
                n = params[0]
                m = params[1]
                q = params[2]
                continue

            # second line are nodes s and t
            elif i == 1:
                nodes = line.strip().split(" ")
                s = nodes[0]
                t = nodes[1]
                continue
            
            edge = line.strip().split(" ")
            if edge[0] not in G:
                G[edge[0]] = {edge[1] : edge[2]}
            else:
                G[edge[0]][edge[1]] = edge[2]

    answer = find_cheapest_walks(G, s, t, int(q))
    print(*answer, end="")