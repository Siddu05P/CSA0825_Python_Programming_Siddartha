import random, time, timeit
from decimal import Decimal as D, ROUND_HALF_UP
from milkrate import rate_per_litre

CENT = D("0.01")

def make_data(n, dp):
    return [(round(random.uniform(5, 30), dp), round(random.uniform(3, 5), 1),
             round(random.uniform(8, 9), 1)) for _ in range(n)]

for dp in (1, 2):
    print(f"litres with {dp} decimal(s)")
    for n in (300, 6000, 150000):
        random.seed(n)
        data = make_data(n, dp)
        t = time.perf_counter()
        fl = 0.0
        for l, f, s in data:
            fl += l * rate_per_litre(f, s)
        t_f = time.perf_counter() - t
        t = time.perf_counter()
        exact = each = D(0)
        for l, f, s in data:
            amt = D(str(l)) * D(str(rate_per_litre(f, s)))
            exact += amt
            each += amt.quantize(CENT, ROUND_HALF_UP)
        t_d = time.perf_counter() - t
        once = exact.quantize(CENT, ROUND_HALF_UP)
        print(f"{n:>7} | float {fl:>14.2f} | each {each:>13} | once {once:>13} | diff {each - once:>6} | {t_f:.4f}s {t_d:.4f}s")

table = {}
def lookup(f, s):
    if (f, s) not in table:
        table[f, s] = rate_per_litre(f, s)
    return table[f, s]

t_re = timeit.timeit(lambda: [rate_per_litre(f, s) for _, f, s in data], number=1)
t_lk = timeit.timeit(lambda: [lookup(f, s) for _, f, s in data], number=1)
print(f"recalc {t_re:.4f}s | dict {t_lk:.4f}s | distinct pairs {len(table)}")