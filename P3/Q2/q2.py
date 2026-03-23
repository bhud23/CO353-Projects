import sys
from collections import defaultdict

n = None
d = {}
neighbours = defaultdict(list)

# Get input O(n)
for i, line in enumerate(sys.stdin):
  line = line.strip()
  if not line:
    continue
  elif i == 0:
    n = int(line)
    continue
  elif i == 1:
    demands = map(int, line.split())
    for j, demand in enumerate(demands):
      d[j + 1] = demand
  elif i <= n:
    j, k = map(int, line.split())
    neighbours[k].append(j)
    neighbours[j].append(k)

D = sum(d.values())

# Idea: traverse down, up, and back down the tree
#   this should be O(3n) so long as numerical values are used rather than lists

# Details:
#   Let x be the node we care about
#   Let X_d be the depot value of X
#   Let y be the node that is the parent of x
#   Let Y_d be the depot value of Y
#   Let L be the set of vertices that are descendents of x (including x)
#   We know the depot value of y is:
#   Y_d = sum(d[i]*c(i,y), for i=1..n)
#   = X_d + sum(d[i] for i in L) - sum(d[i] for i not in L)
#   = X_d + sum(d[i] for i in L) - (D - sum(d[i] for i in L))
#   = X_d + 2 * sum(d[i] for i in L) - D
#   Thus:
#   X_d = Y_d + D - 2 * sum(d[i] for i in L)

root = 1 # set root to arbitrary node
descendent_demand_sum = {} # sum(d[i] for i in L[x]): defaults to 0

# Traverse down and up once - O(2n)
def find_descendent_demands(node, parent):
    descendent_demand_sum[node] = d[node]

    # Get children
    children = list(filter(lambda n: n != parent, neighbours[node]))

    # Leaf
    if not len(children):
        return [d[node]]

    # Find child_demands
    child_demands = []
    for child in children:
        demands = find_descendent_demands(child, node)
        for i in range(len(demands)):
            if len(child_demands) > i:
                child_demands[i] += demands[i]
            else:
                child_demands.append(demands[i])

    # Set descendents value
    descendent_demand_sum[node] = d[node] + sum(child_demands)

    # Add node to child_demands and return
    child_demands.insert(0, d[node])
    return child_demands

root_depot_value = 0
for i, demand in enumerate(find_descendent_demands(root, None)):
    root_depot_value += i * demand

# Create depot_values dict
depot_values = {}
depot_values[root] = root_depot_value

# Based on the equation of X_d above and the known depot value of root we can descend down
def set_depot_values(node, parent):
    depot_values[node] = depot_values[parent] + D - 2 * descendent_demand_sum[node]

    children = list(filter(lambda n: n != parent, neighbours[node]))
    for child in children:
       set_depot_values(child, node)

# Traverse back down the tree - O(n)
root_children = filter(lambda x: x != root, neighbours[root])
for child in root_children:
    set_depot_values(child, root)

# Check each node to find the minimum - O(n)
min_value = None
min_key = None
for node, v in depot_values.items():
    if min_value == None:
       min_value = v
       min_key = node
    elif v < min_value:
        min_value = v
        min_key = node

# Output the solution
print(min_key)
