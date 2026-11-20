import csv, io, sqlite3, time, random, statistics, cProfile, pstats, tracemalloc, os, sys
from collections import defaultdict, Counter
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("charts", exist_ok=True)
random.seed(7)

# =============== B1.1 small dirty file ===============
print("=== B1.1 Clean a small file with every problem ===")
DIRTY = """station,date,hour,pm25,pm10,no2,temp
Adyar,2026-10-01,8,48,80,30,30.0
Adyar,2026-10-01,9,NA,82,31,31.0
Adyar,2026-10-01,10,,85,32,31.5
Adyar,2026-10-01,11,-5,90,33,32.0
Adyar,2026-10-01,12,5000,95,34,32.5
Adyar,2026-10-01,8,48,80,30,30.0
Guindy,2026-10-01,8,95,150,60,86.0
Guindy,2026-10-01,9,121,170,65,89.6
"""
F_STATIONS = {"Guindy"}              # stations that report in Fahrenheit
def to_float(x):
    x = (x or "").strip()
    if x == "" or x.upper() == "NA": return None
    try: return float(x)
    except ValueError: return None
def clean_rows(text, fahrenheit=F_STATIONS, max_pm=999):
    seen, out, log = set(), [], Counter()
    for r in csv.DictReader(io.StringIO(text)):
        key = (r["station"], r["date"], r["hour"])
        if key in seen: log["duplicate"] += 1; continue
        seen.add(key)
        pm = to_float(r["pm25"])
        if pm is None: log["missing"] += 1; continue
        if pm < 0 or pm > max_pm: log["impossible"] += 1; continue
        t = to_float(r["temp"])
        if t is not None and r["station"] in fahrenheit: t = round((t - 32) * 5 / 9, 1)
        out.append((r["station"].strip().title(), r["date"], int(r["hour"]), pm, to_float(r["pm10"]), to_float(r["no2"]), t))
    return out, log
print("BEFORE:"); print(DIRTY)
cl, log = clean_rows(DIRTY)
print("AFTER:"); [print(r) for r in cl]; print("removed:", dict(log))

