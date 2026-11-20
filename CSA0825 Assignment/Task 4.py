import math

for fat, std in ((4.2, 3.5), (8.7, 8.5), (3.1, 3.5)):
    print(f"({fat} - {std}) / 0.1 =", (fat - std) / 0.1)
print((4.2 - 3.5) / 0.1 == 7)
print(-2 ** 2, (-2) ** 2, 2 ** 3 ** 2, 10 - 4 - 3, 30 + 7 * 0.4 + 2 * 0.3)

print(f"{'value':>8} {'round':>6} {'int':>5} {'floor':>6}")
for v in (7.000000000000001, 6.999999999999999, -4.000000000000001, -3.9999999999999996, -2.5, 2.5):
    print(f"{v:>8.3f} {round(v):>6} {int(v):>5} {math.floor(v):>6}")
print(round(2.5), round(3.5))

for fat in (4.2, 3.1):
    raw = (fat - 3.5) / 0.1
    for name, s in (("round", round(raw)), ("int", int(raw)), ("floor", math.floor(raw))):
        print(f"fat {fat} {name:5} steps={s:3} rate=Rs {30 + s * 0.40:.2f}")

fat = 4.2
print(2.0 <= fat <= 7.0, fat >= 2.0 and fat <= 7.0, not (2.0 <= 7.5 <= 7.0))

litres, snf = 8.5, 8.7
fs, ss = round((fat - 3.5) / 0.1), round((snf - 8.5) / 0.1)
rate = 30.0 + fs * 0.40 + ss * 0.30
print(fs, ss, round(rate, 2), round(litres * rate, 2))