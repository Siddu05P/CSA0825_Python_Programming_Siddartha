import os, csv, tempfile, time, shutil, random
from pathlib import Path
from decimal import Decimal, InvalidOperation

WORK = Path(tempfile.mkdtemp())


# ---------------- TASK 2 ----------------
print("\n=== TASK 2: attendance monthly processing ===")
adir = WORK / "attendance"; adir.mkdir()
(adir / "2026-10-01.txt").write_text("192311001,2026-10-01,P\n192311002,2026-10-01,A\n192311003,2026-10-01,P\n")
(adir / "2026-10-02.txt").write_text("192311001,2026-10-02,P\n192311002,2026-10-02,A\n192311003,2026-10-02\n")
(adir / "2026-10-03.txt").write_text("192311001,2026-10-03,A\n192311002,2026-10-03,P\n192311003,2026-10-03,X\n")
def process_month(folder, report_path, errlog_path):
    present, total, errors = {}, {}, []
    for p in sorted(Path(folder).glob("*.txt")):
        with open(p, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                parts = line.strip().split(",")
                if len(parts) != 3 or parts[2] not in ("P", "A"):
                    errors.append(f"{p.name}:{n}:{line.strip()}"); continue
                r, d, s = parts
                total[r] = total.get(r, 0) + 1
                present[r] = present.get(r, 0) + (s == "P")
    pct = {r: round(100 * present[r] / total[r], 1) for r in total}
    with open(report_path, "w", encoding="utf-8") as f:
        for r in sorted(pct): f.write(f"{r},{pct[r]}\n")
    with open(errlog_path, "w", encoding="utf-8") as f: f.write("\n".join(errors))
    return pct, [r for r in pct if pct[r] < 75], errors
pct, low, errs = process_month(adir, WORK / "rep.csv", WORK / "err.log")
print("percent:", pct); print("below 75%:", low); print("damaged:", errs)

