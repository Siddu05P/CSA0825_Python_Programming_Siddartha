import os, csv, tempfile, time, shutil, random
from pathlib import Path
from decimal import Decimal, InvalidOperation

WORK = Path(tempfile.mkdtemp())


# ---------------- TASK 1 ----------------
print("=== TASK 1: repaired mess-bill script ===")
mess = WORK / "mess_oct.txt"
mess.write_text("192311001,Arun,1250.50\n192311002,Bala,1300\n192311003,Chitra,abc\n192311004,Deepa\n192311005,Eswar,-50\n192311006,Farid,1100.25\n\n", encoding="utf-8")

def original_script(path):
    f = open(path); data = f.read(); total = 0; report = ""
    for line in data.split("\n"):
        try:
            parts = line.split(","); total = total + int(parts[2]); report = report + parts[1] + " " + parts[2] + "\n"
        except: pass
    return report, total
print("ORIGINAL ->", original_script(mess))      # 1250.50 and 1100.25 silently dropped

def total_bills(filename):
    total, lines, rejected = Decimal("0"), [], []
    try:
        with open(filename, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                line = line.strip()
                if not line: continue
                parts = line.split(",")
                try:
                    if len(parts) != 3: raise ValueError("expected 3 fields")
                    amt = Decimal(parts[2])
                    if amt < 0: raise ValueError("negative amount")
                except InvalidOperation:
                    rejected.append((n, line, "amount is not a number")); continue
                except ValueError as e:
                    rejected.append((n, line, str(e))); continue
                total += amt; lines.append(f"{parts[1]} {amt}")
    except FileNotFoundError:
        rejected.append((0, filename, "file not found"))
    return total, "\n".join(lines), rejected
t, rep, rej = total_bills(mess)
print(rep); print("Total", t); print("Rejected:", rej)
print(total_bills(WORK / "nofile.txt"))

