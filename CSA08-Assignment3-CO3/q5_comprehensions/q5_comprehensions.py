import random, time, sys, copy, re
from collections import deque, Counter

def tm(f, *a):
    s = time.perf_counter(); r = f(*a); return r, time.perf_counter() - s


print("\n=== Q5 Comprehensions ===")
def mkT(n): return [random.uniform(-60, 60) for _ in range(n)]
def v_loop(r):
    c = []
    for t in r:
        if -50 <= t <= 50: c.append(t)
    f = []
    for t in c: f.append(t * 9 / 5 + 32)
    return c, f
def v_comp(r):
    c = [t for t in r if -50 <= t <= 50]; return c, [t * 9 / 5 + 32 for t in c]
def v_map(r):
    c = list(filter(lambda t: -50 <= t <= 50, r)); return c, list(map(lambda t: t * 9 / 5 + 32, c))
for n in (10_000, 100_000, 1_000_000):
    R = mkT(n); a, t1 = tm(v_loop, R); b, t2 = tm(v_comp, R); c, t3 = tm(v_map, R)
    print(f"n={n:8d} loop={t1:.4f}s comp={t2:.4f}s map/filter={t3:.4f}s identical={a==b==c}")
R = mkT(1000)
alarms = [i for i, t in enumerate(R) if not 2 <= t <= 8]
lc = [t for t in range(1_000_000)]; ge = (t for t in range(1_000_000))
print("getsizeof list comp", sys.getsizeof(lc), "generator", sys.getsizeof(ge))
print("all-valid:", len(v_comp([5.0]*10)[0]), "all-invalid:", len(v_comp([99.0]*10)[0]))
print({i: t for i, t in enumerate([1, 99, 5]) if -50 <= t <= 50}, {round(t) for t in [1.2, 1.4, 5]})
R = mkT(1_000_000)
_, ta = tm(lambda: sum([c for c in R if -50 <= c <= 50])); _, tb = tm(lambda: sum(c for c in R if -50 <= c <= 50))
print(f"sum(list) {ta:.4f}s sum(gen) {tb:.4f}s")

