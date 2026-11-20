import csv, io, sqlite3, time, random, statistics, cProfile, pstats, tracemalloc, os, sys
from collections import defaultdict, Counter
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("charts", exist_ok=True)
random.seed(7)

# =============== B2 Adversarial ===============
print("\n=== B2 Adversarial data ===")
def safe_load(raw_bytes, delimiter=","):
    try: text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as e: return f"ENCODING ERROR: {e.reason}"
    if not text.strip(): return "EMPTY FILE"
    rd = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    need = {"station", "date", "pm25"}
    if not rd.fieldnames or not need <= set(rd.fieldnames): return f"MISSING COLUMNS: {sorted(need - set(rd.fieldnames or []))}"
    return f"OK {len(list(rd))} rows"
print("missing column  :", safe_load(b"station,date\nAdyar,2026-10-01\n"))
print("wrong delimiter :", safe_load(b"station;date;pm25\nAdyar;2026-10-01;48\n"))
print("latin-1 encoding:", safe_load("station,date,pm25\nPer\xe5ngudi,2026-10-01,48\n".encode("latin-1")))
print("empty file      :", safe_load(b""))
print("fixed delimiter :", safe_load(b"station;date;pm25\nAdyar;2026-10-01;48\n", ";"))
con2 = sqlite3.connect(":memory:"); con2.execute("CREATE TABLE aq (station TEXT, pm25 REAL)")
con2.executemany("INSERT INTO aq VALUES (?,?)", [("Adyar", 48), ("O'Brien Road", 70)])
try: con2.execute("SELECT * FROM aq WHERE station = '" + "O'Brien Road" + "'").fetchall()
except sqlite3.OperationalError as e: print("string + quote  -> OperationalError:", e)
print("? placeholder   ->", con2.execute("SELECT * FROM aq WHERE station = ?", ("O'Brien Road",)).fetchall())
evil = "x' OR '1'='1"
print("injection by +  ->", con2.execute("SELECT * FROM aq WHERE station = '" + evil + "'").fetchall(), "(ALL rows leaked)")
print("injection by ?  ->", con2.execute("SELECT * FROM aq WHERE station = ?", (evil,)).fetchall())
# B2 complete the code
readings = [("Adyar", "2026-10-01", 48.0), ("Guindy", "2026-10-01", 95.0), ("Guindy", "2026-10-03", 121.0), ("Adyar", "2026-10-04", 60.0)]
con3 = sqlite3.connect(":memory:"); con3.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")
con3.executemany("INSERT INTO aq VALUES (?,?,?)", readings); con3.commit()
def station_average(name):
    return con3.execute("SELECT AVG(pm25) FROM aq WHERE station = ?", (name,)).fetchone()[0]
print(station_average("Adyar"), station_average("Guindy")); print(station_average("Adyar' OR '1'='1")); con3.close()
rows = [(f"S{i%12}", "2026-10-01", i % 24, float(i % 100)) for i in range(200000)]
c = sqlite3.connect(":memory:"); c.execute("CREATE TABLE t (a,b,c,d)")
s = time.perf_counter(); c.executemany("INSERT INTO t VALUES (?,?,?,?)", rows); c.commit(); t1 = time.perf_counter() - s
c.execute("DELETE FROM t")
s = time.perf_counter()
for r in rows: c.execute("INSERT INTO t VALUES (?,?,?,?)", r)
c.commit(); t2 = time.perf_counter() - s
print(f"200,000 inserts: executemany {t1:.3f}s | execute in loop {t2:.3f}s")

# sentiment
POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}
def score(text, pos=POSITIVE, neg=NEGATIVE):
    words = text.lower().replace(".", " ").replace(",", " ").replace("!", " ").split()
    total = 0
    for i, w in enumerate(words):
        v = 1 if w in pos else -1 if w in neg else 0
        if v and i > 0 and words[i - 1] in NEGATORS: v = -v
        total += v
    return total
def label(text):
    s = score(text); return "positive" if s > 0 else "negative" if s < 0 else "neutral"
print("\n--- B2 sentiment adversarial ---")
for s_ in ["Oh great, another day of thick smoke. Wonderful service!", "I can't say it was not bad.", "The roads are clean but the air is terrible and the staff are rude.",
           "Air is good but traffic smoke is bad.", "The air quality is not very good", "Never seen it this clean, but the bus is slow", "Awful! the air is horrible"]:
    print(f"score={score(s_):+d} {label(s_):8} | {s_}")

