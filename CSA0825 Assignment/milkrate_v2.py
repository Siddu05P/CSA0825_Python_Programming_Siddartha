"""Revised rate module: season-aware rate card, 2-decimal analyser readings, bonus."""
from decimal import Decimal as D, ROUND_HALF_UP
CENT, STD_FAT, STD_SNF, STEP = D("0.01"), D("3.5"), D("8.5"), D("0.1")
BONUS_LITRES, BONUS_RATE = D("500"), D("0.50")
RATE_CARDS = {
    "normal":   {"base": D("30.00"), "fat_step": D("0.40"), "snf_step": D("0.30")},
    "seasonal": {"base": D("32.00"), "fat_step": D("0.45"), "snf_step": D("0.30")},
}
def season_for_month(month):
    """Return 'seasonal' for April-June, else 'normal'."""
    return "seasonal" if month in (4, 5, 6) else "normal"
def validate(litres, fat, snf):
    """Raise ValueError if a reading is invalid; return Decimals."""
    litres, fat, snf = D(str(litres)), D(str(fat)), D(str(snf))
    if litres < 0:
        raise ValueError("negative litres")
    if not D("2.0") <= fat <= D("7.0"):
        raise ValueError("fat out of range")
    if not D("6.0") <= snf <= D("10.0"):
        raise ValueError("SNF out of range")
    return litres, fat, snf
def rate_per_litre(fat, snf, season="normal"):
    """Exact (unrounded) rate per litre; steps are proportional, not rounded."""
    c = RATE_CARDS[season]
    return (c["base"] + (D(str(fat)) - STD_FAT) / STEP * c["fat_step"]
            + (D(str(snf)) - STD_SNF) / STEP * c["snf_step"])
def payout(litres, fat, snf, season="normal"):
    """Payment for one entry, rounded to paise (ROUND_HALF_UP)."""
    litres, fat, snf = validate(litres, fat, snf)
    return (litres * rate_per_litre(fat, snf, season)).quantize(CENT, ROUND_HALF_UP)
def bonus(total_litres):
    """Bonus of Rs 0.50/litre on all litres if ten-day supply exceeds 500 L."""
    total_litres = D(str(total_litres))
    if total_litres > BONUS_LITRES:
        return (total_litres * BONUS_RATE).quantize(CENT, ROUND_HALF_UP)
    return D("0.00")
def ten_day_total(entries, season="normal"):
    """entries = [(litres, fat, snf), ...] -> (payments, bonus, grand total)."""
    pay = sum((payout(l, f, s, season) for l, f, s in entries), D("0.00"))
    b = bonus(sum(D(str(l)) for l, _, _ in entries))
    return pay, b, pay + b