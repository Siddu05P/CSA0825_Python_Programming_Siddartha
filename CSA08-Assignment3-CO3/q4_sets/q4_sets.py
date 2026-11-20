import random, time, sys, copy, re
from collections import deque, Counter

def tm(f, *a):
    s = time.perf_counter(); r = f(*a); return r, time.perf_counter() - s


print("\n=== Q4 Sets ===")
ai = {"192311001", "192311004", "192311007", "192311009"}
iot = {"192311002", "192311004", "192311009", "192311010"}
allst = {f"1923110{i:02d}" for i in range(1, 11)}
both = ai & iot; exactly_one = ai ^ iot; neither = allst - (ai | iot)
print("clash      :", sorted(both)); print("exactly one:", sorted(exactly_one)); print("neither    :", sorted(neither))
b2, e2, n2 = ai.intersection(iot), ai.symmetric_difference(iot), allst.difference(ai.union(iot))
print("methods same:", (both, exactly_one, neither) == (b2, e2, n2))
print("empty:", set() & ai, "| identical:", ai & ai == ai, (ai ^ ai))
for n in (10_000, 100_000, 1_000_000):
    L = list(range(n)); S = set(L); target = n - 1
    s = time.perf_counter(); [target in L for _ in range(20)]; tl = (time.perf_counter()-s)/20
    s = time.perf_counter(); [target in S for _ in range(20)]; ts = (time.perf_counter()-s)/20
    print(f"n={n:8d} in list {tl*1e6:9.1f} us | in set {ts*1e6:6.2f} us")
def common_loops(a, b): return [x for x in a if any(x == y for y in b)]
for n in (500, 2000, 4000):
    A = list(range(n)); B = list(range(n//2, n + n//2))
    r1, t1 = tm(common_loops, A, B); r2, t2 = tm(lambda: sorted(set(A) & set(B)))
    print(f"n={n} nested={t1:.4f}s set&={t2:.5f}s same={sorted(r1)==r2}")

