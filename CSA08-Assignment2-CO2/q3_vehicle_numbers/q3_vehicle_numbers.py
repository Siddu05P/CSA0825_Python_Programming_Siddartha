import time, sys
from functools import lru_cache


print("\n=== Q3 Vehicle numbers ===")
def normalise(text):
    return text.replace(" ", "").replace("-", "").upper()
def is_valid(reg):
    if len(reg) not in (9, 10): return False
    state, dist, tail = reg[:2], reg[2:4], reg[-4:]
    series = reg[4:-4]
    return state.isalpha() and dist.isdigit() and series.isalpha() and tail.isdigit() and len(series) in (1, 2)
def fmt(reg):
    return " ".join([reg[:2], reg[2:4], reg[4:-4], reg[-4:]])
for raw in ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234", "TN 22 1234 AB"]:
    reg = normalise(raw)
    print(f"{raw:15} -> {reg:11} {'valid' if is_valid(reg) else 'INVALID'}")
for raw in ["Tn09Ab1234", "tn-09-ab-1234", "TN09ABC1234", "TN09AB123", "T109AB1234", "  tn 09 a 1 2 3 4 "]:
    r = normalise(raw.strip()); print(f"{raw!r:22} -> {r:12} {is_valid(r)}", fmt(r) if is_valid(r) else "")
s9, s10 = "KA01M0007", "TN09AB1234"
print(s9[-4:], repr(s9[4:-4]), s10[-4:], repr(s10[4:-4]))

