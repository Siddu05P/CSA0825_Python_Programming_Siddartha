import time, sys
from functools import lru_cache


calls = 0
def ways_naive(n):
    global calls
    calls += 1
    if n <= 1: return 1
    return ways_naive(n-1) + ways_naive(n-2)
def ways_loop(n):
    a, b = 1, 1
    for _ in range(n - 1): a, b = b, a + b
    return b if n >= 1 else 1

print("\n=== Q7 Redesign of Q6: naive -> loop ===")
for n in (20, 25, 30, 32):
    s = time.perf_counter(); calls = 0; ways_naive(n); t1 = time.perf_counter() - s
    s = time.perf_counter(); ways_loop(n); t2 = time.perf_counter() - s
    print(f"n={n} naive calls={calls} time={t1:.4f}s | loop additions={n-1} time={t2*1e6:.2f}us")
