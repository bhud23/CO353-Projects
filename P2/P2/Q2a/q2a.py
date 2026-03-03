import sys
# import DSU
# python q2a.py < tests/test.in > tests/test.out; diff test.out test.expect

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

def find_t_vals(n, blue, red):
    ans = [0] * (n - 1)

    for u, v, d, idx in red:
        dsu = DSU(n) # special class i made for disjoint set union

        # add the red edges with smaller rd val than fixed d val
        for ru, rv, rd, _ in red:
            if rd < d:
                dsu.union(ru, rv)

        if dsu.same(u, v): # if u and v are in the same connected component
            ans[idx] = -d
            continue

        thresh = None # threshold blue edges must be less than
        i = 0
        b_len = len(blue)

        while i < b_len:
            c = blue[i][2] # cost c at index 2 in blue

            while i < b_len and blue[i][2] == c:
                a, b, _, _ = blue[i] # edge a->b in blue tree
                dsu.union(a, b)
                i += 1

            if dsu.same(u, v):
                thresh = c
                break

        ans[idx] = thresh - d # maximum threshold minus d equals max t val

    return ans

if __name__ == "__main__":
    n = -1
    B = [] # adjecency lists for blue/red tree
    R = []

    data = sys.stdin.buffer.read().split()
    if not data:
        exit(0)
    
    it = iter(data)

    n = int(next(it))

    B = []
    for i in range(n - 1):
        u = int(next(it))
        v = int(next(it))
        c = int(next(it))
        B.append((u, v, c, i))

    R = []
    for i in range(n - 1):
        u = int(next(it))
        v = int(next(it))
        d = int(next(it))
        R.append((u, v, d, i))

    B.sort(key=lambda x: x[2])  # sort by the cost value in increasing order

    answer = find_t_vals(n, B, R)
    print(*answer, end="")

    