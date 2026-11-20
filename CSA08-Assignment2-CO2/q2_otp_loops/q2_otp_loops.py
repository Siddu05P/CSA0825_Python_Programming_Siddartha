import time, sys
from functools import lru_cache


print("\n=== Q2 OTP ===")
def otp_while(inputs, correct="1234", extra=False, sec_ok=False):
    attempts, limit, it = 0, 3, iter(inputs)
    if extra and sec_ok: limit = 5
    while attempts < limit:
        try: e = next(it)
        except StopIteration: break
        if e == "":
            continue                # blank entry: not counted
        attempts += 1               # counter updated AFTER the blank check
        if e == correct:
            return "OK after %d" % attempts
    else:
        return "LOCKED 30 min"
    return "no more input"
def otp_for(inputs, correct="1234"):
    it = iter(inputs)
    for attempt in range(3):
        e = next(it, None)
        while e == "":              # blank: re-ask without consuming an attempt
            e = next(it, None)
        if e == correct: return "OK on attempt %d" % (attempt+1)
        else: pass
    else:
        return "LOCKED 30 min"
print(otp_while(["", "1", "", "2", "1234"]))
print(otp_while(["1","2","3"]))
print(otp_while(["1","2","3","4","1234"], extra=True, sec_ok=True))
print(otp_for(["", "1", "2", "1234"]))
print(otp_for(["1", "2", "3"]))
def otp_rec(inputs, i=0, tries=0, limit=3, correct="1234"):
    if tries == limit: return "LOCKED"
    if i >= len(inputs): return "no input"
    if inputs[i] == "": return otp_rec(inputs, i+1, tries, limit, correct)
    if inputs[i] == correct: return "OK"
    return otp_rec(inputs, i+1, tries+1, limit, correct)
print(otp_rec(["1","2","1234"]), otp_rec(["1","2","3"]))

