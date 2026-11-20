import csv, io, sqlite3, time, random, statistics, cProfile, pstats, tracemalloc, os, sys
from collections import defaultdict, Counter
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("charts", exist_ok=True)
random.seed(7)

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
print("\n--- B4 Complete the Code output ---")
for c_ in ["Roads are clean and the bus was fast.", "Smoke from the factory, air is bad.", "The staff were not helpful.", "Not bad, service improved."]:
    print(f"{label(c_):8} | {c_}")
# =============== B4 complaints ===============
print("\n=== B4 Complaints: 50 complaints, my own labels ===")
COMPLAINTS = [
 ("The air near the factory is bad and full of smoke.", "negative"), ("Roads are clean and the bus service is fast.", "positive"),
 ("The staff were not helpful at the office.", "negative"), ("Not bad, the service improved this month.", "positive"),
 ("Garbage burning every night, the smoke is terrible.", "negative"), ("The new air monitor display is helpful.", "positive"),
 ("Dust everywhere and the response is slow.", "negative"), ("Thanks, the problem was fixed quickly.", "positive"),
 ("The officer was rude and did not listen.", "negative"), ("Air quality improved after the new rules.", "positive"),
 ("Traffic smoke is bad near the signal.", "negative"), ("I never saw the air this clean before.", "positive"),
 ("Complaint number was not registered.", "negative"), ("The app is slow and often broken.", "negative"),
 ("Good work by the cleaning team.", "positive"), ("There is a bad smell from the drain.", "negative"),
 ("Noise and smoke from the generator all day.", "negative"), ("The helpline is fast and helpful.", "positive"),
 ("Nobody came to check the dirty canal.", "negative"), ("Park is clean and trees improved the air.", "positive"),
 ("The reading shows 150 near my school.", "neutral"), ("I am asking about the PM2.5 level today.", "neutral"),
 ("The factory chimney is putting out black smoke.", "negative"), ("Not good, the air is bad in the morning.", "negative"),
 ("Bus service has improved and is not crowded.", "positive"), ("The sensor is broken near the market.", "negative"),
 ("Please share the report for last week.", "neutral"), ("Air is clean after the rain.", "positive"),
 ("Burning of waste near the school is very bad.", "negative"), ("The reply from the office was helpful.", "positive"),
 ("Slow response, rude staff and no action.", "negative"), ("Roads are dirty and broken.", "negative"),
 ("I cannot breathe, the smoke is unbearable.", "negative"), ("Nice work, the monitor is working again.", "positive"),
 ("The station is near the bus stand.", "neutral"), ("Great improvement in the air this week.", "positive"),
 ("Toxic fumes from the plant every evening.", "negative"), ("Not clean at all near the lake.", "negative"),
 ("Staff were polite and quick.", "positive"), ("When will the new station open?", "neutral"),
 ("The air is good today.", "positive"), ("Smoke from the crackers made it unbearable.", "negative"),
 ("It is not bad at all, very fast service.", "positive"), ("Wonderful service, thank you.", "positive"),
 ("Smell from the dump yard is horrible.", "negative"), ("The readings were not updated today.", "negative"),
 ("Dirty water and bad air near my house.", "negative"), ("The app shows data for all stations.", "neutral"),
 ("Clean air, helpful staff, fast reply.", "positive"), ("Poor service, nobody answers the phone.", "negative")]
EXT_POS = POSITIVE | {"great", "nice", "thanks", "wonderful", "polite", "quick", "quickly", "improvement", "good"}
EXT_NEG = NEGATIVE | {"terrible", "toxic", "horrible", "poor", "dust", "unbearable", "burning", "fumes", "smell", "noise", "garbage", "awful"}
def agree(pos, neg):
    ok, wrong = 0, []
    for t, gold in COMPLAINTS:
        s = score(t, pos, neg); p = "positive" if s > 0 else "negative" if s < 0 else "neutral"
        if p == gold: ok += 1
        else: wrong.append((p, gold, t))
    return ok, wrong
ok1, w1 = agree(POSITIVE, NEGATIVE); ok2, w2 = agree(EXT_POS, EXT_NEG)
print(f"basic lexicon agreement: {ok1}/50 = {ok1*2}%   extended lexicon: {ok2}/50 = {ok2*2}%")
print("sample wrong (extended):"); [print("  ", w) for w in w2[:6]]
print("gold counts:", Counter(g for _, g in COMPLAINTS))
STOPW = {"the", "a", "is", "are", "was", "were", "and", "of", "to", "in", "at", "near", "from", "for", "it", "i", "this", "that", "my", "not", "there", "an", "by", "on", "with"}
def summarise(texts, k=3):
    words = Counter(w for t in texts for w in t.lower().replace(".", " ").replace(",", " ").split() if w not in STOPW)
    sents = [t for t in texts]
    return sorted(sents, key=lambda s: -sum(words[w] for w in set(s.lower().replace(".", " ").replace(",", " ").split()) if w not in STOPW))[:k], words.most_common(5)
neg_texts = [t for t, g in COMPLAINTS if g == "negative"]
best, top = summarise(neg_texts); print("top words:", top); print("extractive summary:", best)
print("first-k summary   :", neg_texts[:3])
# index
big = sqlite3.connect(":memory:")
big.execute("CREATE TABLE readings (station TEXT, day TEXT, hour INTEGER, pm25 REAL)")
rnd = random.Random(2)
big.executemany("INSERT INTO readings VALUES (?,?,?,?)", ((f"S{rnd.randrange(112)}", f"2026-{rnd.randrange(1,13):02d}-{rnd.randrange(1,29):02d}", rnd.randrange(24), rnd.uniform(5, 200)) for _ in range(1_000_000)))
Q = "SELECT AVG(pm25) FROM readings WHERE station='S7' AND day='2026-10-05'"
def timeq():
    s = time.perf_counter()
    for _ in range(20): big.execute(Q).fetchone()
    return (time.perf_counter() - s) / 20
t_no = timeq(); big.execute("CREATE INDEX idx_sd ON readings(station, day)"); t_ix = timeq()
print("EXPLAIN before index: SCAN readings | after:", big.execute("EXPLAIN QUERY PLAN " + Q).fetchall()[0][-1])
print(f"1,000,000 rows, one-station-one-day query: no index {t_no*1e3:.2f} ms | with index {t_ix*1e3:.3f} ms | speed-up {t_no/t_ix:.0f}x")
# scorer timing
big_c = [t for t, _ in COMPLAINTS] * 1000
s = time.perf_counter(); [label(t) for t in big_c]; ts_ = time.perf_counter() - s
print(f"scorer: {len(big_c)} complaints in {ts_:.3f}s = {ts_/len(big_c)*1e6:.1f} us each -> 50,000 complaints in {ts_/len(big_c)*50000:.2f}s")