# =============== B1 Complete the Code ===============
print("\n=== B1 Complete the Code ===")
RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
Guindy,2026-10-04,5000
"""
def load_clean(text):
    rows = []
    for r in csv.DictReader(io.StringIO(text)):
        v = r["pm25"].strip()
        if v == "" or v.upper() == "NA": continue
        v = float(v)
        if v < 0 or v > 999: continue            # extra check: > 999 is a sensor fault
        rows.append((r["station"], r["date"], v))
    return rows
def min_max(values):
    lo, hi = min(values), max(values)
    return [round((v - lo) / (hi - lo), 3) for v in values]
clean = load_clean(RAW); print(clean); print(min_max([pm for _, _, pm in clean]))
def z_score(values):
    m, s = statistics.mean(values), statistics.pstdev(values)
    return [round((v - m) / s, 3) for v in values]
print("z-scores:", z_score([pm for _, _, pm in clean]))

# =============== synthetic network data ===============
STATIONS = ["Adyar", "Guindy", "T Nagar", "Velachery", "Manali", "Alandur", "Anna Nagar", "Kodambakkam", "Perungudi", "Royapuram", "Tambaram", "Besant Nagar"]
def gen_station_rows(stations, days, seed=1):
    rnd = random.Random(seed); rows = []
    for si, st in enumerate(stations):
        base = 40 + (si * 7) % 50
        for d in range(days):
            for h in range(24):
                rush = 25 if h in (8, 9, 18, 19, 20) else 0
                temp = round(26 + 6 * (1 if 11 <= h <= 16 else 0) + rnd.gauss(0, 1.5), 1)
                pm = max(1, round(base + rush + (temp - 28) * 1.5 + rnd.gauss(0, 10) + d * 0.4, 1))
                rows.append((st, f"2026-10-{d+1:02d}", h, pm, temp))
    return rows
data = gen_station_rows(STATIONS, 30)
print("\ngenerated", len(data), "clean readings")

# =============== B1.3 SQLite ===============
print("\n=== B1.3 Store and query ===")
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE stations (station_id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL)")
con.execute("CREATE TABLE readings (station TEXT NOT NULL, day TEXT NOT NULL, hour INTEGER NOT NULL, pm25 REAL, temp_c REAL, PRIMARY KEY (station, day, hour))")
con.executemany("INSERT INTO stations (name) VALUES (?)", [(s,) for s in STATIONS])
con.executemany("INSERT INTO readings VALUES (?,?,?,?,?)", data); con.commit()
q1 = con.execute("SELECT ROUND(AVG(pm25),2) FROM readings WHERE station=? AND day LIKE '2026-10-%'", ("Adyar",)).fetchone()
q2 = con.execute("SELECT station, ROUND(AVG(pm25),1) a FROM readings GROUP BY station ORDER BY a DESC LIMIT 3").fetchall()
q3 = con.execute("SELECT hour, ROUND(AVG(pm25),1) a FROM readings GROUP BY hour ORDER BY a DESC LIMIT 3").fetchall()
print("Q1 avg PM2.5 Adyar Oct:", q1); print("Q2 3 worst stations:", q2); print("Q3 3 worst hours:", q3)

# =============== B1.4 charts ===============
daily = con.execute("SELECT day, AVG(pm25) FROM readings WHERE station='Adyar' GROUP BY day ORDER BY day").fetchall()
plt.figure(figsize=(7, 3.6)); plt.plot([int(d[-2:]) for d, _ in daily], [v for _, v in daily], marker="o")
plt.xlabel("Day of October 2026"); plt.ylabel("Daily mean PM2.5 (ug/m3)"); plt.title("Adyar: PM2.5 trend over October"); plt.grid(alpha=.3); plt.tight_layout(); plt.savefig("charts/trend.png", dpi=130); plt.close()
sa = con.execute("SELECT station, AVG(pm25) FROM readings GROUP BY station ORDER BY 2 DESC").fetchall()
plt.figure(figsize=(7, 3.8)); plt.bar([s for s, _ in sa], [v for _, v in sa]); plt.xticks(rotation=60, ha="right")
plt.ylabel("Mean PM2.5 (ug/m3)"); plt.xlabel("Station"); plt.title("Mean PM2.5 by station"); plt.tight_layout(); plt.savefig("charts/stations.png", dpi=130); plt.close()
tp = con.execute("SELECT temp_c, pm25 FROM readings WHERE station='Adyar'").fetchall()
plt.figure(figsize=(6, 4)); plt.scatter([t for t, _ in tp], [p for _, p in tp], s=6, alpha=.5)
plt.xlabel("Temperature (C)"); plt.ylabel("PM2.5 (ug/m3)"); plt.title("Adyar: temperature vs PM2.5"); plt.tight_layout(); plt.savefig("charts/scatter.png", dpi=130); plt.close()
hr = con.execute("SELECT hour, AVG(pm25) FROM readings GROUP BY hour ORDER BY hour").fetchall()
plt.figure(figsize=(7, 3.6)); plt.bar([h for h, _ in hr], [v for _, v in hr]); plt.xlabel("Hour of day"); plt.ylabel("Mean PM2.5 (ug/m3)")
plt.title("Average PM2.5 by hour (all stations)"); plt.tight_layout(); plt.savefig("charts/hours.png", dpi=130); plt.close()
xs = [t for t, _ in tp]; ys = [p for _, p in tp]
print("correlation temp vs PM2.5 (Adyar):", round(statistics.correlation(xs, ys), 3))
print("worst hour:", max(hr, key=lambda x: x[1]), "| best hour:", min(hr, key=lambda x: x[1]))

# =============== pandas vs csv cleaning, 1k / 100k / 1M ===============
print("\n=== B1 alt: csv loops vs pandas cleaning ===")
def make_csv(n):
    rnd = random.Random(3); lines = ["station,date,pm25"]
    for i in range(n):
        r = rnd.random(); v = "NA" if r < .03 else "" if r < .05 else "-5" if r < .06 else str(round(rnd.uniform(10, 200), 1))
        lines.append(f"S{i%12},2026-10-{i%28+1:02d},{v}")
    return "\n".join(lines) + "\n"
def clean_csv(text):
    out = []
    for r in csv.DictReader(io.StringIO(text)):
        v = r["pm25"].strip()
        if v == "" or v.upper() == "NA": continue
        v = float(v)
        if v < 0 or v > 999: continue
        out.append(v)
    lo, hi = min(out), max(out)
    return [(v - lo) / (hi - lo) for v in out]
def clean_pd(text):
    df = pd.read_csv(io.StringIO(text), na_values=["NA", ""])
    df = df.dropna(subset=["pm25"]); df = df[(df.pm25 >= 0) & (df.pm25 <= 999)]
    return ((df.pm25 - df.pm25.min()) / (df.pm25.max() - df.pm25.min())).tolist()
for n in (1000, 100000, 1000000):
    txt = make_csv(n)
    s = time.perf_counter(); a = clean_csv(txt); t1 = time.perf_counter() - s
    s = time.perf_counter(); b = clean_pd(txt); t2 = time.perf_counter() - s
    tracemalloc.start(); clean_csv(txt); m1 = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"n={n:8d} csv loop {t1:.3f}s ({m1/1e6:.1f} MB peak) | pandas {t2:.3f}s | same count {len(a)==len(b)} maxdiff {max(abs(x-y) for x,y in zip(a[:1000], b[:1000])):.1e}")

