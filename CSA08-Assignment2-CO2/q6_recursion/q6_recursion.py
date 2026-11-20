import time, sys
from functools import lru_cache


print("\n=== Q6 Recursion ===")
calls = 0
def ways_naive(n):
    global calls
    calls += 1
    if n <= 1: return 1
    return ways_naive(n-1) + ways_naive(n-2)
@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1
    if n <= 1: return 1
    return ways_memo(n-1) + ways_memo(n-2)
def ways_loop(n):
    a, b = 1, 1
    for _ in range(n - 1): a, b = b, a + b
    return b if n >= 1 else 1
print([ways_naive(n) for n in range(1, 7)])
for n in (10, 20, 25, 30):
    ways_memo.cache_clear()
    calls = 0; ways_naive(n); cn = calls
    calls = 0; ways_memo(n); cm = calls
    print(f"n={n}: naive calls={cn}  memo calls={cm}")
ways_memo.cache_clear()
calls = 0; print("naive:", ways_naive(25), "calls =", calls)
ways_memo.cache_clear()
calls = 0; print("memo :", ways_memo(25), "calls =", calls)
print("limit", sys.getrecursionlimit())
ways_memo.cache_clear()
try: ways_memo(1000); print("memo(1000) fine")
except RecursionError as e: print("RecursionError:", e)
sys.setrecursionlimit(5000); ways_memo.cache_clear()
v = ways_memo(1000); print("after raising limit, digits:", len(str(v)))
print("loop equals memo:", ways_loop(1000) == v)
for name, fn in (("memo", lambda: (ways_memo.cache_clear(), ways_memo(1000))), ("loop", lambda: ways_loop(1000))):
    s = time.perf_counter(); [fn() for _ in range(200)]; print(name, f"{(time.perf_counter()-s)/200*1e6:.1f} us per run")

