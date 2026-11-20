import time
BASE_RATE, FAT_STEP_VALUE, SNF_STEP_VALUE = 30.0, 0.40, 0.30
def rate_per_litre(fat, snf):
    """Return price per litre for the given fat % and SNF %."""
    return round(BASE_RATE + round((fat - 3.5) / 0.1) * FAT_STEP_VALUE
                 + round((snf - 8.5) / 0.1) * SNF_STEP_VALUE, 2)
def payout(litres, fat, snf):
    """Return payment amount (Rs) for one collection entry."""
    return round(litres * rate_per_litre(fat, snf), 2)
def ten_day_total(entries):
    """Return total payment for a farmer; entries = [(litres, fat, snf), ...]."""
    total = 0.0
    for e in entries:
        total += payout(*e)
    return round(total, 2)
def scope_demo():
    BASE_RATE = 0
    return BASE_RATE
entries = [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]
print(rate_per_litre(4.2, 8.7), payout(8.5, 4.2, 8.7), ten_day_total(entries))
print("printing ->", end=" "); print(payout(10, 3.5, 8.5))
print("returned ->", payout(10, 3.5, 8.5) * 2)
print(scope_demo(), BASE_RATE, rate_per_litre.__doc__)
pay_lambda = lambda l, f, s: round(l * rate_per_litre(f, s), 2)
data = [(10, 3.5, 8.5)] * 200_000
t = time.perf_counter(); [payout(*d) for d in data]; t1 = time.perf_counter() - t
t = time.perf_counter()
for l, f, s in data:
    round(l * round(30.0 + round((f - 3.5) / 0.1) * 0.40 + round((s - 8.5) / 0.1) * 0.30, 2), 2)
t2 = time.perf_counter() - t
print(f"functions {t1:.3f}s | inlined {t2:.3f}s | lambda:", pay_lambda(10, 3.5, 8.5))