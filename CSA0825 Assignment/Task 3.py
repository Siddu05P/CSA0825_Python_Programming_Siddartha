import timeit

BASE_RATE, FAT_STEP_VALUE, SNF_STEP_VALUE = 30.00, 0.40, 0.30
STD_FAT, STD_SNF, STEP_SIZE = 3.5, 8.5, 0.1
MIN_FAT, MAX_FAT, MIN_SNF, MAX_SNF = 2.0, 7.0, 6.0, 10.0
MIN_LITRES, DAYS_PER_PERIOD = 0.0, 10
print(BASE_RATE, FAT_STEP_VALUE, SNF_STEP_VALUE, MIN_FAT, MAX_FAT, MIN_SNF, MAX_SNF)

x = 10
print(x, type(x).__name__)
x = "ten"
print(x, type(x).__name__)

a, b = 4.2, 3.1
a, b = b, a
c = d = 0
print(a, b, c, d)

BASE_RATE = 99
print("BASE_RATE silently changed to", BASE_RATE)

RATE_CARD = {"base": 30.0, "fat": 0.40, "snf": 0.30}
rate_magic = lambda fs, ss: 30.0 + fs * 0.40 + ss * 0.30
rate_dict = lambda fs, ss: RATE_CARD["base"] + fs * RATE_CARD["fat"] + ss * RATE_CARD["snf"]
print(rate_magic(7, 2), rate_dict(7, 2))
for f in (rate_magic, rate_dict):
    print(round(timeit.timeit(lambda: f(7, 2), number=1_000_000), 3), "s")