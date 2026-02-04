from .graphs import SegTreeGraph

def q2_input(input):
    n, q, s = 0, 0, 0

    if not input:
        return SegTreeGraph(0, [])

    input_arcs = []

    # read lines to generate graph G
    for i, line in enumerate(input):
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
    g = SegTreeGraph(n, input_arcs)

    return g, s