"""
Advanced Forex Scanner — 28 liquid pairs
==========================================

Method:
1) D1 + H4 + H1 TradingView technical alignment.
2) EMA50 direction + slope on all 3 timeframes.
3) ADX trend-strength check on H4/H1.
4) D1/H4 market-structure proxy from completed swing highs/lows.
5) H1 Break -> Retest -> Confirmation from completed candles.
6) Transparent quality score (NOT a probability of winning).

The scanner writes LATEST_FOREX_SCAN.md after each run.
"""

from __future__ import annotations

import math
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
ADX_MIN = 20.0

# We use completed candles only:
STRUCTURE_BARS = 7
BRC_BARS = 10


@dataclass(frozen=True)
class QueryField:
    """Minimal field object accepted by tvscreener.select()."""

    field_name: str
    label: str
    historical: bool = False

    def has_recommendation(self) -> bool:
        return False


@dataclass
class PairScan:
    pair: str
    symbol: str
    provider: str
    direction: str
    bias: str
    d1_rating: Optional[float]
    h4_rating: Optional[float]
    h1_rating: Optional[float]
    price: Optional[float]
    ema_passes: int
    ema_total: int
    adx_h4: Optional[float]
    adx_h1: Optional[float]
    d1_structure: str
    h4_structure: str
    brc_status: str
    zone: Optional[float]
    quality_score: float
    setup_grade: str


def q(field_name: str, label: str) -> QueryField:
    return QueryField(field_name=field_name, label=label)


def safe_float(value) -> Optional[float]:
    try:
        value = float(value)
        if math.isnan(value):
            return None
        return value
    except (TypeError, ValueError):
        return None


