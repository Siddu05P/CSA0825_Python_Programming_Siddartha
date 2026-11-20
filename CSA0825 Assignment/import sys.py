import sys
import milkrate
import milkrate as mr
from milkrate import payout

print(payout(20, 4.0, 8.8), milkrate.rate_per_litre(4.0, 8.8), mr.BASE_RATE)
print("milkrate" in sys.modules)