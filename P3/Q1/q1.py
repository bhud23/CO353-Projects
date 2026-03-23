import sys
from math import hypot

def solve (customers, tol = 1e-9, max_iters = 10_000, eps = 1e-12):
    total_demand = sum(d for _, _, d in customers)

    # good inital value for depot is weighed average for x and y coords
    x = sum(cx * d for cx, _, d in customers) / total_demand
    y = sum(cy * d for _, cy, d in customers) / total_demand

    for _ in range(max_iters):
        numerator_x = 0.0
        numerator_y = 0.0
        denominator = 0.0

        for cx, cy, d in customers:
            dist = hypot(x - cx, y - cy)

            if dist < eps: # this avoids instability/errors by avoiding diving by numbers near 0. we cna just return if we're going to put depot on top of customer
               return cx, cy

            w = d / dist
            numerator_x += w * cx
            numerator_y += w * cy
            denominator += w

        x_new = numerator_x / denominator
        y_new = numerator_y / denominator

        if hypot(x_new - x, y_new - y) < tol: # break loop and return if dist between old depot and new depot is too small, for efficiency
            return x_new, y_new

        x, y = x_new, y_new

    return x, y

if __name__ == "__main__":
    n = -1
    customers = []

    data = sys.stdin.buffer.read().split()
    if not data:
        exit(0)
    
    it = iter(data)

    n = int(next(it)) # i don't think we actually need this

    for _ in range(n):
        x = int(next(it))
        y = int(next(it))
        d = int(next(it))
        customers.append((x, y, d))

    x, y = solve(customers)

    print(f"{x:.6f} {y:.6f}")