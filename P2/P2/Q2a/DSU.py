# custom class for a disjoint-set union DS
class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1) # array of 1s

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)

        if ra == rb:
            return False
        
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra # swap
        
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

    def same (self, a, b):
        return self.find(a) == self.find(b)