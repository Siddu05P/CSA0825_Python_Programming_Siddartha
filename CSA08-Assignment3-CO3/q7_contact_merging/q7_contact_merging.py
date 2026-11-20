import random, time, sys, copy, re
from collections import deque, Counter

def tm(f, *a):
    s = time.perf_counter(); r = f(*a); return r, time.perf_counter() - s


print("\n=== Q7 Contacts ===")
def norm_num(n):
    d = "".join(c for c in n if c.isdigit())
    return d[-10:] if len(d) >= 10 else d
def norm_name(s):
    s = s.lower().replace(".", " ")
    return " ".join(w for w in s.split() if w not in {"dr", "mr", "mrs", "ms"})
def merge(contacts):
    people = {}; no_num = []
    for c in contacts:
        nums = {norm_num(n) for n in c.get("phones", []) if norm_num(n)}
        if not nums: no_num.append(c); continue
        key = next((k for k in nums if k in people), None)
        if key is None: key = min(nums); people[key] = {"names": set(), "phones": set(), "emails": set()}
        rec = people[key]
        for n in nums: people[n] = rec if n not in people else people[n]
        rec["names"].add(norm_name(c["name"])); rec["phones"] |= nums; rec["emails"] |= {e.lower() for e in c.get("emails", [])}
    uniq = {id(v): v for v in people.values()}
    return list(uniq.values()), no_num
sample = [{"name": "Dr. Ravi", "phones": ["+91 98400 12345"], "emails": ["Ravi@x.com"]},
          {"name": "ravi kumar", "phones": ["9840012345", "044-2345678"], "emails": []},
          {"name": "Priya", "phones": ["98765 43210"]}, {"name": "Priya", "phones": ["99999 11111"]}, {"name": "NoPhone", "emails": ["a@b.c"]}]
m, nn = merge(sample)
for r in m: print(sorted(r["names"]), sorted(r["phones"]), sorted(r["emails"]))
print("no phone:", [c["name"] for c in nn])
def gen_c(n): return [{"name": f"P{i%(n//2)}", "phones": [f"+91 {9000000000 + (i % (n//2))}"], "emails": [f"p{i}@x.com"]} for i in range(n)]
def merge_pairs(contacts):
    groups = []
    for c in contacts:
        nums = {norm_num(n) for n in c["phones"]}
        for g in groups:
            if g["phones"] & nums: g["phones"] |= nums; g["emails"] |= set(c["emails"]); break
        else: groups.append({"phones": set(nums), "emails": set(c["emails"])})
    return groups
for n in (1000, 100000):
    C = gen_c(n); (r1, _), t1 = tm(merge, C)
    if n <= 10000: r2, t2 = tm(merge_pairs, C); print(f"n={n:6d} dict={t1:.4f}s pairwise={t2:.4f}s groups {len(r1)} vs {len(r2)}")
    else: print(f"n={n:6d} dict={t1:.4f}s pairwise skipped (O(n^2) = {n*n//2:,} comparisons) groups={len(r1)}")
C = gen_c(10000); _, t2 = tm(merge_pairs, C); print("pairwise n=10000:", f"{t2:.3f}s")
