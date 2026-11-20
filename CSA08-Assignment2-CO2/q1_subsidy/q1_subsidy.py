import time, sys
from functools import lru_cache


print("=== Q1 Subsidy ===")
def subsidy_separate_if(units, ration, senior):
    r = []
    if units <= 100: r.append("full")
    if 101 <= units <= 200 and ration: r.append("partial")
    if units > 200 and senior: r.append("senior")
    return r
def subsidy_elif(units, ration, senior):
    if units <= 100: return "full"
    elif 101 <= units <= 200:
        return "partial" if ration else "none"
    elif senior: return "senior"
    else: return "none"
# buggy version of the developer: overlapping conditions
def subsidy_buggy(units, ration, senior):
    r = []
    if units <= 100: r.append("full")
    if units <= 200 and ration: r.append("partial")   # overlaps with first
    if units > 200 and senior or units > 100 and senior: r.append("senior")  # overlaps
    return r
tests = [(50,0,0),(100,0,0),(100,1,0),(101,0,0),(101,1,0),(200,1,0),(201,0,0),(201,0,1),(250,1,1)]
print("units ration senior | buggy-separate-if | fixed-separate-if | if-elif")
for t in tests:
    print(t, subsidy_buggy(*t), subsidy_separate_if(*t), subsidy_elif(*t))

