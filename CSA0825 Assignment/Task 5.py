def to_float(t):
    try:
        return float(t)
    except ValueError:
        return None

def to_float_str(t):
    s = t.strip()
    return float(s) if s.replace(".", "", 1).isdigit() else None

print(type("42"), int("42") + 1, float("8.5") + 1)
for e in ("8.5", " 8.5 ", "8,5", "eight", "-3", "1e2"):
    print(f"{e!r:>10} | {to_float(e)!s:>10} | {to_float_str(e)!s:>10}")

for p, t in (("litres", "12.5"), ("fat", "8,5"), ("snf", "eight")):
    v = to_float(t)
    if v is None:
        print(f"Invalid entry for {p}: {t!r} -> please re-enter")
    print("->", v)

amount = 283.9
print(f"|{amount:8.2f}|{amount:<10.1f}|{amount:>12,.2f}|{'ID007':>8}|")