def rating_text(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
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
    raw = symbol.split(":", 1)[-1].upper()
    if len(raw) == 6 and raw.isalpha():
        return raw
    return ""


def build_query_fields():
    fields = [
        ForexField.NAME,
        ForexField.TECHNICAL_RATING,   # D1
        ForexField.RECOMMEND_ALL_240,  # H4
        ForexField.RECOMMEND_ALL_60,   # H1
        ForexField.PRICE,
        q("EMA50", "EMA50 D1"),
        q("EMA50[1]", "EMA50 D1 Prev"),
        q("EMA50|240", "EMA50 H4"),
        q("EMA50[1]|240", "EMA50 H4 Prev"),
        q("EMA50|60", "EMA50 H1"),
        q("EMA50[1]|60", "EMA50 H1 Prev"),
        q("ADX|240", "ADX H4"),
        q("ADX|60", "ADX H1"),
        q("ATR|60", "ATR H1"),
    ]

    # D1/H4 completed highs & lows for structure detection.
    for i in range(1, STRUCTURE_BARS + 1):
        fields += [
            q(f"high[{i}]", f"D1 High {i}"),
            q(f"low[{i}]", f"D1 Low {i}"),
            q(f"high[{i}]|240", f"H4 High {i}"),
            q(f"low[{i}]|240", f"H4 Low {i}"),
        ]

    # H1 completed OHLC candles for Break -> Retest -> Confirmation.
    for i in range(1, BRC_BARS + 1):
        fields += [
            q(f"open[{i}]|60", f"H1 Open {i}"),
            q(f"high[{i}]|60", f"H1 High {i}"),
            q(f"low[{i}]|60", f"H1 Low {i}"),
            q(f"close[{i}]|60", f"H1 Close {i}"),
        ]

    return fields


QUERY_FIELDS = build_query_fields()


def fetch_pair(pair: str):
    screener = ForexScreener()
    screener.select(*QUERY_FIELDS)
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


def classify_alignment(d1, h4, h1):
    if None in (d1, h4, h1):
        return "—", "NO DATA"

    if d1 > STRONG_LEVEL and h4 > STRONG_LEVEL and h1 > STRONG_LEVEL:
        return "LONG", "STRONG"
    if d1 < -STRONG_LEVEL and h4 < -STRONG_LEVEL and h1 < -STRONG_LEVEL:
        return "SHORT", "STRONG"
    if d1 > DIRECTION_LEVEL and h4 > DIRECTION_LEVEL and h1 > DIRECTION_LEVEL:
        return "LONG", "ALIGNED"
    if d1 < -DIRECTION_LEVEL and h4 < -DIRECTION_LEVEL and h1 < -DIRECTION_LEVEL:
        return "SHORT", "ALIGNED"
    return "—", "MIXED"


def ema_frame_ok(direction: str, price, ema, ema_prev) -> bool:
    if None in (price, ema, ema_prev):
        return False
    if direction == "LONG":
        return price > ema and ema > ema_prev
    if direction == "SHORT":
        return price < ema and ema < ema_prev
    return False


def detect_structure(highs: list[Optional[float]], lows: list[Optional[float]]) -> str:
    """
    Uses completed candles, oldest -> newest.
    First preference: last two local swing highs + last two local swing lows.
    Fallback: compare recent 3-bar average high/low with the older 3-bar average.
    """
    if any(v is None for v in highs + lows):
        return "N/A"

    highs_f = [float(v) for v in highs]
    lows_f = [float(v) for v in lows]

    swing_highs = []
    swing_lows = []
    for i in range(1, len(highs_f) - 1):
        if highs_f[i] > highs_f[i - 1] and highs_f[i] > highs_f[i + 1]:
            swing_highs.append(highs_f[i])
        if lows_f[i] < lows_f[i - 1] and lows_f[i] < lows_f[i + 1]:
            swing_lows.append(lows_f[i])

    if len(swing_highs) >= 2 and len(swing_lows) >= 2:
        hh = swing_highs[-1] > swing_highs[-2]
        hl = swing_lows[-1] > swing_lows[-2]
        lh = swing_highs[-1] < swing_highs[-2]
        ll = swing_lows[-1] < swing_lows[-2]
        if hh and hl:
            return "BULL"
        if lh and ll:
            return "BEAR"

    recent_high = sum(highs_f[-3:]) / 3
    old_high = sum(highs_f[:3]) / 3
    recent_low = sum(lows_f[-3:]) / 3
    old_low = sum(lows_f[:3]) / 3

    if recent_high > old_high and recent_low > old_low:
        return "BULL"
    if recent_high < old_high and recent_low < old_low:
        return "BEAR"
    return "MIXED"


def structure_matches(direction: str, structure: str) -> bool:
    return (direction == "LONG" and structure == "BULL") or (
        direction == "SHORT" and structure == "BEAR"
    )


def detect_brc(direction: str, candles: list[dict], atr: Optional[float]):
    """
    candles: oldest -> newest, completed H1 candles only.
    We search for a recent sequence:
      Break above/below the prior 3-candle level
      -> later retest of that level
      -> later confirmation candle.
    """
    if direction not in {"LONG", "SHORT"} or len(candles) < 7:
        return "WAIT", None

    if any(c[k] is None for c in candles for k in ("open", "high", "low", "close")):
        return "WAIT", None

    atr_value = float(atr) if atr is not None and atr > 0 else None
    fallback_price = float(candles[-1]["close"])
    tolerance = (0.25 * atr_value) if atr_value else (0.0015 * fallback_price)

    latest_progress = ("WAIT", None)

    for break_i in range(3, len(candles) - 2):
        previous = candles[break_i - 3:break_i]
        break_candle = candles[break_i]

        if direction == "LONG":
            level = max(float(c["high"]) for c in previous)
            broke = float(break_candle["close"]) > level
        else:
            level = min(float(c["low"]) for c in previous)
            broke = float(break_candle["close"]) < level

        if not broke:
            continue

        latest_progress = ("BREAK", level)

        for retest_i in range(break_i + 1, len(candles) - 1):
            retest = candles[retest_i]

            if direction == "LONG":
                touched = float(retest["low"]) <= level + tolerance
                held = float(retest["close"]) >= level - tolerance
            else:
                touched = float(retest["high"]) >= level - tolerance
                held = float(retest["close"]) <= level + tolerance

            if not (touched and held):
                continue

            latest_progress = ("RETEST", level)

            for confirm_i in range(retest_i + 1, len(candles)):
                confirm = candles[confirm_i]
                if direction == "LONG":
                    confirmed = (
                        float(confirm["close"]) > float(confirm["open"])
                        and float(confirm["close"]) > level
                    )
                else:
                    confirmed = (
                        float(confirm["close"]) < float(confirm["open"])
                        and float(confirm["close"]) < level
                    )

                if confirmed:
                    return "READY", level

    return latest_progress


def calc_quality(
    direction: str,
    ratings: tuple[Optional[float], Optional[float], Optional[float]],
    ema_passes: int,
    adx_h4: Optional[float],
    adx_h1: Optional[float],
    d1_structure: str,
    h4_structure: str,
    brc_status: str,
) -> float:
    if direction not in {"LONG", "SHORT"}:
        return 0.0

    valid_ratings = [abs(v) for v in ratings if v is not None]
    rating_score = (sum(valid_ratings) / len(valid_ratings) * 25) if valid_ratings else 0.0

    ema_score = (ema_passes / 3) * 20

    adx_score = 0.0
    for adx in (adx_h4, adx_h1):
        if adx is not None:
            adx_score += min(max((adx - 15) / 20, 0), 1) * 7.5

    structure_score = 0.0
    if structure_matches(direction, d1_structure):
        structure_score += 10
    if structure_matches(direction, h4_structure):
        structure_score += 10

    brc_score = {
        "WAIT": 0,
        "BREAK": 6,
        "RETEST": 12,
        "READY": 20,
    }.get(brc_status, 0)

    return round(min(rating_score + ema_score + adx_score + structure_score + brc_score, 100), 1)


def setup_grade(
    direction: str,
    ema_passes: int,
    adx_h4: Optional[float],
    adx_h1: Optional[float],
    d1_structure: str,
    h4_structure: str,
    brc_status: str,
    quality: float,
) -> str:
    if direction not in {"LONG", "SHORT"}:
        return "—"

    structure_both = (
        structure_matches(direction, d1_structure)
        and structure_matches(direction, h4_structure)
    )
    adx_ok = (
        adx_h4 is not None and adx_h4 >= ADX_MIN
        and adx_h1 is not None and adx_h1 >= ADX_MIN
    )

    if brc_status == "READY" and ema_passes == 3 and structure_both and adx_ok:
        return "A+ READY"
    if brc_status in {"RETEST", "READY"} and ema_passes >= 2 and quality >= 65:
        return "A"
    return "WATCH"


def row_series(row, prefix: str, n: int):
    # API response gives bar 1 as newest. Reverse to oldest -> newest.
    return [safe_float(row.get(f"{prefix} {i}")) for i in range(n, 0, -1)]


def scan_pair(pair: str) -> PairScan:
    try:
        row = fetch_pair(pair)
        if row is None:
            return PairScan(
                pair, "", "", "—", "NO DATA", None, None, None, None,
                0, 3, None, None, "N/A", "N/A", "WAIT", None, 0.0, "—"
            )

        symbol = str(row.get("Symbol", ""))
        provider = symbol.split(":", 1)[0] if ":" in symbol else ""

        d1 = safe_float(row.get("Technical Rating"))
        h4 = safe_float(row.get("Recommend All|240"))
        h1 = safe_float(row.get("Recommend All|60"))
        price = safe_float(row.get("Price"))
        direction, bias = classify_alignment(d1, h4, h1)

        ema_d1 = safe_float(row.get("EMA50 D1"))
        ema_d1_prev = safe_float(row.get("EMA50 D1 Prev"))
        ema_h4 = safe_float(row.get("EMA50 H4"))
        ema_h4_prev = safe_float(row.get("EMA50 H4 Prev"))
        ema_h1 = safe_float(row.get("EMA50 H1"))
        ema_h1_prev = safe_float(row.get("EMA50 H1 Prev"))

        ema_passes = sum([
            ema_frame_ok(direction, price, ema_d1, ema_d1_prev),
            ema_frame_ok(direction, price, ema_h4, ema_h4_prev),
            ema_frame_ok(direction, price, ema_h1, ema_h1_prev),
        ])

        adx_h4 = safe_float(row.get("ADX H4"))
        adx_h1 = safe_float(row.get("ADX H1"))
        atr_h1 = safe_float(row.get("ATR H1"))

        d1_highs = row_series(row, "D1 High", STRUCTURE_BARS)
        d1_lows = row_series(row, "D1 Low", STRUCTURE_BARS)
        h4_highs = row_series(row, "H4 High", STRUCTURE_BARS)
        h4_lows = row_series(row, "H4 Low", STRUCTURE_BARS)

        d1_structure = detect_structure(d1_highs, d1_lows)
        h4_structure = detect_structure(h4_highs, h4_lows)

        candles = []
        for i in range(BRC_BARS, 0, -1):
            candles.append({
                "open": safe_float(row.get(f"H1 Open {i}")),
                "high": safe_float(row.get(f"H1 High {i}")),
                "low": safe_float(row.get(f"H1 Low {i}")),
                "close": safe_float(row.get(f"H1 Close {i}")),
            })

        brc_status, zone = detect_brc(direction, candles, atr_h1)

        quality = calc_quality(
            direction,
            (d1, h4, h1),
            ema_passes,
            adx_h4,
            adx_h1,
            d1_structure,
            h4_structure,
            brc_status,
        )

        grade = setup_grade(
            direction,
            ema_passes,
            adx_h4,
            adx_h1,
            d1_structure,
            h4_structure,
            brc_status,
            quality,
        )

        return PairScan(
            pair=pair,
            symbol=symbol,
            provider=provider,
            direction=direction,
            bias=bias,
            d1_rating=d1,
            h4_rating=h4,
            h1_rating=h1,
            price=price,
            ema_passes=ema_passes,
            ema_total=3,
            adx_h4=adx_h4,
            adx_h1=adx_h1,
            d1_structure=d1_structure,
            h4_structure=h4_structure,
            brc_status=brc_status,
            zone=zone,
            quality_score=quality,
            setup_grade=grade,
        )

    except Exception as exc:
        print(f"[WARN] {pair}: {exc}")
        return PairScan(
            pair, "", "", "—", "ERROR", None, None, None, None,
            0, 3, None, None, "N/A", "N/A", "WAIT", None, 0.0, "—"
        )


def scan_all_pairs() -> list[PairScan]:
    results = []
    for index, pair in enumerate(PAIRS, start=1):
        print(f"[{index:02d}/{len(PAIRS)}] Scan {pair}...")
        results.append(scan_pair(pair))
        time.sleep(0.15)
    return results


def candidates(results: list[PairScan]) -> list[PairScan]:
    selected = [r for r in results if r.direction in {"LONG", "SHORT"}]
    priority = {"A+ READY": 0, "A": 1, "WATCH": 2, "—": 3}
    selected.sort(key=lambda r: (priority.get(r.setup_grade, 9), -r.quality_score, r.pair))
    return selected


def fmt_num(value: Optional[float], digits: int = 1) -> str:
    if value is None:
        return "N/A"
    return f"{value:.{digits}f}"


def fmt_zone(value: Optional[float]) -> str:
    if value is None:
        return "—"
    if abs(value) >= 20:
        return f"{value:.3f}"
    return f"{value:.5f}"


def write_markdown(results: list[PairScan], path: str = "LATEST_FOREX_SCAN.md") -> None:
    now = datetime.now(ZoneInfo("Europe/Athens"))
    top = candidates(results)
    ready = [r for r in top if r.setup_grade == "A+ READY"]

    lines = [
        "# Latest Forex Scan",
        "",
        f"**Τελευταία ενημέρωση:** {now:%d/%m/%Y %H:%M} (Europe/Athens)",
        "",
        f"**Pairs:** {len(results)}  |  **Aligned:** {len(top)}  |  **A+ READY:** {len(ready)}",
        "",
        "> Το Quality Score είναι βαθμός συμφωνίας φίλτρων, **όχι πιθανότητα κέρδους**.",
        "",
        "> **ENTRY READY** απαιτεί: D1/H4/H1 alignment + EMA50 + D1/H4 structure + ADX + ολοκληρωμένο H1 Break → Retest → Confirmation.",
        "",
        "## Top candidates",
        "",
    ]

    if top:
        lines += [
            "| # | Pair | Dir | Setup | Bias | EMA50 | D1 Struct | H4 Struct | ADX H4 | ADX H1 | B→R→C | H1 Zone | Quality |",
            "|---:|---|---|---|---|---:|---|---|---:|---:|---|---:|---:|",
        ]
        for i, r in enumerate(top, start=1):
            lines.append(
                f"| {i} | **{r.pair}** | {r.direction} | **{r.setup_grade}** | {r.bias} | "
                f"{r.ema_passes}/3 | {r.d1_structure} | {r.h4_structure} | "
                f"{fmt_num(r.adx_h4)} | {fmt_num(r.adx_h1)} | **{r.brc_status}** | "
                f"{fmt_zone(r.zone)} | **{r.quality_score:.1f}/100** |"
            )
    else:
        lines.append("Δεν βρέθηκε αυτή τη στιγμή D1 + H4 + H1 alignment.")

    lines += [
        "",
        "### Rating detail",
        "",
        "| Pair | D1 | H4 | H1 | Direction |",
        "|---|---|---|---|---|",
    ]
    for r in top:
        lines.append(
            f"| {r.pair} | {rating_text(r.d1_rating)} | {rating_text(r.h4_rating)} | "
            f"{rating_text(r.h1_rating)} | {r.direction} |"
        )

    lines += [
        "",
        "## Όλα τα 28 pairs",
        "",
        "| Pair | D1 | H4 | H1 | Dir | EMA | D1 Struct | H4 Struct | BRC | Quality |",
        "|---|---|---|---|---|---:|---|---|---|---:|",
    ]
    for r in sorted(results, key=lambda x: x.pair):
        lines.append(
            f"| {r.pair} | {rating_text(r.d1_rating)} | {rating_text(r.h4_rating)} | "
            f"{rating_text(r.h1_rating)} | {r.direction} | {r.ema_passes}/3 | "
            f"{r.d1_structure} | {r.h4_structure} | {r.brc_status} | {r.quality_score:.1f} |"
        )

    lines += [
        "",
        "## Πώς διαβάζεται",
        "",
        "- **Bias STRONG/ALIGNED:** συμφωνία Technical Rating σε D1/H4/H1.",
        "- **EMA50 3/3:** τιμή και κλίση EMA50 συμφωνούν με την κατεύθυνση και στα 3 TF.",
        "- **D1/H4 Struct:** BULL ή BEAR από ολοκληρωμένα swing highs/lows.",
        "- **ADX:** πάνω από ~20 δείχνει ισχυρότερη τάση· δεν είναι μόνο του σήμα εισόδου.",
        "- **BRC WAIT/BREAK/RETEST/READY:** πρόοδος του H1 Break → Retest → Confirmation.",
        "- **A+ READY:** το πιο αυστηρό φίλτρο του scanner. Ακόμα χρειάζεται ανθρώπινος έλεγχος chart πριν από trade.",
        "",
    ]

    Path(path).write_text("\n".join(lines), encoding="utf-8")


def print_results(results: list[PairScan]) -> None:
    top = candidates(results)
    print("\n" + "=" * 130)
    print("ADVANCED FOREX SCANNER — 28 PAIRS")
    print("=" * 130)
    print(
        f"{'#':<3} {'PAIR':<8} {'DIR':<6} {'SETUP':<10} {'EMA':<5} "
        f"{'D1':<6} {'H4':<6} {'ADX4':>6} {'ADX1':>6} {'BRC':<7} {'QUALITY':>8}"
    )
    print("-" * 130)

    for i, r in enumerate(top, start=1):
        print(
            f"{i:<3} {r.pair:<8} {r.direction:<6} {r.setup_grade:<10} "
            f"{r.ema_passes}/3  {r.d1_structure:<6} {r.h4_structure:<6} "
            f"{fmt_num(r.adx_h4):>6} {fmt_num(r.adx_h1):>6} "
            f"{r.brc_status:<7} {r.quality_score:>7.1f}"
        )

    ready = sum(1 for r in top if r.setup_grade == "A+ READY")
    print("-" * 130)
    print(f"Checked: {len(results)} | Aligned: {len(top)} | A+ READY: {ready}")
    print("Quality Score = confluence score, NOT win probability.")


def main():
    print("Ξεκινά advanced scan 28 Forex pairs...")
    results = scan_all_pairs()
    print_results(results)
    write_markdown(results)
    print("\nΑποθηκεύτηκε: LATEST_FOREX_SCAN.md")


if __name__ == "__main__":
    main()
