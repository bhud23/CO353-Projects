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
                heapq.heappush(mh, (d + w, u))

    return answers


if __name__ == "__main__":
    n = m = q = -1
    s = t = None
    G = {} # we represent the digraph as a dict of a dict where first key is tail, with value that is a dict with key that is head and value is weight of an edge

    for i, line in enumerate(sys.stdin):
        line = line.strip()
        if not line:
            continue  # skip blank lines

        if i == 0:
            n, m, q = map(int, line.split())
            continue

        if i == 1:
            s, t = line.split()
            # if your nodes are integers, do: s, t = map(int, line.split())
            continue

        u, v, w = line.split()
        w = int(w)  # or float(w) if weights can be non-integers

        G.setdefault(u, {})[v] = w
        G.setdefault(v, {})  # ensure v is in G

    answer = find_cheapest_walks(G, s, t, q)
    print(*answer, end="")