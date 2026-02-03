class Node:
    """
    _id (Str)
    weight (Int)
    """
    def __init__(self, id, weight = None):
        self._id = id
        self.weight = weight

class Arc:
    """
    node_out (Node)
    node_in (Node)
    weight (Int)
    """
    def __init__(self, node_out, node_in, weight = None):    
        self.node_out = node_out
        self.node_in = node_in
        self.weight = weight

class Digraph:
    """
    _arc_matrix (dictof Str (listof Arc))
    _node_list (listof Node)
    """
    def __init__(self, num_nodes, node_weights=None, arcs=None):
        # Set data objects
        self._arc_matrix = [[None for _ in range(num_nodes)] for _ in range(num_nodes)]
        self._node_list = []

        # Create nodes
        if node_weights:
            for i, weight in enumerate(node_weights):
                new = Node(i, weight)
                self._node_list.append(new)
        else:
            for node in range(num_nodes):
                new = Node(node)
                self._node_list.append(new)

        # Create arcs
        for arc in arcs:
            node_out = arc[0]
            node_in = arc[1]
            weight = arc[2]
            new_arc = Arc(node_out, node_in, weight)
            existing_arc = self._arc_matrix[node_out-1][node_in-1]
            if (not existing_arc or existing_arc.weight > new_arc.weight):
                self._arc_matrix[node_out-1][node_in-1] = new_arc

    def get_node(self, id):
        return self._node_list[id - 1]
    
    def get_arc(self, node_out, node_in):
        return self._arc_matrix[node_out-1][node_in-1]
          
    def nodes(self):
      return list(map(lambda node: node._id, self._node_list))

    def arcs(self):     
        arc_list = []
        for arcs in self._arc_matrix:
            arc_list = arc_list + arcs
        return arc_list
    
    def is_arc(self, node_out, node_in):
        return self._arc_matrix[node_out-1][node_in-1] != None
    
    def out_arcs(self, node_id):
        return list(filter(bool, self._arc_matrix[node_id-1]))
    
    def in_arcs(self, node_id):
        in_arcs = []
        for arcs in self._arc_matrix:
            if arcs[node_id-1] != None:
                in_arcs.append(arcs[node_id-1])
        return in_arcs

    def node_weight(self, node_id):
        return self._node_list[node_id-1].weight

    def arc_weight(self, node_out, node_in):
        arc = self._arc_matrix[node_out-1][node_in-1]
        return None if arc == None else arc.weight

    def set_node_weight(self, id, weight):     
        self._node_list[id-1].weight = weight
     
    def set_arc_weight(self, node_out, node_in, weight):
        self._arc_matrix[node_out-1][node_in-1].weight = weight
