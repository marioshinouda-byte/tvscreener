"""
Forex Scanner — 28 liquid pairs, D1 + H4 + H1 alignment
========================================================

Τι κάνει:
- Σκανάρει μόνο 28 γνωστά/ρευστά Forex pairs.
- Παίρνει TradingView Technical Rating για D1, H4 και H1.
- Επιλέγει μία καθαρή εγγραφή ανά pair (χωρίς .P / synthetic duplicates).
- A+ = Strong Buy και στα 3 TF ή Strong Sell και στα 3 TF.
- WATCH = Buy και στα 3 TF ή Sell και στα 3 TF.
- Δημιουργεί το αρχείο LATEST_FOREX_SCAN.md για εύκολη προβολή στο GitHub.

Επόμενο στάδιο:
Break -> Retest -> Confirmation + H1 zones + EMA50.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

from tvscreener import ForexField, ForexScreener


PAIRS = [
    "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "USDCAD", "AUDUSD", "NZDUSD",
    "EURGBP", "EURJPY", "EURCHF", "EURCAD", "EURAUD", "EURNZD",
    "GBPJPY", "GBPCHF", "GBPCAD", "GBPAUD", "GBPNZD",
    "AUDJPY", "AUDCHF", "AUDCAD", "AUDNZD",
    "NZDJPY", "NZDCHF", "NZDCAD",
    "CADJPY", "CADCHF", "CHFJPY",
]

PROVIDER_PRIORITY = [
    "OANDA", "FOREXCOM", "FX_IDC", "SAXO", "FXCM",
    "PEPPERSTONE", "BLACKBULL", "CAPITALCOM",
]

STRONG_LEVEL = 0.5
DIRECTION_LEVEL = 0.1


@dataclass
class PairScan:
    pair: str
    symbol: str
    provider: str
    d1: Optional[float]
    h4: Optional[float]
    h1: Optional[float]
    direction: str
    grade: str
    score: float


def rating_text(value: Optional[float]) -> str:
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


def provider_rank(symbol: str) -> int:
    provider = symbol.split(":", 1)[0] if ":" in symbol else ""
    try:
        return PROVIDER_PRIORITY.index(provider)
    except ValueError:
        return len(PROVIDER_PRIORITY)


def exact_pair_from_symbol(symbol: str) -> str:
    """
    Επιστρέφει μόνο καθαρό 6-letter symbol.
    Π.χ. OANDA:EURUSD -> EURUSD
    BLACKBULL:EURUSD.P -> "" (απορρίπτεται)
    """
    raw = symbol.split(":", 1)[-1].upper()
    if len(raw) == 6 and raw.isalpha():
        return raw
    return ""


def fetch_pair(pair: str):
    """Ψάχνει ένα pair ώστε να μη βασιζόμαστε στα πρώτα N αλφαβητικά αποτελέσματα."""
    screener = ForexScreener()
    screener.select(
        ForexField.NAME,
        ForexField.TECHNICAL_RATING,   # D1
        ForexField.RECOMMEND_ALL_240,  # H4
        ForexField.RECOMMEND_ALL_60,   # H1
    )
    screener.search(pair)
    screener.set_range(0, 50)
    data = screener.get()

    if data.empty:
        return None

    exact_rows = []
    for _, row in data.iterrows():
        symbol = str(row.get("Symbol", ""))
        if exact_pair_from_symbol(symbol) == pair:
            exact_rows.append(row)

    if not exact_rows:
        return None

    exact_rows.sort(key=lambda row: provider_rank(str(row.get("Symbol", ""))))
    return exact_rows[0]


def classify(d1: Optional[float], h4: Optional[float], h1: Optional[float]):
    if d1 is None or h4 is None or h1 is None:
        return "—", "—", 0.0

    if d1 > STRONG_LEVEL and h4 > STRONG_LEVEL and h1 > STRONG_LEVEL:
        direction, grade = "LONG", "A+"
    elif d1 < -STRONG_LEVEL and h4 < -STRONG_LEVEL and h1 < -STRONG_LEVEL:
        direction, grade = "SHORT", "A+"
    elif d1 > DIRECTION_LEVEL and h4 > DIRECTION_LEVEL and h1 > DIRECTION_LEVEL:
        direction, grade = "LONG", "WATCH"
    elif d1 < -DIRECTION_LEVEL and h4 < -DIRECTION_LEVEL and h1 < -DIRECTION_LEVEL:
        direction, grade = "SHORT", "WATCH"
    else:
        direction, grade = "—", "—"

    score = round((abs(d1) + abs(h4) + abs(h1)) / 3 * 100, 1)
    return direction, grade, score


def scan_pair(pair: str) -> PairScan:
    try:
        row = fetch_pair(pair)
        if row is None:
            return PairScan(pair, "", "", None, None, None, "—", "—", 0.0)

        symbol = str(row.get("Symbol", ""))
        provider = symbol.split(":", 1)[0] if ":" in symbol else ""

        try:
            d1 = float(row["Technical Rating"])
            h4 = float(row["Recommend All|240"])
            h1 = float(row["Recommend All|60"])
        except (TypeError, ValueError, KeyError):
            d1 = h4 = h1 = None

        direction, grade, score = classify(d1, h4, h1)
        return PairScan(pair, symbol, provider, d1, h4, h1, direction, grade, score)

    except Exception as exc:
        print(f"[WARN] {pair}: {exc}")
        return PairScan(pair, "", "", None, None, None, "—", "—", 0.0)


def scan_all_pairs() -> list[PairScan]:
    results = []
    for index, pair in enumerate(PAIRS, start=1):
        print(f"[{index:02d}/{len(PAIRS)}] Scan {pair}...")
        results.append(scan_pair(pair))
        time.sleep(0.15)
    return results


def aligned_results(results: list[PairScan]) -> list[PairScan]:
    aligned = [r for r in results if r.grade in {"A+", "WATCH"}]
    aligned.sort(key=lambda r: (r.grade != "A+", -r.score, r.pair))
    return aligned


def write_markdown(results: list[PairScan], path: str = "LATEST_FOREX_SCAN.md") -> None:
    now = datetime.now(ZoneInfo("Europe/Athens"))
    aligned = aligned_results(results)
    a_plus = [r for r in aligned if r.grade == "A+"]

    lines = [
        "# Latest Forex Scan",
        "",
        f"**Τελευταία ενημέρωση:** {now:%d/%m/%Y %H:%M} (Europe/Athens)",
        "",
        f"**Pairs που ελέγχθηκαν:** {len(results)}  |  **Aligned:** {len(aligned)}  |  **A+:** {len(a_plus)}",
        "",
        "> Alignment δεν σημαίνει entry. Για είσοδο περιμένουμε Break → Retest → Confirmation.",
        "",
        "## Top aligned setups",
        "",
    ]

    if aligned:
        lines += [
            "| # | Pair | Direction | Grade | D1 | H4 | H1 | Score | Provider |",
            "|---:|---|---|---|---|---|---|---:|---|",
        ]
        for i, r in enumerate(aligned, start=1):
            lines.append(
                f"| {i} | **{r.pair}** | {r.direction} | **{r.grade}** | "
                f"{rating_text(r.d1)} | {rating_text(r.h4)} | {rating_text(r.h1)} | "
                f"{r.score:.1f}% | {r.provider or 'N/A'} |"
            )
    else:
        lines.append("Δεν βρέθηκε αυτή τη στιγμή κοινή κατεύθυνση D1 + H4 + H1.")

    lines += [
        "",
        "## Όλα τα 28 pairs",
        "",
        "| Pair | D1 | H4 | H1 | Direction | Grade | Score |",
        "|---|---|---|---|---|---|---:|",
    ]
    for r in results:
        lines.append(
            f"| {r.pair} | {rating_text(r.d1)} | {rating_text(r.h4)} | "
            f"{rating_text(r.h1)} | {r.direction} | {r.grade} | {r.score:.1f}% |"
        )

    lines += [
        "",
        "## Επόμενο φίλτρο",
        "",
        "H1 zones → Break → Retest → Confirmation candle → EMA50 → τελικό A+ ranking.",
        "",
    ]

    Path(path).write_text("\n".join(lines), encoding="utf-8")


def print_results(results: list[PairScan]) -> None:
    aligned = aligned_results(results)

    print("\n" + "=" * 108)
    print("FOREX SCANNER — 28 PAIRS — D1 + H4 + H1")
    print("=" * 108)
    print(
        f"{'#':<3} {'PAIR':<8} {'DIR':<7} {'GRADE':<7} "
        f"{'D1':<13} {'H4':<13} {'H1':<13} {'SCORE':>7}  PROVIDER"
    )
    print("-" * 108)

    if not aligned:
        print("Δεν βρέθηκε aligned setup.")
    else:
        for i, r in enumerate(aligned, start=1):
            print(
                f"{i:<3} {r.pair:<8} {r.direction:<7} {r.grade:<7} "
                f"{rating_text(r.d1):<13} {rating_text(r.h4):<13} "
                f"{rating_text(r.h1):<13} {r.score:>6.1f}%  {r.provider}"
            )

    a_plus = sum(1 for r in aligned if r.grade == "A+")
    print("-" * 108)
    print(f"Checked: {len(results)} | Aligned: {len(aligned)} | A+: {a_plus}")
    print("Alignment != entry. Entry μόνο μετά από Break -> Retest -> Confirmation.")


def main():
    print("Ξεκινά scanner 28 Forex pairs...")
    results = scan_all_pairs()
    print_results(results)
    write_markdown(results)
    print("\nΑποθηκεύτηκε: LATEST_FOREX_SCAN.md")


if __name__ == "__main__":
    main()
