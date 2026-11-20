import random, time, sys, copy, re
from collections import deque, Counter

def tm(f, *a):
    s = time.perf_counter(); r = f(*a); return r, time.perf_counter() - s


print("\n=== Q3 Dictionaries ===")
calls = ["seeds not received seeds delayed", "fertiliser price high", "seeds price high subsidy not received"]
STOP = {"not", "high"}
def frequencies(texts, stop):
    d = {}
    for t in texts:
        for w in re.sub(r"[^\w\s]", "", t.lower()).split():
            if w not in stop: d[w] = d.get(w, 0) + 1
    return d
def top(counts, k): return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
print(top(frequencies(calls, STOP), 3))
print(frequencies([""], STOP), frequencies(["Seeds, SEEDS! seeds."], STOP))
by_district = {}
for d, c in [("Salem", "seeds late"), ("Erode", "price high"), ("Salem", "no fertiliser")]: by_district.setdefault(d, []).append(c)
print(by_district)
vocab = [f"w{i}" for i in range(300)]
def mk(n): return [" ".join(random.choice(vocab) for _ in range(8)) for _ in range(n)]
def count_list(texts):
    words = [w for t in texts for w in t.split()]
    return {w: words.count(w) for w in set(words)}
def count_counter(texts): return Counter(w for t in texts for w in t.split())
for n in (1000, 10000, 100000):
    T = mk(n); r1, t1 = tm(frequencies, T, set())
    if n <= 10000: r2, t2 = tm(count_list, T)
    else: r2, t2 = None, float('nan')
    r3, t3 = tm(count_counter, T)
    print(f"n={n:6d} dict={t1:.4f}s list.count={'skipped' if t2!=t2 else format(t2,'.4f')} Counter={t3:.4f}s same={r1==dict(r3)}")

