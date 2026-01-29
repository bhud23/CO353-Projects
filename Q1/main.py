import sys

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
    
    print("running")
    print(n, m, q, s, t)
    print(G)