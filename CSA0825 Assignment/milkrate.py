"""Rate card of the village milk co-operative."""
BASE_RATE, FAT_STEP_VALUE, SNF_STEP_VALUE = 30.00, 0.40, 0.30
STD_FAT, STD_SNF, STEP = 3.5, 8.5, 0.1


def rate_per_litre(fat, snf):
    """Return the price per litre, rounded to two decimals."""
    return round(BASE_RATE + round((fat - STD_FAT) / STEP) * FAT_STEP_VALUE
                 + round((snf - STD_SNF) / STEP) * SNF_STEP_VALUE, 2)


def payout(litres, fat, snf):
    """Return the payment amount rounded to two decimals."""
    return round(litres * rate_per_litre(fat, snf), 2)


if __name__ == "__main__":
    for l, f, s in [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]:
        print(f"{l:5} L fat {f} snf {s} rate {rate_per_litre(f, s):6.2f} pay {payout(l, f, s):8.2f}")