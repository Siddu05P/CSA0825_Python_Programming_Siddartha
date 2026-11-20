import random, time, sys, copy, re
from collections import deque, Counter

def tm(f, *a):
    s = time.perf_counter(); r = f(*a); return r, time.perf_counter() - s


print("\n=== Q6 Railway ===")
def make_tt(n, stations=50):
    tt = {}
    for t in range(n):
        k = random.randint(4, 8); st = random.sample(range(stations), k); h = random.randint(0, 15) * 60
        route = []
        for s in st: h += random.randint(20, 90); route.append((f"S{s}", f"{h//60%24:02d}:{h%60:02d}", f"{(h+2)//60%24:02d}:{(h+2)%60:02d}"))
        tt[10000 + t] = {"name": f"Train{t}", "route": route, "days": set(random.sample(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], random.randint(3, 7)))}
    return tt
def query(tt, st, day):
    res = [(tn, [dep for s, arr, dep in d["route"] if s == st][0]) for tn, d in tt.items() if day in d["days"] and any(s == st for s, _, _ in d["route"])]
    return sorted(res, key=lambda p: p[1])
def build_index(tt):
    idx = {}
    for tn, d in tt.items():
        for s, arr, dep in d["route"]: idx.setdefault(s, []).append((tn, dep))
    return idx
def query_idx(tt, idx, st, day): return sorted([(tn, dep) for tn, dep in idx.get(st, []) if day in tt[tn]["days"]], key=lambda p: p[1])
small = {12627: {"name": "Karnataka Exp", "route": [("SBC", "00:00", "19:20"), ("JTJ", "21:00", "21:02"), ("MAS", "23:30", "23:30")], "days": {"Mon", "Tue"}}}
print(small[12627]["route"][2][2], query(small, "JTJ", "Mon"), query(small, "XXX", "Mon"), query(small, "JTJ", "Fri"))
import tracemalloc
for n in (100, 1000, 10000):
    tt = make_tt(n)
    tracemalloc.start(); idx = build_index(tt); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    s = time.perf_counter(); [query(tt, "S7", "Mon") for _ in range(20)]; t1 = (time.perf_counter()-s)/20
    s = time.perf_counter(); [query_idx(tt, idx, "S7", "Mon") for _ in range(20)]; t2 = (time.perf_counter()-s)/20
    print(f"trains={n:6d} scan={t1*1e3:8.3f} ms  index={t2*1e3:7.3f} ms  index memory={mem/1024:.1f} KiB  same={query(tt,'S7','Mon')==query_idx(tt,idx,'S7','Mon')}")

