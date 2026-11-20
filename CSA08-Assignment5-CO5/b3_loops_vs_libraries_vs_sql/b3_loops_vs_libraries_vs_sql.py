import csv, io, sqlite3, time, random, statistics, cProfile, pstats, tracemalloc, os, sys
from collections import defaultdict, Counter
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("charts", exist_ok=True)
random.seed(7)

# =============== B3 loops vs pandas vs SQL ===============
print("\n=== B3 Loops vs pandas vs SQL ===")
def write_csv(path, stations, days=365):
    rnd = random.Random(5)
    with open(path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["station", "date", "hour", "pm25"])
        for s in range(stations):
            for d in range(days):
                dt = f"2026-{d//31+1:02d}-{d%31+1:02d}"
                for h in range(24):
                    if (d * 24 + h) % 3 == 0 and False: continue
                    w.writerow([f"S{s}", dt, h, round(rnd.uniform(5, 200), 1)])
def daily_loops(path):
    groups = defaultdict(list)
    with open(path, newline="") as f:
        for r in csv.DictReader(f): groups[(r["station"], r["date"])].append(float(r["pm25"]))
    return {k: statistics.mean(v) for k, v in groups.items()}
def daily_running(path):
    sums = defaultdict(lambda: [0.0, 0])
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            a = sums[(r["station"], r["date"])]; a[0] += float(r["pm25"]); a[1] += 1
    return {k: a[0] / a[1] for k, a in sums.items()}
def daily_pandas(path):
    return pd.read_csv(path).groupby(["station", "date"]).pm25.mean().to_dict()
def daily_sql(path):
    c = sqlite3.connect(":memory:"); c.execute("CREATE TABLE r (station, date, hour, pm25)")
    with open(path, newline="") as f:
        rd = csv.reader(f); next(rd); c.executemany("INSERT INTO r VALUES (?,?,?,?)", ((a, b, int(h), float(p)) for a, b, h, p in rd))
    return {(s, d): m for s, d, m in c.execute("SELECT station, date, AVG(pm25) FROM r GROUP BY station, date")}
write_csv("small.csv", 1, 3)
r1, r2, r3, r4 = daily_loops("small.csv"), daily_pandas("small.csv"), daily_sql("small.csv"), daily_running("small.csv")
print("small-data agreement:", all(abs(r1[k] - r2[k]) < 1e-9 and abs(r1[k] - r3[k]) < 1e-9 and abs(r1[k] - r4[k]) < 1e-9 for k in r1), "| groups:", len(r1))
print("stations | rows | loops+statistics | running sum | pandas groupby | SQL")
for st in (1, 12, 120):
    write_csv("big.csv", st); n = st * 365 * 24; ts = []
    for fn in (daily_loops, daily_running, daily_pandas, daily_sql):
        s = time.perf_counter(); fn("big.csv"); ts.append(time.perf_counter() - s)
    print(f"{st:8d} | {n:9d} | {ts[0]:.3f}s | {ts[1]:.3f}s | {ts[2]:.3f}s | {ts[3]:.3f}s")
write_csv("big.csv", 12)
pr = cProfile.Profile(); pr.enable(); daily_loops("big.csv"); pr.disable()
st = pstats.Stats(pr); st.sort_stats("cumulative").print_stats(8)
os.remove("big.csv"); os.remove("small.csv")

