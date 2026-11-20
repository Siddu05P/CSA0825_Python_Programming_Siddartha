import random, time, sys, copy, re
from collections import deque, Counter

def tm(f, *a):
    s = time.perf_counter(); r = f(*a); return r, time.perf_counter() - s


print("\n=== Q2 Tuples/copy ===")
rows, cols = 3, 4
bad = [[0] * cols] * rows
bad[0][1] = 7
good = [[0] * cols for _ in range(rows)]
good[0][1] = 7
print("bad :", bad); print("good:", good); print(bad[0] is bad[1], good[0] is good[1])
print([id(r) for r in bad][:2], [id(r) for r in good][:2])
stops = {(13.0827, 80.2707): "Chennai Central", (13.0418, 80.2341): "T. Nagar"}
print(stops[(13.0418, 80.2341)])
try: {[13.0418, 80.2341]: "x"}
except TypeError as e: print("TypeError:", e)
for (lat, lon), name in stops.items(): print(name, lat, lon)
a = [[1, 2], [3, 4]]; alias = a; sh = copy.copy(a); sl = a[:]; dp = copy.deepcopy(a)
a[0][0] = 99
print("alias", alias, "| shallow", sh, "| slice", sl, "| deep", dp)
a.append([5]); print("after append: alias", len(alias), "shallow", len(sh))
def change(lst): lst.append("X")
L = [1]; change(L); print("caller list:", L)
lst = list(range(1_000_000)); tup = tuple(lst)
print("getsizeof list", sys.getsizeof(lst), "tuple", sys.getsizeof(tup))
for name, f in (("list create", lambda: list(range(1_000_000))), ("tuple create", lambda: tuple(range(1_000_000)))):
    _, t = tm(f); print(name, f"{t:.4f}s")
def idx(c):
    for i in range(0, 1_000_000, 1000): c[i]
print("index list", f"{tm(idx, lst)[1]:.5f}s", "tuple", f"{tm(idx, tup)[1]:.5f}s")
t = ([1, 2], 3)
try: t[0] += [3]
except TypeError as e: print("TypeError:", e, "| tuple is now", t)
sparse = {}; sparse[(0, 1)] = sparse.get((0, 1), 0) + 7
print("sparse grid", sparse, "dense cells 3x4 =", rows*cols)

