import sys

n = m = -1
lines = []

# Get input O(m)
for i, line in enumerate(sys.stdin): 
  line = line.strip()
  if not line:
    continue
  elif i == 0:
    n, m = map(int, line.split())
    continue

  l, r, c = map(int, line.split())

  # If length is not greater than capacity do nothing (since this line restricts nothing)
  if r - l + 1 <= c:
    continue

  # Sort into the lines array
  lines.append((l, r, c))

class Node:
  def __init__(self, l, r):
    self.l = l
    self.r = r
    self.max_points = r - l + 1
    self.mid = (l + r) // 2
    self.left = (l, self.mid)
    self.right = (self.mid + 1, r)

class SegTree:
  # O(n + m log n)
  def __init__(self, n, lines):
    self.root = Node(1, n)
    self.nodes = {}

    # Build tree structure O(n)
    self.build_default_tree(self.root)

    # Add range nodes O(m log n)
    for line in lines:
      l, r, c = line

      # find relevant intervals O(log n)
      useful_intervals = self.find_corresponding_intervals((l, r), (1, n))
      
      # Set max points for each interval O(m log n)
      for interval in useful_intervals:
        node = self.nodes[interval]
        if c > 0:
          if c >= node.max_points:
            c -= node.max_points
          else:
            node.max_points = c
            c = 0
        else:
          node.max_points = 0

    # Set points for all intervals O(n)
    self.set_points(self.root)

  # Recursivly add the segtree nodes to cover the entire range
  def build_default_tree(self, parent):
    self.nodes[(parent.l, parent.r)] = parent
    if parent.l == parent.r: return
    self.build_default_tree(Node(parent.l, parent.mid))
    self.build_default_tree(Node(parent.mid + 1, parent.r))

  # Find intervals to cover a range
  def find_corresponding_intervals(self, search_interval, check_interval):
    search_left, search_right = search_interval
    check_left, check_right = check_interval
    if search_left == check_left and search_right == check_right:
      return [check_interval]
    
    corresponding_intervals = []

    check_mid = (check_left + check_right) // 2
    if search_left <= check_mid:
      corresponding_intervals += self.find_corresponding_intervals(
        (search_left, min(search_right, check_mid)), (check_left, check_mid))
    if search_right > check_mid:
      corresponding_intervals += self.find_corresponding_intervals(
        (max(check_mid + 1, search_left), search_right), (check_mid + 1, check_right))

    return corresponding_intervals
  
  # Recursivly upadate node points to reflect the max points and children
  def set_points(self, node):
    if node.l == node.r:
      node.points = node.max_points
    else:
      left_points = self.set_points(self.nodes[node.left])
      right_points = self.set_points(self.nodes[node.right])
      node.points = min(left_points + right_points, node.max_points)
    return node.points

# Build the tree
tree = SegTree(n, lines)

# Return the max number of points
print(tree.root.points)

# Total time complexity = O(n + m log n)
