import time, sys
from functools import lru_cache


print("\n=== Q4 String building ===")
def build_plus(parts):
    text = ""
    for p in parts: text += p + ";"
    return text
def build_join(parts): return ";".join(parts) + ";"
def build_fstring_plus(n):
    t = ""
    for i in range(n): t += f"Item{i}:Rs{i%50};"
    return t
def build_fstring_join(n):
    return "".join([f"Item{i}:Rs{i%50};" for i in range(n)])
def tm(f, *a):
    s = time.perf_counter(); r = f(*a); return r, time.perf_counter() - s
for n in (1000, 10000, 200000):
    items = [f"Item{i}:Rs{i%50}" for i in range(n)]
    a, tp = tm(build_plus, items); b, tj = tm(build_join, items); c, tf = tm(build_fstring_join, n)
    print(f"n={n:7d} +=:{tp:.4f}s join:{tj:.4f}s fstring-join:{tf:.4f}s same={a==b==c} len={len(b)}")
items = [f"Item{i}:Rs{i % 50}" for i in range(200_000)]
tp_l, tj_l = [], []
for _ in range(3):
    a, tp = tm(build_plus, items); b, tj = tm(build_join, items); tp_l.append(tp); tj_l.append(tj)
print("same text:", a == b, "| length:", len(b))
print(f"avg += {sum(tp_l)/3:.4f}s  avg join {sum(tj_l)/3:.4f}s  runs+={['%.4f'%x for x in tp_l]} join={['%.4f'%x for x in tj_l]}")

