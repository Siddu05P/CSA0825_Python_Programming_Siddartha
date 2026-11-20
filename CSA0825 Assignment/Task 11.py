import json, time, sys
from decimal import Decimal as D, ROUND_HALF_UP

def load_rates(path="rates.json"):
    with open(path) as fh:
        return {k: D(str(v)) for k, v in json.load(fh).items()}

def payout(r, litres, fat, snf):
    fs = ((D(str(fat)) - r["std_fat"]) / D("0.1")).to_integral_value()
    ss = ((D(str(snf)) - r["std_snf"]) / D("0.1")).to_integral_value()
    rate = r["base"] + fs * r["fat_step"] + ss * r["snf_step"]
    return (D(str(litres)) * rate).quantize(D("0.01"), ROUND_HALF_UP)

t = time.perf_counter(); rates = load_rates(); t_load = time.perf_counter() - t
print({k: str(v) for k, v in rates.items()}, f"{t_load * 1e6:.0f} microseconds")
print(payout(rates, 8.5, 4.2, 8.7), payout(rates, 12, 3.1, 8.3), sys.getsizeof(rates), "bytes")
t = time.perf_counter()
tot = sum(payout(rates, 10 + i % 7, 3.5 + (i % 10) / 10, 8.5) for i in range(150000))
print(f"150000 payouts: total {tot} in {time.perf_counter() - t:.2f}s")