import milkrate
from milkrate import payout
import milkrate as mr
import sys
print("payout(20, 4.0, 8.8) =", payout(20, 4.0, 8.8))
print("milkrate.rate_per_litre =", milkrate.rate_per_litre(4.0, 8.8))
print("mr.BASE_RATE =", mr.BASE_RATE)
print("'milkrate' in sys.modules :", "milkrate" in sys.modules)
