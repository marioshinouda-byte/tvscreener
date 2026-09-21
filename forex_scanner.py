"""
Advanced Forex Scanner — 28 liquid pairs
==========================================

Primary source: TradingView Screener (ratings, EMA50, ADX).
Secondary candle source: Yahoo Finance via yfinance (H1 candles used to derive
H4/D1 market structure and H1 Break -> Retest -> Confirmation).

Important:
- Quality Score is a confluence score, NOT a win probability.
- A+ READY is a strict filter, NOT an automatic trade instruction.
- H4/D1 candles derived from Yahoo H1 data can differ slightly from TradingView
  candle boundaries/provider data.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

import pandas as pd
import yfinance as yf

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
MIN_RR = 1.2
SL_ATR_BUFFER = 0.35
MAX_READY_DISTANCE_ATR = 0.75
MAX_BREAK_TO_RETEST_BARS = 3
MAX_RETEST_TO_CONFIRM_BARS = 2


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
    candles: str
    entry: Optional[float]
    stop_loss: Optional[float]
    take_profit: Optional[float]
    rr: Optional[float]
    rr_pass: bool


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


QUERY_FIELDS = [
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
]


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


def fetch_candle_history(pair: str):
    """
    Yahoo Finance H1 data. H4 and D1 are derived from H1 so structure and BRC
    use one consistent candle source.
    """
    ticker = f"{pair}=X"
    df = yf.download(
        ticker,
        period="60d",
        interval="1h",
        auto_adjust=False,
        progress=False,
        threads=False,
    )

    if df is None or df.empty:
        return None

    if isinstance(df.columns, pd.MultiIndex):
        if ticker in df.columns.get_level_values(-1):
            try:
                df = df.xs(ticker, axis=1, level=-1)
            except Exception:
                df.columns = df.columns.get_level_values(0)
        else:
            df.columns = df.columns.get_level_values(0)

    wanted = ["Open", "High", "Low", "Close"]
    if not all(col in df.columns for col in wanted):
        return None

    h1 = df[wanted].dropna().copy()
    if len(h1) < 80:
        return None

    # Exclude newest H1 candle in case it is still forming.
    h1 = h1.iloc[:-1]

    agg = {"Open": "first", "High": "max", "Low": "min", "Close": "last"}
    h4 = h1.resample("4h").agg(agg).dropna()
    d1 = h1.resample("1D").agg(agg).dropna()

    # Exclude potentially incomplete current H4/D1 aggregates.
    if len(h4) > 1:
        h4 = h4.iloc[:-1]
    if len(d1) > 1:
        d1 = d1.iloc[:-1]

    if len(h1) < 30 or len(h4) < 20 or len(d1) < 15:
        return None

    return h1, h4, d1


def detect_structure(frame: pd.DataFrame, lookback: int = 30) -> str:
    """
    Market-structure proxy from completed candles.
    Prefers the last two local swing highs and lows.
    """
    if frame is None or len(frame) < 9:
        return "N/A"

    data = frame.tail(lookback)
    highs = data["High"].astype(float).tolist()
    lows = data["Low"].astype(float).tolist()

    swing_highs = []
    swing_lows = []
    for i in range(1, len(highs) - 1):
        if highs[i] > highs[i - 1] and highs[i] > highs[i + 1]:
            swing_highs.append(highs[i])
        if lows[i] < lows[i - 1] and lows[i] < lows[i + 1]:
            swing_lows.append(lows[i])

    if len(swing_highs) >= 2 and len(swing_lows) >= 2:
        hh = swing_highs[-1] > swing_highs[-2]
        hl = swing_lows[-1] > swing_lows[-2]
        lh = swing_highs[-1] < swing_highs[-2]
        ll = swing_lows[-1] < swing_lows[-2]

        if hh and hl:
            return "BULL"
        if lh and ll:
            return "BEAR"

    recent = data.tail(6)
    older = data.iloc[-12:-6]
    if len(older) == 6:
        recent_high = float(recent["High"].mean())
        recent_low = float(recent["Low"].mean())
        older_high = float(older["High"].mean())
        older_low = float(older["Low"].mean())

        if recent_high > older_high and recent_low > older_low:
            return "BULL"
        if recent_high < older_high and recent_low < older_low:
            return "BEAR"

    return "MIXED"


def structure_matches(direction: str, structure: str) -> bool:
    return (direction == "LONG" and structure == "BULL") or (
        direction == "SHORT" and structure == "BEAR"
    )


def current_atr(frame: pd.DataFrame, period: int = 14) -> Optional[float]:
    if frame is None or len(frame) < period + 2:
        return None

    high = frame["High"].astype(float)
    low = frame["Low"].astype(float)
    close = frame["Close"].astype(float)
    prev_close = close.shift(1)

    tr = pd.concat(
        [
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)

    atr = tr.rolling(period).mean().iloc[-1]
    return safe_float(atr)


def local_swing_levels(frame: pd.DataFrame, lookback: int = 40):
    """Return local H4 swing highs/lows from completed candles."""
    if frame is None or len(frame) < 5:
        return [], []

    data = frame.tail(lookback)
    highs = data["High"].astype(float).tolist()
    lows = data["Low"].astype(float).tolist()

    swing_highs = []
    swing_lows = []
    for i in range(1, len(highs) - 1):
        if highs[i] > highs[i - 1] and highs[i] > highs[i + 1]:
            swing_highs.append(highs[i])
        if lows[i] < lows[i - 1] and lows[i] < lows[i + 1]:
            swing_lows.append(lows[i])

    return swing_highs, swing_lows


def calculate_trade_plan(
    direction: str,
    brc_status: str,
    zone: Optional[float],
    h1: pd.DataFrame,
    h4: pd.DataFrame,
):
    """
    Conservative plan created only after a fresh H1 BRC confirmation.

    Entry = latest completed H1 close.
    SL = BRC zone +/- 0.35 * H1 ATR(14).
    TP = nearest completed H4 swing target beyond entry.
    RR is rejected when below MIN_RR.
    """
    if (
        direction not in {"LONG", "SHORT"}
        or brc_status != "READY"
        or zone is None
        or h1 is None
        or h4 is None
        or h1.empty
        or h4.empty
    ):
        return None, None, None, None, False

    entry = safe_float(h1["Close"].iloc[-1])
    atr = current_atr(h1)
    if entry is None or atr is None or atr <= 0:
        return None, None, None, None, False

    buffer = SL_ATR_BUFFER * atr
    swing_highs, swing_lows = local_swing_levels(h4)

    if direction == "LONG":
        stop = float(zone) - buffer
        if stop >= entry:
            return entry, None, None, None, False

        candidates = sorted(level for level in swing_highs if level > entry)
        target = candidates[0] if candidates else None
        if target is None:
            fallback = safe_float(h4["High"].tail(20).max())
            if fallback is not None and fallback > entry:
                target = fallback

        if target is None:
            return entry, stop, None, None, False

        risk = entry - stop
        reward = target - entry

    else:
        stop = float(zone) + buffer
        if stop <= entry:
            return entry, None, None, None, False

        candidates = sorted(
            (level for level in swing_lows if level < entry),
            reverse=True,
        )
        target = candidates[0] if candidates else None
        if target is None:
            fallback = safe_float(h4["Low"].tail(20).min())
            if fallback is not None and fallback < entry:
                target = fallback

        if target is None:
            return entry, stop, None, None, False

        risk = stop - entry
        reward = entry - target

    if risk <= 0 or reward <= 0:
        return entry, stop, target, None, False

    rr = round(reward / risk, 2)
    return entry, stop, target, rr, rr >= MIN_RR


def detect_brc(direction: str, h1: pd.DataFrame):
    """
    Strict H1 Break -> Retest -> Confirmation.

    READY only when:
    - the break is recent,
    - the retest happens within a few H1 candles after the break,
    - the confirmation is the LATEST completed H1 candle,
    - the latest close is not already too far from the retest zone.

    This prevents old/extended moves from being shown as READY.
    """
    if direction not in {"LONG", "SHORT"} or h1 is None or len(h1) < 20:
        return "WAIT", None

    data = h1.tail(24).copy()
    candles = [
        {
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
        }
        for _, row in data.iterrows()
    ]

    atr = current_atr(h1)
    tolerance = 0.25 * atr if atr else 0.0015 * candles[-1]["close"]
    max_ready_distance = (
        MAX_READY_DISTANCE_ATR * atr
        if atr
        else 0.0030 * candles[-1]["close"]
    )

    latest_i = len(candles) - 1
    latest_progress = ("WAIT", None)
    stale_zone = None

    # Only recent breaks are relevant.
    start = max(3, len(candles) - 9)

    for break_i in range(start, len(candles) - 2):
        previous = candles[break_i - 3:break_i]
        break_candle = candles[break_i]

        if direction == "LONG":
            level = max(c["high"] for c in previous)
            broke = break_candle["close"] > level
        else:
            level = min(c["low"] for c in previous)
            broke = break_candle["close"] < level

        if not broke:
            continue

        latest_progress = ("BREAK", level)

        max_retest_i = min(
            break_i + MAX_BREAK_TO_RETEST_BARS,
            latest_i - 1,
        )

        for retest_i in range(break_i + 1, max_retest_i + 1):
            retest = candles[retest_i]

            if direction == "LONG":
                touched = retest["low"] <= level + tolerance
                held = retest["close"] >= level - tolerance
            else:
                touched = retest["high"] >= level - tolerance
                held = retest["close"] <= level + tolerance

            if not (touched and held):
                continue

            latest_progress = ("RETEST", level)

            # Confirmation must happen very soon after the retest.
            max_confirm_i = min(
                retest_i + MAX_RETEST_TO_CONFIRM_BARS,
                latest_i,
            )

            for confirm_i in range(retest_i + 1, max_confirm_i + 1):
                confirm = candles[confirm_i]

                if direction == "LONG":
                    confirmed = (
                        confirm["close"] > confirm["open"]
                        and confirm["close"] > level
                    )
                else:
                    confirmed = (
                        confirm["close"] < confirm["open"]
                        and confirm["close"] < level
                    )

                if not confirmed:
                    continue

                # Old confirmation is no longer an entry signal.
                if confirm_i != latest_i:
                    stale_zone = level
                    continue

                # Do not chase price if it already extended too far from zone.
                distance = abs(confirm["close"] - level)
                if distance > max_ready_distance:
                    return "WAIT NEW RETEST", level

                return "READY", level

    if stale_zone is not None:
        return "WAIT NEW RETEST", stale_zone

    # A retest from many candles ago is no longer "live".
    if latest_progress[0] == "RETEST":
        return "WAIT NEW RETEST", latest_progress[1]

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
        "WAIT NEW RETEST": 0,
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
    rr_pass: bool,
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

    if brc_status == "READY" and ema_passes == 3 and structure_both and adx_ok and rr_pass:
        return "A+ READY"
    if brc_status == "READY" and ema_passes >= 2 and quality >= 65 and rr_pass:
        return "A"
    if brc_status == "RETEST" and ema_passes >= 2 and quality >= 65:
        return "A"
    return "WATCH"


def scan_pair(pair: str) -> PairScan:
    try:
        row = fetch_pair(pair)
        if row is None:
            return PairScan(
                pair, "", "", "—", "NO DATA", None, None, None, None,
                0, 3, None, None, "N/A", "N/A", "WAIT", None, 0.0, "—", "N/A",
                None, None, None, None, False
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

        d1_structure = "N/A"
        h4_structure = "N/A"
        brc_status = "WAIT"
        zone = None
        candle_status = "SKIPPED"
        entry = None
        stop_loss = None
        take_profit = None
        rr = None
        rr_pass = False

        if direction in {"LONG", "SHORT"}:
            candle_history = fetch_candle_history(pair)
            if candle_history is not None:
                h1_candles, h4_candles, d1_candles = candle_history
                d1_structure = detect_structure(d1_candles)
                h4_structure = detect_structure(h4_candles)
                brc_status, zone = detect_brc(direction, h1_candles)
                entry, stop_loss, take_profit, rr, rr_pass = calculate_trade_plan(
                    direction, brc_status, zone, h1_candles, h4_candles
                )
                candle_status = "YF"
            else:
                candle_status = "N/A"

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
            rr_pass,
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
            candles=candle_status,
            entry=entry,
            stop_loss=stop_loss,
            take_profit=take_profit,
            rr=rr,
            rr_pass=rr_pass,
        )

    except Exception as exc:
        print(f"[WARN] {pair}: {exc}")
        return PairScan(
            pair, "", "", "—", "ERROR", None, None, None, None,
            0, 3, None, None, "N/A", "N/A", "WAIT", None, 0.0, "—", "ERROR",
            None, None, None, None, False
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


def fmt_price(pair: str, value: Optional[float]) -> str:
    if value is None:
        return "—"
    return f"{value:.3f}" if "JPY" in pair else f"{value:.5f}"


def fmt_rr(value: Optional[float], passed: bool) -> str:
    if value is None:
        return "—"
    mark = "✅" if passed else "❌"
    return f"{value:.2f} {mark}"


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
        "> Ratings / EMA50 / ADX: TradingView Screener. Structure / BRC: Yahoo Finance H1 candles (H4/D1 derived). Μπορεί να υπάρχουν μικρές διαφορές candle boundaries από TradingView.",
        "",
        "> **A+ READY** απαιτεί: D1/H4/H1 alignment + EMA50 3/3 + D1/H4 structure + ADX + **confirmation στο τελευταίο κλεισμένο H1**, χωρίς υπερβολική απόσταση από τη zone + **RR ≥ 1.2**.",
        "",
        "## Top candidates",
        "",
    ]

    if top:
        lines += [
            "| # | Pair | Dir | Setup | Bias | EMA50 | D1 Struct | H4 Struct | ADX H4 | ADX H1 | B→R→C | H1 Zone | Entry | SL | TP | RR | Quality |",
            "|---:|---|---|---|---|---:|---|---|---:|---:|---|---:|---:|---:|---:|---:|---:|",
        ]
        for i, r in enumerate(top, start=1):
            lines.append(
                f"| {i} | **{r.pair}** | {r.direction} | **{r.setup_grade}** | {r.bias} | "
                f"{r.ema_passes}/3 | {r.d1_structure} | {r.h4_structure} | "
                f"{fmt_num(r.adx_h4)} | {fmt_num(r.adx_h1)} | **{r.brc_status}** | "
                f"{fmt_zone(r.zone)} | {fmt_price(r.pair, r.entry)} | "
                f"{fmt_price(r.pair, r.stop_loss)} | {fmt_price(r.pair, r.take_profit)} | "
                f"**{fmt_rr(r.rr, r.rr_pass)}** | **{r.quality_score:.1f}/100** |"
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
        "| Pair | D1 | H4 | H1 | Dir | EMA | D1 Struct | H4 Struct | BRC | RR | Quality |",
        "|---|---|---|---|---|---:|---|---|---|---:|---:|",
    ]
    for r in sorted(results, key=lambda x: x.pair):
        lines.append(
            f"| {r.pair} | {rating_text(r.d1_rating)} | {rating_text(r.h4_rating)} | "
            f"{rating_text(r.h1_rating)} | {r.direction} | {r.ema_passes}/3 | "
            f"{r.d1_structure} | {r.h4_structure} | {r.brc_status} | "
            f"{fmt_rr(r.rr, r.rr_pass)} | {r.quality_score:.1f} |"
        )

    lines += [
        "",
        "## Πώς διαβάζεται",
        "",
        "- **Bias STRONG/ALIGNED:** συμφωνία Technical Rating σε D1/H4/H1.",
        "- **EMA50 3/3:** τιμή και κλίση EMA50 συμφωνούν με την κατεύθυνση και στα 3 TF.",
        "- **D1/H4 Struct:** BULL ή BEAR από ολοκληρωμένα swing highs/lows.",
        "- **ADX:** πάνω από ~20 δείχνει ισχυρότερη τάση· δεν είναι μόνο του σήμα εισόδου.",
        "- **BRC WAIT/BREAK/RETEST/READY:** πρόοδος του H1 Break → Retest → Confirmation. **WAIT NEW RETEST** σημαίνει ότι το παλιό confirmation θεωρείται πλέον ξεπερασμένο ή η τιμή έχει απομακρυνθεί πολύ από τη zone.",
        "- **Entry/SL/TP:** εμφανίζονται μόνο όταν το BRC είναι READY. Entry = τελευταίο κλεισμένο H1, SL = H1 zone ± 0.35×ATR, TP = κοντινότερο ολοκληρωμένο H4 swing target.",
        f"- **RR:** ✅ όταν RR ≥ {MIN_RR:.1f}, ❌ όταν είναι χαμηλότερο. Το A+ READY απαιτεί RR pass.",
        "- **A+ READY:** το αυστηρότερο φίλτρο. Πριν από trade χρειάζεται τελικός οπτικός έλεγχος chart, spread/news και sizing.",
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
        f"{'D1':<6} {'H4':<6} {'ADX4':>6} {'ADX1':>6} {'BRC':<7} {'RR':>6} {'QUALITY':>8}"
    )
    print("-" * 130)

    for i, r in enumerate(top, start=1):
        print(
            f"{i:<3} {r.pair:<8} {r.direction:<6} {r.setup_grade:<10} "
            f"{r.ema_passes}/3  {r.d1_structure:<6} {r.h4_structure:<6} "
            f"{fmt_num(r.adx_h4):>6} {fmt_num(r.adx_h1):>6} "
            f"{r.brc_status:<7} {fmt_num(r.rr, 2):>6} {r.quality_score:>7.1f}"
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
