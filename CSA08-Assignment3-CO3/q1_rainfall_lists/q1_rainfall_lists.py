import random, time, sys, copy, re
from collections import deque, Counter

def tm(f, *a):
    s = time.perf_counter(); r = f(*a); return r, time.perf_counter() - s


print("=== Q1 Rainfall ===")
random.seed(1)
def gen(n): return [0 if random.random() < 0.6 else round(random.uniform(0.5, 60), 1) for _ in range(n)]
readings = gen(365)
weeks = [round(sum(readings[i:i+7]), 1) for i in range(0, len(readings), 7)]
mx, mn = max(weeks), min(weeks)
print("weeks:", len(weeks), "wettest week#", weeks.index(mx)+1, mx, "driest week#", weeks.index(mn)+1, mn)
print("max day", max(readings), "at", readings.index(max(readings)), "| dry days:", readings.count(0))
dry_days = [i for i, r in enumerate(readings) if r == 0]
def ma_naive(x, w=7):
    adds = 0; out = []
    for i in range(len(x) - w + 1):
        s = 0
        for j in range(i, i + w): s += x[j]; adds += 1
        out.append(s / w)
    return out, adds
def ma_running(x, w=7):
    if len(x) < w: return [], 0
    adds = 0; s = sum(x[:w]); adds += w - 1; out = [s / w]
    for i in range(w, len(x)):
        s += x[i] - x[i-w]; adds += 2; out.append(s / w)
    return out, adds
print("slices:", readings[7:14] == readings[7:14], len(readings[-7:]), len(readings[::7]))
for n in (365, 36500, 365000):
    x = gen(n)
    (a, ca), ta = tm(ma_naive, x); (b, cb), tb = tm(ma_running, x)
    print(f"n={n:6d} naive adds={ca:8d} t={ta:.4f}s | running adds={cb:8d} t={tb:.4f}s | same={all(abs(p-q)<1e-6 for p,q in zip(a,b))}")
print("empty:", ma_naive([]), ma_running([]), "short:", ma_naive([1,2,3]), ma_running([1,2,3]))
big = list(range(1_000_000)); s = time.perf_counter(); big.insert(0, -1); print("insert at 0 on 1M list: %.5fs" % (time.perf_counter()-s))
def ma_deque(x, w=7):
    d = deque(maxlen=w); out = []
    for v in x:
        d.append(v)
        if len(d) == w: out.append(sum(d) / w)
    return out
x = gen(36500); (_, _), t1 = tm(ma_running, x); _, t2 = tm(ma_deque, x); print(f"running {t1:.4f}s deque(sum) {t2:.4f}s")

