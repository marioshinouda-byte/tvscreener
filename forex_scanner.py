"""
Forex Scanner — D1 + H4 + H1 alignment
=======================================

Πρώτο λειτουργικό στάδιο του project:
- Διαβάζει Forex δεδομένα από TradingView Screener μέσω tvscreener.
- Ελέγχει Technical Rating στα D1, H4 και H1.
- Κρατά μόνο ζευγάρια όπου και τα 3 timeframes συμφωνούν.
- A+ = Strong Buy και στα 3 TF ή Strong Sell και στα 3 TF.
- WATCH = Buy και στα 3 TF ή Sell και στα 3 TF.
- Ταξινομεί τα αποτελέσματα με βάση τη δύναμη του alignment.

Επόμενο στάδιο:
Break -> Retest -> Confirmation + zones + EMA50.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from tvscreener import ForexField, ForexScreener


# TradingView Technical Rating boundaries:
# Strong Buy:  0.5 < x <= 1.0
# Buy:         0.1 < x <= 0.5
# Neutral:    -0.1 <= x <= 0.1
# Sell:       -0.5 <= x < -0.1
# Strong Sell:-1.0 <= x < -0.5
STRONG_LEVEL = 0.5
DIRECTION_LEVEL = 0.1


@dataclass
class Setup:
    symbol: str
    name: str
    direction: str
    grade: str
    d1: float
    h4: float
    h1: float
    score: float


def rating_text(value: Optional[float]) -> str:
    """Μετατρέπει το numeric TradingView rating σε ευανάγνωστη ένδειξη."""
    if value is None:
        return "N/A"

    value = float(value)
    if value > 0.5:
        return "STRONG BUY"
    if value > 0.1:
        return "BUY"
    if value >= -0.1:
        return "NEUTRAL"
    if value >= -0.5:
        return "SELL"
    return "STRONG SELL"


def fetch_forex_market():
    """Ζητά μόνο τα πεδία που χρειαζόμαστε για D1/H4/H1 alignment."""
    screener = ForexScreener()
    screener.select(
        ForexField.NAME,
        ForexField.TECHNICAL_RATING,   # D1 = Recommend.All
        ForexField.RECOMMEND_ALL_240,  # H4
        ForexField.RECOMMEND_ALL_60,   # H1
    )
    # Μεγαλύτερο range ώστε να μην περιοριστούμε στα πρώτα 150 αποτελέσματα.
    screener.set_range(0, 500)
    return screener.get()


def build_setups(data) -> list[Setup]:
    """Βρίσκει τα ζευγάρια με κοινή κατεύθυνση στα D1/H4/H1."""
    setups: list[Setup] = []

    for _, row in data.iterrows():
        try:
            d1 = float(row["Technical Rating"])
            h4 = float(row["Recommend All|240"])
            h1 = float(row["Recommend All|60"])
        except (TypeError, ValueError, KeyError):
            continue

        # A+ LONG: Strong Buy και στα 3 timeframes.
        if d1 > STRONG_LEVEL and h4 > STRONG_LEVEL and h1 > STRONG_LEVEL:
            direction = "LONG"
            grade = "A+"

        # A+ SHORT: Strong Sell και στα 3 timeframes.
        elif d1 < -STRONG_LEVEL and h4 < -STRONG_LEVEL and h1 < -STRONG_LEVEL:
            direction = "SHORT"
            grade = "A+"

        # WATCH LONG: τουλάχιστον Buy και στα 3.
        elif d1 > DIRECTION_LEVEL and h4 > DIRECTION_LEVEL and h1 > DIRECTION_LEVEL:
            direction = "LONG"
            grade = "WATCH"

        # WATCH SHORT: τουλάχιστον Sell και στα 3.
        elif d1 < -DIRECTION_LEVEL and h4 < -DIRECTION_LEVEL and h1 < -DIRECTION_LEVEL:
            direction = "SHORT"
            grade = "WATCH"
        else:
            continue

        # 0–100: μέσος όρος απόλυτης ισχύος των 3 ratings.
        score = round((abs(d1) + abs(h4) + abs(h1)) / 3 * 100, 1)

        setups.append(
            Setup(
                symbol=str(row.get("Symbol", "")),
                name=str(row.get("Name", "")),
                direction=direction,
                grade=grade,
                d1=d1,
                h4=h4,
                h1=h1,
                score=score,
            )
        )

    # Πρώτα A+, μετά υψηλότερο score.
    setups.sort(key=lambda s: (s.grade != "A+", -s.score))
    return setups


def print_setups(setups: list[Setup], limit: int = 20) -> None:
    """Εμφανίζει καθαρό πίνακα αποτελεσμάτων."""
    print("\n" + "=" * 106)
    print("FOREX SCANNER — D1 + H4 + H1 ALIGNMENT")
    print("=" * 106)
    print(
        f"{'#':<3} {'PAIR':<18} {'DIR':<7} {'GRADE':<7} "
        f"{'D1':<13} {'H4':<13} {'H1':<13} {'SCORE':>7}"
    )
    print("-" * 106)

    if not setups:
        print("Δεν βρέθηκε αυτή τη στιγμή κοινό setup D1 + H4 + H1.")
        return

    for i, setup in enumerate(setups[:limit], start=1):
        print(
            f"{i:<3} {setup.symbol:<18} {setup.direction:<7} {setup.grade:<7} "
            f"{rating_text(setup.d1):<13} {rating_text(setup.h4):<13} "
            f"{rating_text(setup.h1):<13} {setup.score:>6.1f}%"
        )

    a_plus = sum(1 for s in setups if s.grade == "A+")
    print("-" * 106)
    print(f"Σύνολο aligned setups: {len(setups)} | A+: {a_plus}")
    print("\nΣημείωση: alignment ≠ είσοδος.")
    print("Για entry περιμένουμε ακόμη Break -> Retest -> Confirmation.")


def main():
    print("Κατεβάζω Forex δεδομένα...")
    data = fetch_forex_market()
    print(f"Ελήφθησαν {len(data)} Forex εγγραφές.")

    setups = build_setups(data)
    print_setups(setups)

    print("\nΕΠΟΜΕΝΟ ΒΗΜΑ:")
    print("- H1 zones")
    print("- Break")
    print("- Retest")
    print("- Confirmation candle")
    print("- EMA50 filter")
    print("- τελικό ranking A+ setups")


if __name__ == "__main__":
    main()
