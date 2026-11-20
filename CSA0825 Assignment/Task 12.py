from decimal import Decimal as D
from milkrate_v2 import payout, rate_per_litre, bonus, ten_day_total, season_for_month

f, s = 4.27, 8.63
fs, ss = round((f - 3.5) / 0.1), round((s - 8.5) / 0.1)
old = round(30 + fs * 0.40 + ss * 0.30, 2)
print(f"Original: steps {fs}, {ss} -> rate {old:.2f} -> pay {old * 10:.2f}")
for season in ("normal", "seasonal"):
    print(f"{season}: rate {rate_per_litre(f, s, season):.4f} -> pay {payout(10, f, s, season)}")

total = lambda e, season: ten_day_total(e, season)[2]
e520 = [(260, 3.5, 8.5)] * 2
tests = [
    ("Original rate, 8.5 L 4.2/8.7", payout(8.5, 4.2, 8.7), D("283.90")),
    ("Original rate, 12 L 3.1/8.3", payout(12, 3.1, 8.3), D("333.60")),
    ("Standard milk, normal", payout(10, 3.5, 8.5), D("300.00")),
    ("Standard milk, seasonal", payout(10, 3.5, 8.5, "seasonal"), D("320.00")),
    ("Seasonal 8.5 L 4.2/8.7", payout(8.5, 4.2, 8.7, "seasonal"), D("303.88")),
    ("Two-decimal normal", payout(10, 4.27, 8.63), D("334.70")),
    ("Two-decimal seasonal", payout(10, 4.27, 8.63, "seasonal"), D("358.55")),
    ("Bonus: 500 L exactly", bonus(500), D("0.00")),
    ("Bonus: 520 L", bonus(520), D("260.00")),
    ("April maps to seasonal", season_for_month(4), "seasonal"),
    ("July maps to normal", season_for_month(7), "normal"),
    ("520 L normal total", total(e520, "normal"), D("15860.00")),
    ("520 L seasonal total", total(e520, "seasonal"), D("16900.00")),
    ("400 L seasonal, no bonus", total([(100, 3.5, 8.5)] * 4, "seasonal"), D("12800.00")),
]
for i, (name, act, exp) in enumerate(tests, 1):
    print(f"{i:<3}{name:<30}{exp!s:>10}{act!s:>10}  {'PASS' if act == exp else 'FAIL'}")
print("ALL PASSED" if all(a == e for _, a, e in tests) else "SOME FAILED")
try:
    payout(10, 7.5, 8.5)
except ValueError as e:
    print("Validation still works ->", e)