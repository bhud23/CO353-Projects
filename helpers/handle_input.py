from .graphs import Digraph

def q2_input(input):
    n, q, s = 0, 0, 0

    if not input:
        return Digraph(0)
    
    input_arcs = []

    # read lines to generate graph G
    for i, line in enumerate(input):
        # first line are paramters n, m, q
        if i == 0:
            params = line.strip().split(" ")
            n = int(params[0])
            q = int(params[1])
            s = int(params[2])
            continue
        elif q < i:
            break

        arcs = line.strip().split(" ")
        v = int(arcs[0])
        l = int(arcs[1])
        r = int(arcs[2])
        c = int(arcs[3])
        for node_in in range(l, r + 1):
            input_arcs.append((v, node_in, c))
    
    # Build G
    g = Digraph(n, None, input_arcs)

    return g, s