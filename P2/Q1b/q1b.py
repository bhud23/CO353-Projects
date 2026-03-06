import sys

n = m = k = -1
lines = []
colours = {}

# Get input O(m)
for i, line in enumerate(sys.stdin): 
  line = line.strip()
  if not line:
    continue
  elif i == 0:
    n, m, k = map(int, line.split())
    continue
  elif i <= m:
    # Read line
    l, r, c = map(int, line.split())

    # If length is not greater than capacity do nothing (since this line restricts nothing)
    if r - l + 1 <= c:
      continue

    # Sort into the lines array
    lines.append((l, r, c))
  else:
    # Read point colour
    colours[i - m] = line

# Sort lines by size O(m log m)
#lines.sort(key=lambda line: line[1] - line[0])

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

    # Set red/blue counts O(n)
    self.set_colour_counts(self.root)

    # Add range nodes O(m log n)
    for line in lines:
      l, r, c = line

      # find relevant intervals O(log n)
      useful_intervals = self.find_corresponding_intervals((l, r), (1, n))
      
      # Set max points and colours for each interval O(m log n)
      c_red = c_blue = c
      for interval in useful_intervals:
        node = self.nodes[interval]
        # Max points
        if c > 0:
          if c >= node.max_points:
            c -= node.max_points
          else:
            node.max_points = c
            c = 0
        else:
          node.max_points = 0
        # Max red
        if c_red > 0:
          if c_red >= node.max_red:
            c_red -= node.max_red
          else:
            node.max_red = c_red
            c_red = 0
        else:
          node.max_red = 0
        # Max blue
        if c_blue > 0:
          if c_blue >= node.max_blue:
            c_blue -= node.max_blue
          else:
            node.max_blue = c_blue
            c_blue = 0
        else:
          node.max_blue = 0

    # Set points for all intervals O(n)
    self.set_points(self.root)

  # Recursivly add the segtree nodes to cover the entire range
  def build_default_tree(self, parent):
    self.nodes[(parent.l, parent.r)] = parent
    if parent.l == parent.r: return
    self.build_default_tree(Node(parent.l, parent.mid))
    self.build_default_tree(Node(parent.mid + 1, parent.r))

  # Sets the max of each colour at every node
  def set_colour_counts(self, node):
    if node.l == node.r:
      node.max_red = 1 if colours[node.l] == 'R' else 0
      node.max_blue = 1 - node.max_red
    else:
      l_max_red, l_max_blue = self.set_colour_counts(self.nodes[node.left])
      r_max_red, r_max_blue = self.set_colour_counts(self.nodes[node.right])
      node.max_red = l_max_red + r_max_red
      node.max_blue = l_max_blue + r_max_blue
    return node.max_red, node.max_blue

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
      if node.max_points:
        node.max_red = 1 if colours[node.l] == 'R' and node.max_red != 0 else 0
        node.max_blue = 1 - node.max_red
    else:
      left_points, l_max_red, l_max_blue = self.set_points(self.nodes[node.left])
      right_points, r_max_red, r_max_blue = self.set_points(self.nodes[node.right])
      node.points = min(left_points + right_points, node.max_points)
      node.max_red = min(l_max_red + r_max_red, node.max_red)
      node.max_blue = min(l_max_blue + r_max_blue, node.max_blue)
    return node.points, node.max_red, node.max_blue

# Build the tree
tree = SegTree(n, lines)

# Return
max_points = tree.root.points
min_red = max(tree.root.points - tree.root.max_blue, 0)
max_red = min(tree.root.max_red, tree.root.points)
k_red = int(min_red <= k and k <= max_red)
print(max_points, min_red, max_red, k_red)

# Total time complexity = O(n + m log n)
