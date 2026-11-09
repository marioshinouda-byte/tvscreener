"""
Advanced Forex Scanner — 28 liquid pairs
==========================================

Primary OHLC source: Yahoo Finance via yfinance. EMA50, ADX, structure, price,
and Break -> Retest -> Confirmation are calculated from fully closed candles
from this single feed. TradingView Screener ratings are context only.

Important:
- Quality Score is a confluence score, NOT a win probability.
- A+ READY is a strict filter, NOT an automatic trade instruction.
- Outdated Yahoo H1 candles are marked YF-STALE and are NOT actionable.
  No trend or reversal signals are generated when the source is stale.
"""

from __future__ import annotations

import math
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

import pandas as pd
import yfinance as yf
from market_data_quality import verify_h1_history

from tvscreener import CryptoField, CryptoScreener, ForexField, ForexScreener


PAIRS = [
    "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "USDCAD", "AUDUSD", "NZDUSD",
    "EURGBP", "EURJPY", "EURCHF", "EURCAD", "EURAUD", "EURNZD",
    "GBPJPY", "GBPCHF", "GBPCAD", "GBPAUD", "GBPNZD",
    "AUDJPY", "AUDCHF", "AUDCAD", "AUDNZD",
    "NZDJPY", "NZDCHF", "NZDCAD",
    "CADJPY", "CADCHF", "CHFJPY",
]

CRYPTO_ASSETS = ["BTC", "ETH", "SOL"]
CRYPTO_PROVIDER_PRIORITY = ["COINBASE", "KRAKEN", "BITSTAMP", "BINANCE", "BYBIT"]

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
MAX_BREAK_TO_RETEST_BARS = 12
MAX_RETEST_TO_CONFIRM_BARS = 2
MAX_CONFIRMED_SETUP_AGE_BARS = 3
MAX_H1_DATA_AGE_HOURS = 4
WEEKLY_TOP5_PATH = "WEEKLY_FOREX_TOP5.json"
HOT_NEW_MIN_SCORE = 70.0
H1_SWING_LEFT = 8
H1_SWING_RIGHT = 8
H1_SWING_PROMINENCE_ATR = 0.50
BREAK_CLOSE_BUFFER_ATR = 0.05

# Independent, reversible mode for higher-timeframe reversal setups. Set
# ENABLE_HTF_REVERSAL=false to disable it without touching the A+ trend model.
ENABLE_HTF_REVERSAL = os.getenv("ENABLE_HTF_REVERSAL", "true").strip().lower() not in {
    "0", "false", "no", "off",
}
REVERSAL_MIN_RR = 3.0
REVERSAL_D1_LOOKBACK = 55
REVERSAL_H4_TOUCH_BARS = 18
REVERSAL_ZONE_TOUCH_ATR = 0.55
REVERSAL_INVALIDATION_ATR = 0.20
REVERSAL_SL_BUFFER_ATR = 0.20
# Pre-break reversal contexts are ARMED only when price is genuinely close
# to the required H1 break. ATR keeps the rule consistent across all pairs.
REVERSAL_MAX_ARMED_BREAK_DISTANCE_ATR = 1.50
REVERSAL_MIN_ACTIVE_SCORE = 75.0

_CANDLE_HISTORY_CACHE = {}


@dataclass(frozen=True)
class QueryField:
    """Minimal field object accepted by tvscreener.select()."""

    field_name: str
    label: str
    historical: bool = False

    def has_recommendation(self) -> bool:
        return False


@dataclass
class ReversalScan:
    direction: str = "—"
    status: str = "NO SETUP"
    score: float = 0.0
    htf_zone: Optional[float] = None
    zone_kind: str = "—"
    sweep: bool = False
    rejection: bool = False
    displacement: bool = False
    h4_structure: str = "N/A"
    brc_status: str = "WAIT"
    h1_zone: Optional[float] = None
    entry: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    rr: Optional[float] = None
    rr_pass: bool = False
    note: str = ""


@dataclass
class OandaPreScreen:
    """OANDA-only TradingView context, NEVER a BRC or entry signal."""
    direction: str
    score: float
    price: Optional[float]
    ema_passes: int
    ema_checked: int
    adx_h4: Optional[float]
    adx_h1: Optional[float]
    oanda_prev_h1_open: Optional[float] = None
    oanda_h1_update: Optional[float] = None


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
    reversal: Optional[ReversalScan] = None
    # Weekly rating is context only; it does not change the D1/H4/H1 A+ rules.
    w1_rating: Optional[float] = None
    # Timestamp of the last closed H1 candle used by BRC and structure checks.
    h1_closed_at: Optional[object] = None
    oanda_prescreen: Optional[OandaPreScreen] = None


@dataclass
class CryptoScan:
    asset: str
    symbol: str
    provider: str
    price: Optional[float]
    w1_rating: Optional[float]
    d1_rating: Optional[float]
    h4_rating: Optional[float]
    h1_rating: Optional[float]
    direction: str
    bias: str


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
    ForexField.RECOMMEND_ALL_1W,   # W1 context only
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
    ForexField.CLOSE_60,
    ForexField.TIME_60,
    ForexField.LAST_BAR_UPDATE_TIME_60,
    q("close[1]|60", "OANDA Previous H1 Close"),
    q("time[1]|60", "OANDA Previous H1 Open"),
]

CRYPTO_QUERY_FIELDS = [
    CryptoField.NAME,
    CryptoField.RECOMMEND_ALL_1W,
    CryptoField.TECHNICAL_RATING,
    CryptoField.RECOMMEND_ALL_240,
    CryptoField.RECOMMEND_ALL_60,
    CryptoField.PRICE,
]


def crypto_provider_rank(symbol: str) -> int:
    provider = symbol.split(":", 1)[0] if ":" in symbol else ""
    try:
        return CRYPTO_PROVIDER_PRIORITY.index(provider)
    except ValueError:
        return len(CRYPTO_PROVIDER_PRIORITY)


def fetch_crypto(asset: str):
    """Fetch a liquid spot USD/USDT market for BTC, ETH or SOL."""
    candidates = []
    for quote_rank, market in enumerate((f"{asset}USD", f"{asset}USDT")):
        screener = CryptoScreener()
        screener.select(*CRYPTO_QUERY_FIELDS)
        screener.search(market)
        screener.set_range(0, 50)
        data = screener.get()
        if data.empty:
            continue

        for _, row in data.iterrows():
            symbol = str(row.get("Symbol", ""))
            raw = symbol.split(":", 1)[-1].upper()
            if raw == market:
                candidates.append((quote_rank, crypto_provider_rank(symbol), row))

    if not candidates:
        return None

    candidates.sort(key=lambda item: (item[0], item[1]))
    return candidates[0][2]


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


def ema_frame_signal(frame: pd.DataFrame, period: int = 50) -> Optional[str]:
    """Return the EMA50 direction from a frame of fully closed candles."""
    if frame is None or len(frame) < period + 2:
        return None
    close = frame["Close"].astype(float)
    ema = close.ewm(span=period, adjust=False, min_periods=period).mean()
    price, current_ema, previous_ema = (
        safe_float(close.iloc[-1]),
        safe_float(ema.iloc[-1]),
        safe_float(ema.iloc[-2]),
    )
    if price is None or current_ema is None or previous_ema is None:
        return None
    if price > current_ema and current_ema > previous_ema:
        return "LONG"
    if price < current_ema and current_ema < previous_ema:
        return "SHORT"
    return None


def calculate_adx(frame: pd.DataFrame, period: int = 14) -> Optional[float]:
    """Calculate Wilder ADX from the same completed OHLC candles used by BRC."""
    if frame is None or len(frame) < period * 2 + 2:
        return None

    high = frame["High"].astype(float)
    low = frame["Low"].astype(float)
    close = frame["Close"].astype(float)
    up_move = high.diff()
    down_move = -low.diff()
    plus_dm = up_move.where((up_move > down_move) & (up_move > 0), 0.0)
    minus_dm = down_move.where((down_move > up_move) & (down_move > 0), 0.0)
    previous_close = close.shift(1)
    true_range = pd.concat(
        [(high - low), (high - previous_close).abs(), (low - previous_close).abs()],
        axis=1,
    ).max(axis=1)

    alpha = 1.0 / period
    atr = true_range.ewm(alpha=alpha, min_periods=period, adjust=False).mean()
    plus_di = 100.0 * plus_dm.ewm(alpha=alpha, min_periods=period, adjust=False).mean() / atr
    minus_di = 100.0 * minus_dm.ewm(alpha=alpha, min_periods=period, adjust=False).mean() / atr
    denominator = plus_di + minus_di
    dx = 100.0 * (plus_di - minus_di).abs() / denominator.where(denominator != 0)
    adx = dx.ewm(alpha=alpha, min_periods=period, adjust=False).mean()
    return safe_float(adx.iloc[-1])


def prepare_candle_history(df: pd.DataFrame):
    """Keep only fully closed H1 candles and derive fully closed H4/D1 bars."""
    if df is None or df.empty:
        return None

    wanted = ["Open", "High", "Low", "Close"]
    if not all(col in df.columns for col in wanted):
        return None


    h1 = df[wanted].dropna().copy()
    if len(h1) < 80:
        return None
    index = pd.DatetimeIndex(h1.index)
    index = index.tz_localize("UTC") if index.tz is None else index.tz_convert("UTC")
    h1.index = index
    h1 = h1.sort_index()
    if h1.index.has_duplicates:
        return None

    now = pd.Timestamp.now(tz="UTC")
    # Ignore forming H1 candles.
    h1 = h1.loc[h1.index + pd.Timedelta(hours=1) <= now]
    if len(h1) < 80:
        return None

    # OANDA default daily alignment: 17:00 America/New_York, DST-aware.
    # Remove synthetic Yahoo weekend bars before constructing any timeframe.
    ny = h1.index.tz_convert("America/New_York")
    market_open = (
        (ny.dayofweek <= 3)
        | ((ny.dayofweek == 4) & (ny.hour < 17))
        | ((ny.dayofweek == 6) & (ny.hour >= 17))
    )
    h1 = h1.loc[market_open]
    if len(h1) < 80:
        return None

    ny = h1.index.tz_convert("America/New_York")
    session_wall = (
        (ny.tz_localize(None) - pd.Timedelta(hours=17)).normalize()
        + pd.Timedelta(hours=17)
    )
    session_start = pd.DatetimeIndex(session_wall).tz_localize(
        "America/New_York"
    ).tz_convert("UTC")
    elapsed_h = ((h1.index - session_start).total_seconds() // 3600).astype(int)
    h4_starts = session_start + pd.to_timedelta((elapsed_h // 4) * 4, unit="h")

    agg = {"Open": "first", "High": "max", "Low": "min", "Close": "last"}
    h4_group = h1.groupby(h4_starts)
    d1_group = h1.groupby(session_start)
    h4 = h4_group.agg(agg)
    d1 = d1_group.agg(agg)

    # Never calculate structure from incomplete H4 or D1 bars.
    h4_counts = h4_group.size()
    d1_counts = d1_group.size()
    h4_first = h4_group.apply(lambda part: part.index[0])
    h4_last = h4_group.apply(lambda part: part.index[-1])
    d1_first = d1_group.apply(lambda part: part.index[0])
    d1_last = d1_group.apply(lambda part: part.index[-1])
    h4 = h4.loc[
        (h4_counts == 4)
        & (h4_first == h4.index)
        & (h4_last == h4.index + pd.Timedelta(hours=3))
        & (h4.index + pd.Timedelta(hours=4) <= now)
    ]
    d1 = d1.loc[
        (d1_counts >= 23)
        & (d1_first == d1.index)
        & (d1_last == d1.index + pd.Timedelta(hours=23))
        & (d1.index + pd.Timedelta(days=1) <= now)
    ]
    if len(h1) < 80 or len(h4) < 20 or len(d1) < 15:
        return None
    return h1, h4, d1


def extract_ticker_frame(df: pd.DataFrame, ticker: str):
    """Extract one ticker regardless of yfinance MultiIndex orientation."""
    if df is None or df.empty:
        return None
    if not isinstance(df.columns, pd.MultiIndex):
        return df

    for level in range(df.columns.nlevels):
        if ticker in df.columns.get_level_values(level):
            try:
                return df.xs(ticker, axis=1, level=level)
            except (KeyError, ValueError):
                continue
    return None


def log_candle_history(pair: str, df: Optional[pd.DataFrame]) -> None:
    """Show the per-pair Yahoo rows received before candle preparation."""
    if df is None:
        df = pd.DataFrame()
    print(
        f"[INFO] {pair} | candles={len(df)} "
        f"| last={df.index[-1] if len(df) else 'NONE'}"
    )


def prefetch_candle_histories(pairs: list[str]) -> None:
    """
    Fetch all H1 histories in one Yahoo request for the optional reversal mode.

    This materially lowers the chance of HTTP 429 compared with 28 individual
    downloads. Missing tickers are cached as unavailable for this scan.
    """
    missing = [pair for pair in pairs if pair not in _CANDLE_HISTORY_CACHE]
    if not missing:
        return

    tickers = [f"{pair}=X" for pair in missing]
    try:
        batch = yf.download(
            tickers=tickers,
            period="120d",
            interval="1h",
            auto_adjust=False,
            group_by="ticker",
            progress=False,
            threads=True,
        )
    except Exception as exc:
        print(f"[WARN] Yahoo batch candles: {exc}")
        batch = None

    for pair, ticker in zip(missing, tickers):
        frame = extract_ticker_frame(batch, ticker) if batch is not None else None
        log_candle_history(pair, frame)
        _CANDLE_HISTORY_CACHE[pair] = prepare_candle_history(frame)


def fetch_candle_history(pair: str):
    """
    Yahoo Finance H1 data. H4 and D1 are derived from H1 so structure and BRC
    use one consistent candle source.
    """
    if pair in _CANDLE_HISTORY_CACHE:
        return _CANDLE_HISTORY_CACHE[pair]

    ticker = f"{pair}=X"
    try:
        df = yf.download(
            ticker,
            period="120d",
            interval="1h",
            auto_adjust=False,
            progress=False,
            threads=False,
        )
    except Exception as exc:
        print(f"[WARN] {pair} Yahoo candles: {exc}")
        df = None

    frame = extract_ticker_frame(df, ticker) if df is not None else None
    log_candle_history(pair, frame)
    history = prepare_candle_history(frame)
    _CANDLE_HISTORY_CACHE[pair] = history
    return history


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


def find_key_h1_level(direction: str, h1: pd.DataFrame):
    """
    Find a CONFIRMED H1 swing resistance/support.

    We deliberately use a much wider pivot window than the old 3-candle rule:
    15 candles left + 15 candles right, close to the support/resistance logic
    the user follows on TradingView.

    LONG  -> latest confirmed swing HIGH = resistance to break.
    SHORT -> latest confirmed swing LOW  = support to break.
    """
    if direction not in {"LONG", "SHORT"} or h1 is None:
        return None, None

    data = h1.tail(180).copy()
    min_bars = H1_SWING_LEFT + H1_SWING_RIGHT + 5
    if len(data) < min_bars:
        return None, None

    highs = data["High"].astype(float).tolist()
    lows = data["Low"].astype(float).tolist()
    atr = current_atr(h1)
    min_prominence = (
        H1_SWING_PROMINENCE_ATR * atr
        if atr is not None and atr > 0
        else 0.0
    )

    pivots = []
    for i in range(H1_SWING_LEFT, len(data) - H1_SWING_RIGHT):
        left = i - H1_SWING_LEFT
        right = i + H1_SWING_RIGHT + 1

        window_high = max(highs[left:right])
        window_low = min(lows[left:right])

        if direction == "LONG":
            level = highs[i]
            is_pivot = level >= window_high
            prominence = level - window_low
        else:
            level = lows[i]
            is_pivot = level <= window_low
            prominence = window_high - level

        if is_pivot and prominence >= min_prominence:
            pivots.append((i, float(level)))

    if not pivots:
        return None, None

    # Latest confirmed major H1 pivot.
    return pivots[-1]


def detect_brc(direction: str, h1: pd.DataFrame):
    """
    H1 Break -> Retest -> Confirmation using a CONFIRMED major swing level.

    This replaces the old 3-candle high/low rule that could mark small local
    noise as BREAK.

    Status flow:
    WAIT FOR BREAK -> BREAK -> RETEST -> READY
    or WAIT NEW RETEST if the confirmation became stale/price ran away.
    """
    if direction not in {"LONG", "SHORT"} or h1 is None or len(h1) < 40:
        return "WAIT", None

    data = h1.tail(180).copy()
    candles = [
        {
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
        }
        for _, row in data.iterrows()
    ]

    pivot_i, level = find_key_h1_level(direction, data)
    if pivot_i is None or level is None:
        return "WAIT", None

    atr = current_atr(h1)
    tolerance = 0.25 * atr if atr else 0.0015 * candles[-1]["close"]
    break_buffer = (
        BREAK_CLOSE_BUFFER_ATR * atr
        if atr
        else 0.0003 * candles[-1]["close"]
    )
    max_ready_distance = (
        MAX_READY_DISTANCE_ATR * atr
        if atr
        else 0.0030 * candles[-1]["close"]
    )

    latest_i = len(candles) - 1

    # Search for a real H1 CLOSE through the confirmed swing level.
    break_i = None
    for i in range(pivot_i + 1, len(candles)):
        close = candles[i]["close"]
        if direction == "LONG":
            broke = close > level + break_buffer
        else:
            broke = close < level - break_buffer

        if broke:
            break_i = i
            break

    if break_i is None:
        return "WAIT FOR BREAK", level

    # Keep the broken zone active for the configured number of closed H1 candles.
    # The retest candle may be the latest candle; confirmation must come after it.
    max_retest_i = min(
        break_i + MAX_BREAK_TO_RETEST_BARS,
        latest_i,
    )

    retest_i = None
    for i in range(break_i + 1, max_retest_i + 1):
        retest = candles[i]

        if direction == "LONG":
            touched = retest["low"] <= level + tolerance
            held = retest["close"] >= level - tolerance
        else:
            touched = retest["high"] >= level - tolerance
            held = retest["close"] <= level + tolerance

        if touched and held:
            retest_i = i
            break

    if retest_i is None:
        # Once the configured retest window closes, discard this broken zone.
        if latest_i - break_i >= MAX_BREAK_TO_RETEST_BARS:
            return "WAIT NEW RETEST", level
        return "BREAK", level

    max_confirm_i = min(
        retest_i + MAX_RETEST_TO_CONFIRM_BARS,
        latest_i,
    )

    for confirm_i in range(retest_i + 1, max_confirm_i + 1):
        confirm = candles[confirm_i]

        retest_candle = candles[retest_i]
        if direction == "LONG":
            confirmed = (
                confirm["close"] > confirm["open"]
                and confirm["close"] > level
                and confirm["close"] > retest_candle["high"]
            )
        else:
            confirmed = (
                confirm["close"] < confirm["open"]
                and confirm["close"] < level
                and confirm["close"] < retest_candle["low"]
            )

        if not confirmed:
            continue

        # Keep READY only while the confirmation is within the configured
        # number of completed H1 candles.
        confirm_age = latest_i - confirm_i
        if confirm_age > MAX_CONFIRMED_SETUP_AGE_BARS:
            return "WAIT NEW RETEST", level

        # Invalidate the remembered setup if price closes back through the zone.
        post_confirm = candles[confirm_i + 1: latest_i + 1]
        if direction == "LONG":
            invalidated = any(
                candle["close"] < level - tolerance
                for candle in post_confirm
            )
        else:
            invalidated = any(
                candle["close"] > level + tolerance
                for candle in post_confirm
            )
        if invalidated:
            return "WAIT NEW RETEST", level

        # Don't chase a move that has already extended away from the zone now.
        if abs(candles[-1]["close"] - level) > max_ready_distance:
            return "WAIT NEW RETEST", level

        return "READY", level

    # Retest exists but no fresh confirmation yet.
    if latest_i - retest_i <= MAX_RETEST_TO_CONFIRM_BARS:
        return "RETEST", level

    return "WAIT NEW RETEST", level


def confirmed_daily_levels(frame: pd.DataFrame):
    """Return older, confirmed D1 swing zones for reversal context."""
    if frame is None or len(frame) < 12:
        return [], []

    data = frame.tail(REVERSAL_D1_LOOKBACK).copy()
    # Keep the latest two D1 candles out of the reference set. They are the
    # reaction leg; the zone must already have existed before the reaction.
    reference = data.iloc[:-2]
    if len(reference) < 8:
        return [], []

    highs = reference["High"].astype(float).tolist()
    lows = reference["Low"].astype(float).tolist()
    swing_highs = []
    swing_lows = []

    for i in range(2, len(reference) - 2):
        if highs[i] >= max(highs[i - 2:i + 3]):
            swing_highs.append(highs[i])
        if lows[i] <= min(lows[i - 2:i + 3]):
            swing_lows.append(lows[i])

    # Range extremes are valid HTF zones even when the local-pivot test did
    # not produce one near the edge of the downloaded window.
    swing_highs.append(float(reference["High"].max()))
    swing_lows.append(float(reference["Low"].min()))

    return sorted(set(swing_highs)), sorted(set(swing_lows))


def directional_rejection(direction: str, candle: pd.Series, atr: float) -> bool:
    """Wick rejection that closes back away from the tested HTF zone."""
    open_ = float(candle["Open"])
    high = float(candle["High"])
    low = float(candle["Low"])
    close = float(candle["Close"])
    candle_range = high - low
    if candle_range <= 0:
        return False

    body = abs(close - open_)
    if direction == "SHORT":
        wick = high - max(open_, close)
        closes_away = close <= high - 0.55 * candle_range
    else:
        wick = min(open_, close) - low
        closes_away = close >= low + 0.55 * candle_range

    return closes_away and wick >= max(0.25 * candle_range, 0.75 * body, 0.12 * atr)


def directional_displacement(direction: str, candle: pd.Series, atr: float) -> bool:
    """Strong H4 body closing near its directional extreme."""
    open_ = float(candle["Open"])
    high = float(candle["High"])
    low = float(candle["Low"])
    close = float(candle["Close"])
    candle_range = high - low
    body = abs(close - open_)
    if candle_range <= 0 or body < 0.55 * atr:
        return False

    if direction == "SHORT":
        return close < open_ and close <= low + 0.35 * candle_range
    return close > open_ and close >= high - 0.35 * candle_range


def calculate_reversal_trade_plan(
    direction: str,
    brc_status: str,
    h1: pd.DataFrame,
    h4: pd.DataFrame,
    d1: pd.DataFrame,
    htf_zone: float,
):
    """
    Reversal plan created only after a fresh H1 confirmation.

    SL sits beyond the recent H4 structural extreme. TP is the nearest
    completed D1 swing zone in the trade direction. A reversal is READY only
    when that natural target offers RR >= REVERSAL_MIN_RR.
    """
    if brc_status != "READY" or direction not in {"LONG", "SHORT"}:
        return None, None, None, None, False

    entry = safe_float(h1["Close"].iloc[-1])
    h4_atr = current_atr(h4)
    if entry is None or h4_atr is None or h4_atr <= 0:
        return None, None, None, None, False

    buffer = REVERSAL_SL_BUFFER_ATR * h4_atr
    swing_highs, swing_lows = local_swing_levels(d1, REVERSAL_D1_LOOKBACK)

    if direction == "SHORT":
        recent_extreme = safe_float(h4["High"].tail(REVERSAL_H4_TOUCH_BARS).max())
        if recent_extreme is None:
            return entry, None, None, None, False
        stop = max(float(htf_zone), recent_extreme) + buffer
        targets = sorted((level for level in swing_lows if level < entry), reverse=True)
        target = targets[0] if targets else safe_float(d1["Low"].tail(REVERSAL_D1_LOOKBACK).min())
        risk = stop - entry
        reward = entry - target if target is not None else 0.0
    else:
        recent_extreme = safe_float(h4["Low"].tail(REVERSAL_H4_TOUCH_BARS).min())
        if recent_extreme is None:
            return entry, None, None, None, False
        stop = min(float(htf_zone), recent_extreme) - buffer
        targets = sorted(level for level in swing_highs if level > entry)
        target = targets[0] if targets else safe_float(d1["High"].tail(REVERSAL_D1_LOOKBACK).max())
        risk = entry - stop
        reward = target - entry if target is not None else 0.0

    if target is None or risk <= 0 or reward <= 0:
        return entry, stop, target, None, False

    rr = round(reward / risk, 2)
    return entry, stop, target, rr, rr >= REVERSAL_MIN_RR


def analyze_htf_reversal(
    h1: pd.DataFrame,
    h4: pd.DataFrame,
    d1: pd.DataFrame,
) -> ReversalScan:
    """
    Independent D1 -> H4 -> H1 reversal model.

    D1 supplies an already-confirmed support/resistance zone. A recent H4
    test must then show rejection, liquidity sweep and/or displacement. H1
    BRC controls timing. No rating/EMA input from the trend model is used.
    """
    result = ReversalScan()
    if h1 is None or h4 is None or d1 is None or h4.empty or d1.empty:
        return result

    d1_atr = current_atr(d1)
    h4_atr = current_atr(h4)
    h1_atr = current_atr(h1)
    if (
        d1_atr is None or d1_atr <= 0
        or h4_atr is None or h4_atr <= 0
        or h1_atr is None or h1_atr <= 0
    ):
        return result

    swing_highs, swing_lows = confirmed_daily_levels(d1)
    if not swing_highs and not swing_lows:
        return result

    h4_data = h4.tail(max(50, REVERSAL_H4_TOUCH_BARS + 10)).copy()
    recent_start = max(0, len(h4_data) - REVERSAL_H4_TOUCH_BARS)
    latest_close = float(h4_data["Close"].iloc[-1])
    h4_structure = detect_structure(h4_data)
    evaluations = []

    for direction, levels, price_column, zone_kind in (
        ("SHORT", swing_highs, "High", "D1 RESISTANCE"),
        ("LONG", swing_lows, "Low", "D1 SUPPORT"),
    ):
        for zone in levels:
            recent_prices = h4_data[price_column].iloc[recent_start:].astype(float)
            distances = (recent_prices - float(zone)).abs()
            if distances.empty:
                continue

            touch_label = distances.idxmin()
            touch_distance = float(distances.loc[touch_label]) / d1_atr
            if touch_distance > REVERSAL_ZONE_TOUCH_ATR:
                continue

            # Use a positional index because duplicate/resampled timestamps can
            # otherwise make label lookup ambiguous.
            touch_offset = int(distances.reset_index(drop=True).idxmin())
            touch_pos = recent_start + touch_offset
            touch_candle = h4_data.iloc[touch_pos]
            evidence_window = h4_data.iloc[touch_pos:min(touch_pos + 4, len(h4_data))]
            follow_through = h4_data.iloc[touch_pos:]
            prior = h4_data.iloc[max(0, touch_pos - 8):touch_pos]

            rejection = any(
                directional_rejection(direction, candle, h4_atr)
                for _, candle in evidence_window.iterrows()
            )
            displacement = any(
                directional_displacement(direction, candle, h4_atr)
                for _, candle in follow_through.iterrows()
            )

            sweep = False
            if not prior.empty:
                if direction == "SHORT":
                    prior_level = float(prior["High"].max())
                    sweep = (
                        float(touch_candle["High"]) > prior_level + 0.03 * h4_atr
                        and float(touch_candle["Close"]) < prior_level
                    )
                else:
                    prior_level = float(prior["Low"].min())
                    sweep = (
                        float(touch_candle["Low"]) < prior_level - 0.03 * h4_atr
                        and float(touch_candle["Close"]) > prior_level
                    )

            # Also count a direct sweep of the pre-existing D1 zone.
            if direction == "SHORT":
                sweep = sweep or (
                    float(touch_candle["High"]) > zone
                    and float(touch_candle["Close"]) < zone
                )
                away = float(zone) - latest_close
                invalidated = latest_close > float(zone) + REVERSAL_INVALIDATION_ATR * d1_atr
            else:
                sweep = sweep or (
                    float(touch_candle["Low"]) < zone
                    and float(touch_candle["Close"]) > zone
                )
                away = latest_close - float(zone)
                invalidated = latest_close < float(zone) - REVERSAL_INVALIDATION_ATR * d1_atr

            moved_away = away >= 0.45 * h4_atr
            stale_move = away > 2.75 * d1_atr
            brc_status, h1_zone = detect_brc(direction, h1)

            break_distance_atr = None
            if brc_status == "WAIT FOR BREAK" and h1_zone is not None:
                h1_close = float(h1["Close"].iloc[-1])
                break_distance_atr = abs(h1_close - float(h1_zone)) / h1_atr

            score = 25.0
            score += max(0.0, 10.0 * (1.0 - touch_distance / REVERSAL_ZONE_TOUCH_ATR))
            score += 15.0 if sweep else 0.0
            score += 15.0 if rejection else 0.0
            score += 15.0 if displacement else 0.0
            score += 5.0 if moved_away else 0.0
            score += 5.0 if structure_matches(direction, h4_structure) else 0.0
            score += {
                "BREAK": 8.0,
                "RETEST": 12.0,
                "READY": 15.0,
            }.get(brc_status, 0.0)

            evidence_count = sum((sweep, rejection, displacement))
            if invalidated:
                status = "INVALID"
                note = "H4 close πέρα από τη D1 zone"
            elif stale_move:
                status = "INVALID"
                note = "Η κίνηση έχει απομακρυνθεί πολύ από τη zone"
            elif brc_status == "WAIT NEW RETEST":
                status = "INVALID"
                note = "Το H1 break/retest έληξε"
            elif brc_status == "BREAK":
                status = "WAIT RETEST"
                note = "H1 break — περιμένει retest"
            elif brc_status == "RETEST":
                status = "ARMED"
                note = "H1 retest — περιμένει confirmation"
            elif (
                evidence_count >= 2
                and moved_away
                and brc_status == "WAIT FOR BREAK"
                and break_distance_atr is not None
                and break_distance_atr <= REVERSAL_MAX_ARMED_BREAK_DISTANCE_ATR
            ):
                status = "ARMED"
                note = (
                    "HTF αντίδραση — H1 break κοντά "
                    f"({break_distance_atr:.1f} ATR)"
                )
            elif (
                evidence_count >= 2
                and moved_away
                and brc_status == "WAIT FOR BREAK"
                and break_distance_atr is not None
            ):
                status = "WATCH"
                note = (
                    "HTF αντίδραση — H1 break μακριά "
                    f"({break_distance_atr:.1f} ATR)"
                )
            elif evidence_count >= 2 and moved_away:
                status = "WATCH"
                note = "HTF αντίδραση — δεν υπάρχει ακόμη έγκυρο κοντινό H1 break"
            else:
                status = "WATCH"
                note = "D1 zone υπό παρακολούθηση"

            entry, stop, target, rr, rr_pass = calculate_reversal_trade_plan(
                direction, brc_status, h1, h4, d1, float(zone)
            )
            if brc_status == "READY":
                if rr_pass:
                    status = "READY"
                    note = f"Fresh H1 confirmation και RR ≥ {REVERSAL_MIN_RR:.1f}"
                else:
                    status = "INVALID"
                    note = f"H1 confirmation αλλά RR < {REVERSAL_MIN_RR:.1f}"

            evaluations.append(
                ReversalScan(
                    direction=direction,
                    status=status,
                    score=round(min(score, 100.0), 1),
                    htf_zone=float(zone),
                    zone_kind=zone_kind,
                    sweep=sweep,
                    rejection=rejection,
                    displacement=displacement,
                    h4_structure=h4_structure,
                    brc_status=brc_status,
                    h1_zone=h1_zone,
                    entry=entry,
                    stop_loss=stop,
                    take_profit=target,
                    rr=rr,
                    rr_pass=rr_pass,
                    note=note,
                )
            )

    if not evaluations:
        return result

    status_priority = {
        "READY": 5,
        "WAIT RETEST": 4,
        "ARMED": 3,
        "WATCH": 2,
        "INVALID": 1,
    }
    return max(
        evaluations,
        key=lambda item: (status_priority.get(item.status, 0), item.score),
    )


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

    # TradingView ratings contribute only as directional corroboration.
    sign = 1.0 if direction == "LONG" else -1.0
    valid_ratings = [max(0.0, sign * v) for v in ratings if v is not None]
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
        "WAIT FOR BREAK": 0,
        "BREAK": 6,
        "RETEST": 12,
        "READY": 20,
        "WAIT NEW RETEST": 0,
    }.get(brc_status, 0)

    raw_score = min(rating_score + ema_score + adx_score + structure_score + brc_score, 100)

    # Stage-aware readiness cap: strong HTF/context must not make an incomplete
    # Break -> Retest -> Confirmation setup look trade-ready.
    stage_cap = {
        "WAIT": 55.0,
        "WAIT FOR BREAK": 55.0,
        "BREAK": 65.0,
        "RETEST": 85.0,
        "READY": 100.0,
        "WAIT NEW RETEST": 55.0,
    }.get(brc_status, 55.0)

    return round(min(raw_score, stage_cap), 1)


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


def oanda_prescreen_from_row(row) -> Optional[OandaPreScreen]:
    """
    First-stage SHORTLIST only. This is an OANDA TradingView Screener snapshot.
    H1 timestamp is displayed as context, but there is NO full OHLC
    or Break/Retest/Confirmation validation in this first-stage ranking.
    Never infer a trading entry from this function.
    """
    symbol = str(row.get("Symbol", ""))
    if not symbol.startswith("OANDA:"):
        return None
    d1 = safe_float(row.get("Technical Rating"))
    h4 = safe_float(row.get("Recommend All|240"))
    h1 = safe_float(row.get("Recommend All|60"))
    if any(rating is None for rating in (d1, h4, h1)):
        return None
    if d1 > DIRECTION_LEVEL and h4 > DIRECTION_LEVEL and h1 >= -DIRECTION_LEVEL:
        direction, sign = "LONG", 1
    elif d1 < -DIRECTION_LEVEL and h4 < -DIRECTION_LEVEL and h1 <= DIRECTION_LEVEL:
        direction, sign = "SHORT", -1
    else:
        return None

    price = safe_float(row.get("Price"))
    ema_checked = 0
    ema_passes = 0
    d1_h4_ema = []
    for label, previous in (
        ("EMA50 D1", "EMA50 D1 Prev"),
        ("EMA50 H4", "EMA50 H4 Prev"),
        ("EMA50 H1", "EMA50 H1 Prev"),
    ):
        ema = safe_float(row.get(label))
        prev = safe_float(row.get(previous))
        if price is None or ema is None or prev is None:
            d1_h4_ema.append(None)
            continue
        checked = ema_frame_ok(direction, price, ema, prev)
        ema_checked += 1
        ema_passes += int(checked)
        d1_h4_ema.append(checked)

    # Reject chart contexts where the available D1/H4 EMA clearly opposes
    # direction. Missing EMA is reported, never silently marked as passed.
    if d1_h4_ema[0] is False or d1_h4_ema[1] is False:
        return None

    adx_h4 = safe_float(row.get("ADX H4"))
    adx_h1 = safe_float(row.get("ADX H1"))
    if adx_h4 is not None and adx_h4 < ADX_MIN:
        return None

    # Deterministic ranking of CONTEXT, not a probability or READY score.
    rating_points = (
        min(max(sign * d1, 0.0), 1.0) * 35
        + min(max(sign * h4, 0.0), 1.0) * 30
        + min(max(sign * h1, 0.0), 1.0) * 10
    )
    ema_points = 15 * ema_passes / 3
    adx_points = min(max((adx_h4 or 0) / 40, 0.0), 1.0) * 10
    return OandaPreScreen(
        direction=direction,
        score=round(rating_points + ema_points + adx_points, 1),
        price=price,
        ema_passes=ema_passes,
        ema_checked=ema_checked,
        adx_h4=adx_h4,
        adx_h1=adx_h1,
        oanda_prev_h1_open=safe_float(row.get("OANDA Previous H1 Open")),
        oanda_h1_update=safe_float(row.get("Last Bar Update Time|60")),
    )


def oanda_shortlist(results: list[PairScan], limit: int = 5) -> list[PairScan]:
    """Up to five OANDA chart-review candidates, independent of Yahoo OHLC."""
    eligible = [r for r in results if r.oanda_prescreen is not None]
    eligible.sort(
        key=lambda r: (
            -r.oanda_prescreen.score,
            -r.oanda_prescreen.ema_passes,
            r.pair,
        )
    )
    return eligible[:limit]


def oanda_timestamp_label(value: Optional[float]) -> str:
    if value is None:
        return "—"
    try:
        return pd.to_datetime(value, unit="s", utc=True).tz_convert(
            "Europe/Athens"
        ).strftime("%d/%m %H:%M")
    except (ValueError, TypeError, OverflowError):
        return "—"


def oanda_ref_status(value: Optional[float]) -> str:
    if value is None:
        return "NO TIME"
    try:
        age = pd.Timestamp.now(tz="UTC") - pd.to_datetime(value, unit="s", utc=True)
        if age < -pd.Timedelta(minutes=2) or age > pd.Timedelta(hours=4):
            return "STALE"
        return "RECENT"
    except (ValueError, TypeError, OverflowError):
        return "NO TIME"


def write_oanda_shortlist(results: list[PairScan], path: str = "OANDA_SHORTLIST.md") -> None:
    now = datetime.now(ZoneInfo("Europe/Athens"))
    top = oanda_shortlist(results)
    lines = [
        "# OANDA — Top 5 προς έλεγχο",
        "",
        f"**Δημιουργήθηκε:** {now:%d/%m/%Y %H:%M} (ώρα Ελλάδας)",
        "",
        f"**Υποψήφια:** {len(top)} από {len(results)} ζευγάρια",
        "",
        "> **ΜΟΝΟ ΑΡΧΙΚΟ ΦΙΛΤΡΟ — ΟΧΙ ΣΗΜΑ ΕΙΣΟΔΟΥ.**",
        "> Πηγή: TradingView Forex Screener, αποκλειστικά σύμβολα OANDA. "
        "Εμφανίζεται η ώρα του προηγούμενου OANDA H1 και ο έλεγχος "
        "παλαιότητας του feed. Αυτό δεν επαληθεύει όλο το OHLC ιστορικό. "
        "EMA50/ADX εμφανίζονται μόνο αν επιστράφηκαν από το screener.",
        "> Ο δείκτης κατάταξης (/100) δεν είναι πιθανότητα επιτυχίας, "
        "BRC confirmation ή READY.",
        "",
        "| # | Ζευγάρι | Κατεύθυνση ελέγχου | Ranking /100 | W1 | D1 | H4 | H1 | EMA50 TV | ADX H4 | ADX H1 | Προηγούμενο H1 OANDA (Αθήνα) | OANDA update |",
        "|---:|---|---|---:|---|---|---|---|---|---:|---:|---|---|",
    ]
    for i, r in enumerate(top, 1):
        preview = r.oanda_prescreen
        lines.append(
            f"| {i} | **{r.pair}** | {preview.direction} (WATCH ONLY) | "
            f"{preview.score:.1f} | {rating_text(r.w1_rating)} | "
            f"{rating_text(r.d1_rating)} | {rating_text(r.h4_rating)} | "
            f"{rating_text(r.h1_rating)} | {preview.ema_passes}/{preview.ema_checked} verified fields | "
            f"{fmt_num(preview.adx_h4)} | {fmt_num(preview.adx_h1)} | "
            f"{oanda_timestamp_label(preview.oanda_prev_h1_open)} | "
            f"{oanda_ref_status(preview.oanda_h1_update)} |"
        )
    if not top:
        lines.append("| — | Καμία επαρκώς συμφωνημένη ένδειξη OANDA ή μη διαθέσιμα δεδομένα | — | — | — | — | — | — | — | — | — | — | — |")
    lines += [
        "",
        "Η λίστα είναι υποψήφια για χειροκίνητο τελικό έλεγχο μόνο αυτών των γραφημάτων. "
        "Δεν προκύπτουν Entry/SL/TP χωρίς ανεξάρτητη επιβεβαίωση πραγματικών OHLC, "
        "BRC, spread και ειδήσεων.",
        "Κατά το Σαββατοκύριακο οι Forex ενδείξεις μπορεί να αντανακλούν το κλείσιμο της Παρασκευής.",
    ]
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


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

        # TradingView ratings are retained as context only. Trend, EMA50, ADX,
        # BRC, price and zones are evaluated from one completed Yahoo OHLC feed.
        w1 = safe_float(row.get("Recommend All|1W"))
        d1 = safe_float(row.get("Technical Rating"))
        h4 = safe_float(row.get("Recommend All|240"))
        h1 = safe_float(row.get("Recommend All|60"))
        oanda_preview = oanda_prescreen_from_row(row)
        print(
            f"[OANDA-REF] {pair} | H1={row.get('Close|60')} "
            f"| H1-start={row.get('Time|60')} "
            f"| H1-update={row.get('Last Bar Update Time|60')} "
            f"| Prev-H1={row.get('OANDA Previous H1 Close')} "
            f"| Prev-H1-start={row.get('OANDA Previous H1 Open')}"
        )
        price = None
        direction = "—"
        bias = "NO DATA"
        ema_passes = 0
        adx_h4 = None
        adx_h1 = None

        d1_structure = "N/A"
        h4_structure = "N/A"
        brc_status = "WAIT"
        zone = None
        candle_status = "N/A"
        entry = None
        stop_loss = None
        take_profit = None
        rr = None
        rr_pass = False
        reversal = None
        h1_closed_at = None

        candle_history = fetch_candle_history(pair)
        if candle_history is not None:
            h1_candles, h4_candles, d1_candles = candle_history
            if not h1_candles.empty:
                h1_closed_at = h1_candles.index[-1]
                last_close_time = pd.Timestamp(h1_closed_at)
                if last_close_time.tzinfo is None:
                    last_close_time = last_close_time.tz_localize("UTC")
                else:
                    last_close_time = last_close_time.tz_convert("UTC")
                last_close_time += pd.Timedelta(hours=1)
                data_age = pd.Timestamp.now(tz="UTC") - last_close_time

                candle_status = "YF"
                if data_age < pd.Timedelta(0) or data_age > pd.Timedelta(hours=MAX_H1_DATA_AGE_HOURS):
                    print(
                        f"[WARNING] {pair}: stale Yahoo candle "
                        f"({data_age.total_seconds()/3600:.1f}h old); signals suppressed"
                    )
                    # Never publish a trading direction, BRC, quality score or
                    # reversal from old (or future-dated) Yahoo bars. Keep only
                    # the candle timestamp so the problem can be diagnosed.
                    return PairScan(
                        pair=pair, symbol=symbol, provider=provider,
                        direction="—", bias="STALE DATA",
                        d1_rating=d1, h4_rating=h4, h1_rating=h1, price=None,
                        ema_passes=0, ema_total=3, adx_h4=None, adx_h1=None,
                        d1_structure="N/A", h4_structure="N/A",
                        brc_status="WAIT", zone=None, quality_score=0.0,
                        setup_grade="—", candles="YF-STALE", entry=None,
                        stop_loss=None, take_profit=None, rr=None, rr_pass=False,
                        reversal=None, w1_rating=w1, h1_closed_at=h1_closed_at,
                        oanda_prescreen=oanda_preview,
                    )

                verification = verify_h1_history(pair, h1_candles, row)
                if not verification.ok:
                    print(f"[DATA-REJECT] {pair}: {verification.status} — {verification.detail}")
                    return PairScan(
                        pair=pair, symbol=symbol, provider=provider,
                        direction="—", bias="UNVERIFIED DATA",
                        d1_rating=d1, h4_rating=h4, h1_rating=h1, price=None,
                        ema_passes=0, ema_total=3, adx_h4=None, adx_h1=None,
                        d1_structure="N/A", h4_structure="N/A",
                        brc_status="WAIT", zone=None, quality_score=0.0,
                        setup_grade="—", candles=verification.status, entry=None,
                        stop_loss=None, take_profit=None, rr=None, rr_pass=False,
                        reversal=None, w1_rating=w1, h1_closed_at=h1_closed_at,
                        oanda_prescreen=oanda_preview,
                    )
                # The checked previous H1 open is our safe candle boundary.
                prepared = prepare_candle_history(verification.h1)
                if prepared is None:
                    print(f"[DATA-REJECT] {pair}: insufficient checked OHLC history")
                    return PairScan(
                        pair=pair, symbol=symbol, provider=provider,
                        direction="—", bias="UNVERIFIED DATA",
                        d1_rating=d1, h4_rating=h4, h1_rating=h1, price=None,
                        ema_passes=0, ema_total=3, adx_h4=None, adx_h1=None,
                        d1_structure="N/A", h4_structure="N/A",
                        brc_status="WAIT", zone=None, quality_score=0.0,
                        setup_grade="—", candles="NO-VERIFIED-HISTORY",
                        entry=None, stop_loss=None, take_profit=None,
                        rr=None, rr_pass=False, reversal=None, w1_rating=w1,
                        h1_closed_at=h1_closed_at, oanda_prescreen=oanda_preview,
                    )
                h1_candles, h4_candles, d1_candles = prepared
                h1_closed_at = h1_candles.index[-1]
                candle_status = verification.status
                print(
                    f"[DATA-VERIFIED] {pair}: last={h1_closed_at} "
                    f"| source=Yahoo OHLC + OANDA H1 close "
                    f"| delta={verification.difference_pips:.1f} pips"
                )
                price = safe_float(h1_candles["Close"].iloc[-1])
                signals = [
                    ema_frame_signal(d1_candles),
                    ema_frame_signal(h4_candles),
                    ema_frame_signal(h1_candles),
                ]
                # D1 establishes direction, H4 must agree, and H1 is the timing
                # filter. A missing or mixed D1/H4 context cannot create a trend.
                if signals[0] in {"LONG", "SHORT"} and signals[0] == signals[1]:
                    direction = signals[0]
                    ema_passes = sum(signal == direction for signal in signals)
                    bias = "ALIGNED" if ema_passes == 3 else "MIXED"
                else:
                    direction = "—"
                    ema_passes = 0
                    bias = "MIXED" if all(signal is not None for signal in signals[:2]) else "NO DATA"

                adx_h4 = calculate_adx(h4_candles)
                adx_h1 = calculate_adx(h1_candles)

                if direction in {"LONG", "SHORT"}:
                    d1_structure = detect_structure(d1_candles)
                    h4_structure = detect_structure(h4_candles)
                    brc_status, zone = detect_brc(direction, h1_candles)
                    entry, stop_loss, take_profit, rr, rr_pass = calculate_trade_plan(
                        direction, brc_status, zone, h1_candles, h4_candles
                    )

                if ENABLE_HTF_REVERSAL:
                    try:
                        reversal = analyze_htf_reversal(
                            h1_candles, h4_candles, d1_candles
                        )
                    except Exception as exc:
                        print(f"[WARN] {pair} reversal: {exc}")
                        reversal = ReversalScan(note="Reversal analysis error")

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
            reversal=reversal,
            w1_rating=w1,
            h1_closed_at=h1_closed_at,
            oanda_prescreen=oanda_preview,
        )

    except Exception as exc:
        print(f"[WARN] {pair}: {exc}")
        return PairScan(
            pair, "", "", "—", "ERROR", None, None, None, None,
            0, 3, None, None, "N/A", "N/A", "WAIT", None, 0.0, "—", "ERROR",
            None, None, None, None, False
        )

def scan_all_pairs() -> list[PairScan]:
    if ENABLE_HTF_REVERSAL:
        print("Προφόρτωση H1 candles για το HTF Reversal mode...")
        prefetch_candle_histories(PAIRS)

    results = []
    for index, pair in enumerate(PAIRS, start=1):
        print(f"[{index:02d}/{len(PAIRS)}] Scan {pair}...")
        results.append(scan_pair(pair))
        time.sleep(0.15)
    return results


def scan_crypto_asset(asset: str) -> CryptoScan:
    try:
        row = fetch_crypto(asset)
        if row is None:
            return CryptoScan(asset, "", "", None, None, None, None, None, "—", "NO DATA")

        symbol = str(row.get("Symbol", ""))
        provider = symbol.split(":", 1)[0] if ":" in symbol else ""
        w1 = safe_float(row.get("Recommend All|1W"))
        d1 = safe_float(row.get("Technical Rating"))
        h4 = safe_float(row.get("Recommend All|240"))
        h1 = safe_float(row.get("Recommend All|60"))
        price = safe_float(row.get("Price"))
        direction, bias = classify_alignment(d1, h4, h1)
        return CryptoScan(asset, symbol, provider, price, w1, d1, h4, h1, direction, bias)
    except Exception as exc:
        print(f"[WARN] {asset} crypto: {exc}")
        return CryptoScan(asset, "", "", None, None, None, None, None, "—", "ERROR")


def scan_all_crypto() -> list[CryptoScan]:
    results = []
    for asset in CRYPTO_ASSETS:
        print(f"[CRYPTO] Scan {asset}...")
        results.append(scan_crypto_asset(asset))
        time.sleep(0.15)
    return results


def weekly_context(direction: str, w1: Optional[float]) -> str:
    if w1 is None:
        return "N/A"
    if direction == "LONG":
        if w1 > DIRECTION_LEVEL:
            return "✅ SUPPORTS"
        if w1 < -DIRECTION_LEVEL:
            return "⚠️ OPPOSES"
    elif direction == "SHORT":
        if w1 < -DIRECTION_LEVEL:
            return "✅ SUPPORTS"
        if w1 > DIRECTION_LEVEL:
            return "⚠️ OPPOSES"
    return "NEUTRAL"


def candidates(results: list[PairScan]) -> list[PairScan]:
    selected = [r for r in results if r.direction in {"LONG", "SHORT"} and r.candles == "YF+OANDA-H1"]
    priority = {"A+ READY": 0, "A": 1, "WATCH": 2, "—": 3}
    selected.sort(key=lambda r: (priority.get(r.setup_grade, 9), -r.quality_score, r.pair))
    return selected


def weekly_trend_watchlist(
    results: list[PairScan], now: datetime, state_path: str = WEEKLY_TOP5_PATH
) -> tuple[list[PairScan], list[PairScan], str]:
    """Persist the Trend watchlist across scans, resetting on Monday in Athens."""
    week = f"{now.isocalendar().year}-W{now.isocalendar().week:02d}"
    ranked = candidates(results)
    by_pair = {r.pair: r for r in ranked}
    state_file = Path(state_path)
    saved_state = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {}
    state = saved_state
    if state.get("week") != week:
        state = {"week": week, "top5": [r.pair for r in ranked[:5]], "hot_new": []}

    top_pairs = [p for p in state["top5"] if p in by_pair]
    for r in ranked:
        if len(top_pairs) >= 5:
            break
        if r.pair not in top_pairs:
            top_pairs.append(r.pair)
    # Only a confirmed, tradable new setup may displace a weekly pick.
    for r in ranked:
        if r.pair in top_pairs or r.brc_status != "READY" or r.setup_grade not in {"A+ READY", "A"}:
            continue
        if len(top_pairs) < 5:
            top_pairs.append(r.pair)
        else:
            replaceable = [p for p in top_pairs if by_pair[p].setup_grade != "A+ READY"]
            if replaceable:
                weakest = min(replaceable, key=lambda p: by_pair[p].quality_score)
                top_pairs[top_pairs.index(weakest)] = r.pair

    # Rebuild from THIS scan; never carry a formerly strong pair forward
    # after its score, structure or feed quality has deteriorated.
    hot_pairs = []
    for r in ranked:
        if r.pair in top_pairs or r.pair in hot_pairs:
            continue
        strong_context = (r.quality_score >= HOT_NEW_MIN_SCORE and r.ema_passes >= 2
                          and structure_matches(r.direction, r.d1_structure)
                          and structure_matches(r.direction, r.h4_structure))
        if strong_context or r.setup_grade in {"A+ READY", "A"}:
            hot_pairs.append(r.pair)

    next_state = {"week": week, "top5": top_pairs, "hot_new": hot_pairs}
    if saved_state != next_state:
        state_file.write_text(json.dumps(next_state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return [by_pair[p] for p in top_pairs], [by_pair[p] for p in hot_pairs], week


def trend_state(r: PairScan) -> str:
    if r.setup_grade == "A+ READY":
        return "🟢 ENTRY READY"
    if r.direction not in {"LONG", "SHORT"} or r.candles != "YF+OANDA-H1":
        return "🔴 INVALID"
    if r.brc_status in {"RETEST", "READY"} or r.setup_grade == "A":
        return "🟡 WATCH"
    return "⚪ WAIT"


def reversal_candidates(results: list[PairScan]) -> list[PairScan]:
    if not ENABLE_HTF_REVERSAL:
        return []

    selected = [
        r for r in results
        if r.reversal is not None
        and r.reversal.direction in {"LONG", "SHORT"}
        and r.reversal.status in {"READY", "WAIT RETEST", "ARMED"}
        and r.reversal.score >= REVERSAL_MIN_ACTIVE_SCORE
    ]
    priority = {
        "READY": 0,
        "WAIT RETEST": 1,
        "ARMED": 2,
        "WATCH": 3,
        "INVALID": 4,
    }
    selected.sort(
        key=lambda r: (
            priority.get(r.reversal.status, 9),
            -r.reversal.score,
            r.pair,
        )
    )
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


def fmt_zone_distance(pair: str, price: Optional[float], zone: Optional[float]) -> str:
    """Signed distance from the H1 BRC zone using the TradingView price."""
    if price is None or zone is None:
        return "—"
    pip_size = 0.01 if pair.endswith("JPY") else 0.0001
    distance = (price - zone) / pip_size
    return f"{distance:+.1f} pips"


def fmt_h1_closed_at(value) -> str:
    """Format the source timestamp of the last completed H1 candle in Athens time."""
    if value is None:
        return "—"
    timestamp = pd.Timestamp(value)
    if timestamp.tzinfo is None:
        timestamp = timestamp.tz_localize("UTC")
    start = timestamp.tz_convert("Europe/Athens")
    end = (timestamp + pd.Timedelta(hours=1)).tz_convert("Europe/Athens")
    end_label = end.strftime("%d/%m %H:%M") if end.date() != start.date() else end.strftime("%H:%M")
    return f"{start:%d/%m %H:%M}–{end_label}"


def reversal_display_state(rev: ReversalScan) -> str:
    """Explain what the internal ARMED state is waiting for."""
    if rev.status == "ARMED" and rev.brc_status == "RETEST":
        return "ΑΝΑΜΟΝΗ H1 ΕΠΙΒΕΒΑΙΩΣΗΣ"
    if rev.status == "ARMED" and rev.brc_status == "WAIT FOR BREAK":
        return "ARMED · ΑΝΑΜΟΝΗ BREAK"
    return rev.status


def fmt_rr(value: Optional[float], passed: bool) -> str:
    if value is None:
        return "—"
    mark = "✅" if passed else "❌"
    return f"{value:.2f} {mark}"


def fmt_check(value: bool) -> str:
    return "✅" if value else "—"


def write_markdown(
    results: list[PairScan],
    crypto_results: Optional[list[CryptoScan]] = None,
    path: str = "LATEST_FOREX_SCAN.md",
) -> None:
    now = datetime.now(ZoneInfo("Europe/Athens"))
    write_oanda_shortlist(results, str(Path(path).with_name("OANDA_SHORTLIST.md")))
    crypto_results = crypto_results or []
    top = candidates(results)
    weekly, hot_new, week = weekly_trend_watchlist(
        results, now, str(Path(path).with_name(WEEKLY_TOP5_PATH))
    )
    ready = [r for r in top if r.setup_grade == "A+ READY"]
    reversals = reversal_candidates(results)
    reversal_ready = [
        r for r in reversals
        if r.reversal is not None and r.reversal.status == "READY"
    ]

    lines = [
        "# Latest Forex Scan",
        "",
        f"**Τελευταία ενημέρωση:** {now:%d/%m/%Y %H:%M} (Europe/Athens)",
        "",
        f"**Pairs:** {len(results)}  |  **Aligned:** {len(top)}  |  **A+ READY:** {len(ready)}",
        "",
        f"**HTF Reversal mode:** {'ON' if ENABLE_HTF_REVERSAL else 'OFF'}"
        f"  |  **Candidates:** {len(reversals)}  |  **READY:** {len(reversal_ready)}",
        "",
        "> Το score δείχνει συμφωνία των φίλτρων (/100), **όχι πιθανότητα κέρδους ή επιτυχίας**. Τιμή, EMA50, ADX, δομή, BRC και zones βασίζονται στα ίδια κλεισμένα κεριά Yahoo Finance.",
        "",
        "> Τα TradingView ratings είναι μόνο συμπληρωματικό context και δεν καθορίζουν READY. EMA50, ADX, structure, BRC, entry και zone υπολογίζονται από το ίδιο feed OHLC.",
        "> **Δεδομένα:** τα Yahoo OHLC χρησιμοποιούνται για υπολογισμούς μόνο όταν η ώρα και το close του ίδιου κλεισμένου H1 συμφωνούν με ανεξάρτητη αναφορά OANDA (έως 8 pips). Δεν σημαίνει ταύτιση ολόκληρου του ιστορικού.", 
        "> Τα D1/H4 σχηματίζονται πλέον σε συνεδρίες Νέας Υόρκης 17:00, με αποκλεισμό των κλειστών ωρών Σαββατοκύριακου. Απαιτείται ακόμη ξεχωριστός έλεγχος ολόκληρου του ιστορικού OHLC.",
        "> Στους πίνακες, η τιμή είναι το close του τελευταίου επαληθευμένου κλεισμένου H1. Δ zone = close μείον H1 zone σε pips (+ πάνω από τη zone, − κάτω από τη zone).",
        "",
        f"> **W1 / Weekly:** χρησιμοποιείται ως ανώτερο context και εμφανίζεται στο scan. **Δεν αλλάζει** το A+ rule: D1/H4/H1 alignment + EMA50 3/3 + D1/H4 structure + ADX + **confirmation ηλικίας έως {MAX_CONFIRMED_SETUP_AGE_BARS} κλεισμένων H1 κεριών**, χωρίς ακύρωση ή υπερβολική απόσταση από τη zone + **RR ≥ 1.2**.",
        "",
        "## 🟢 ENTRY READY — Trend",
        "",
    ]
    verified_pairs = [r.pair for r in results if r.candles == "YF+OANDA-H1"]
    rejected_pairs = [(r.pair, r.candles) for r in results
                      if r.candles != "YF+OANDA-H1"]
    lines += [
        "",
        f"> **Πηγές δεδομένων:** Yahoo OHLC + OANDA H1 διασταύρωση. "
        f"Επαληθευμένα: {len(verified_pairs)}/{len(results)} · "
        f"Απορρίφθηκαν: {len(rejected_pairs)}. "
        "Για πλήρη εικόνα δες τους λόγους απόρριψης παρακάτω.",
        "",
    ]
    if rejected_pairs:
        lines += [
            "| Ζευγάρι | Κατάσταση πηγής |",
            "|---|---|",
        ]
        for rejected_pair, reason in rejected_pairs:
            lines.append(f"| {rejected_pair} | {reason} |")
        lines.append("")
    stale_pairs = [r.pair for r in results if r.candles == "YF-STALE"]
    if stale_pairs:
        lines += [
            "",
            f"> ⚠️ YF-STALE: {len(stale_pairs)} ζευγάρια ({', '.join(stale_pairs)}) έχουν μη έγκυρο/παλιό κλεισμένο H1 (όριο {MAX_H1_DATA_AGE_HOURS} ώρες). Δεν παράγονται σήματα από παλιά δεδομένα.",
            "",
        ]

    if ready:
        for r in ready:
            lines.append(
                f"**{r.pair} {r.direction} · Agreement score {r.quality_score:.1f}/100 · "
                f"H1 zone {fmt_zone(r.zone)} · Entry {fmt_price(r.pair, r.entry)} · "
                f"SL {fmt_price(r.pair, r.stop_loss)} · TP {fmt_price(r.pair, r.take_profit)} · "
                f"RR {fmt_rr(r.rr, r.rr_pass)}**"
            )
    else:
        lines.append("Κανένα A+ READY στο τρέχον scan.")

    lines += [
        "",
        "> Η ένδειξη απαιτεί έλεγχο στο τρέχον chart, spread, ειδήσεων και μεγέθους θέσης πριν από οποιαδήποτε είσοδο.",
        "",
        "## OANDA — αυτόματο πρώτο φίλτρο (έως 5 ζευγάρια)",
        "",
        f"**{len(oanda_shortlist(results))} ζευγάρια προς έλεγχο** — "
        "δες το [OANDA_SHORTLIST.md](OANDA_SHORTLIST.md). "
        "Μόνο ενδείξεις TradingView OANDA, χωρίς BRC/READY. "
        "Το report εμφανίζει H1 OANDA timestamps, αλλά δεν έχει επιβεβαιωμένο πλήρες OHLC ιστορικό.",
        "",
        f"## Weekly Top 5 — {week} (Europe/Athens)",
        "",
        "Η πεντάδα διατηρείται όλη την εβδομάδα· ανανεώνονται score και κατάσταση σε κάθε scan. "
        "Μόνο νέο επιβεβαιωμένο setup με RR ≥ 1.2 μπορεί να αντικαταστήσει θέση. "
        "Νέα επιλογή γίνεται τη Δευτέρα (ώρα Ελλάδας).",
        "",
        "| # | Pair | Dir | Agreement /100 | Κατάσταση | B→R→C | H1 Zone | Τιμή | Απόσταση zone | Κλεισμένο H1 (ώρα Αθήνας) | RR |",
        "|---:|---|---|---:|---|---|---:|---:|---:|---|---:|",
    ]
    for i, r in enumerate(weekly, start=1):
        lines.append(
            f"| {i} | **{r.pair}** | {r.direction} | **{r.quality_score:.1f}/100** | "
            f"**{trend_state(r)}** | {r.brc_status} | {fmt_zone(r.zone)} | "
            f"{fmt_price(r.pair, r.price)} | {fmt_zone_distance(r.pair, r.price, r.zone)} | "
            f"{fmt_h1_closed_at(r.h1_closed_at)} | {fmt_rr(r.rr, r.rr_pass)} |"
        )
    if not weekly:
        lines.append("| — | Δεν υπάρχουν επαρκή δεδομένα για εβδομαδιαία επιλογή | — | — | — | — | — | — | — | — | — |")

    lines += [
        "",
        "## Νέοι υποψήφιοι για παρακολούθηση — Trend",
        "",
        f"Νέα ζευγάρια εκτός πεντάδας με agreement score ≥ {HOT_NEW_MIN_SCORE:.0f}/100 "
        "και D1/H4 structure + EMA50 ή setup A/A+. Είναι υποψήφια για παρακολούθηση, "
        "όχι σήματα εισόδου· είσοδος εξετάζεται μόνο σε ENTRY READY.", 
        "",
    ]
    if hot_new:
        lines += [
            "| Pair | Dir | Agreement /100 | Κατάσταση | B→R→C | H1 Zone | Τιμή | Απόσταση zone | Κλεισμένο H1 (ώρα Αθήνας) |",
            "|---|---|---:|---|---|---:|---:|---:|---|",
        ]
        for r in hot_new:
            lines.append(
                f"| **{r.pair}** | {r.direction} | **{r.quality_score:.1f}/100** | "
                f"**{trend_state(r)}** | {r.brc_status} | {fmt_zone(r.zone)} | "
                f"{fmt_price(r.pair, r.price)} | {fmt_zone_distance(r.pair, r.price, r.zone)} | "
                f"{fmt_h1_closed_at(r.h1_closed_at)} |"
            )
    else:
        lines.append("Κανένα νέο ζευγάρι που να περνά τα κριτήρια.")

    lines += [
        "",
        "> **Agreement score /100 = βαθμός συμφωνίας φίλτρων, όχι πιθανότητα επιτυχίας.** "
        "🔴 INVALID σημαίνει ότι χάθηκε το alignment ή δεν υπάρχουν αξιόπιστα δεδομένα στο τρέχον scan.",
        "",
        "## Όλοι οι τρέχοντες Trend candidates",
        "",
    ]

    if top:
        lines += [
            "| # | Pair | Dir | Setup | Bias | EMA50 | D1 Struct | H4 Struct | ADX H4 | ADX H1 | B→R→C | H1 Zone | Τιμή | Δ zone | Κλεισμένο H1 (ώρα Αθήνας) | Entry | SL | TP | RR | Agreement /100 |",
            "|---:|---|---|---|---|---:|---|---|---:|---:|---|---:|---:|---:|---|---:|---:|---:|---:|---:|",
        ]
        for i, r in enumerate(top, start=1):
            lines.append(
                f"| {i} | **{r.pair}** | {r.direction} | **{r.setup_grade}** | {r.bias} | "
                f"{r.ema_passes}/3 | {r.d1_structure} | {r.h4_structure} | "
                f"{fmt_num(r.adx_h4)} | {fmt_num(r.adx_h1)} | **{r.brc_status}** | "
                f"{fmt_zone(r.zone)} | {fmt_price(r.pair, r.price)} | "
                f"{fmt_zone_distance(r.pair, r.price, r.zone)} | {fmt_h1_closed_at(r.h1_closed_at)} | "
                f"{fmt_price(r.pair, r.entry)} | {fmt_price(r.pair, r.stop_loss)} | "
                f"{fmt_price(r.pair, r.take_profit)} | **{fmt_rr(r.rr, r.rr_pass)}** | "
                f"**{r.quality_score:.1f}/100** |"
            )
    else:
        lines.append("Δεν βρέθηκε αυτή τη στιγμή D1 + H4 + H1 alignment.")

    lines += [
        "",
        "### Rating detail",
        "",
        "| Pair | W1 | D1 | H4 | H1 | Direction |",
        "|---|---|---|---|---|---|",
    ]
    for r in top:
        lines.append(
            f"| {r.pair} | {rating_text(r.w1_rating)} | {rating_text(r.d1_rating)} | "
            f"{rating_text(r.h4_rating)} | {rating_text(r.h1_rating)} | {r.direction} |"
        )

    lines += [
        "",
        "## Crypto Watch — BTC / ETH / SOL",
        "",
        "> Crypto δεδομένα από TradingView Crypto Screener. Το W1 είναι context· η κατεύθυνση εξακολουθεί να απαιτεί D1/H4/H1 alignment.",
        "",
        "| Asset | Market | Price | W1 | D1 | H4 | H1 | Direction | W1 Context |",
        "|---|---|---:|---|---|---|---|---|---|",
    ]
    if crypto_results:
        for c in crypto_results:
            market = c.symbol or "—"
            price_text = "—" if c.price is None else (f"{c.price:,.2f}" if c.price >= 100 else f"{c.price:,.4f}")
            lines.append(
                f"| **{c.asset}** | {market} | {price_text} | {rating_text(c.w1_rating)} | "
                f"{rating_text(c.d1_rating)} | {rating_text(c.h4_rating)} | {rating_text(c.h1_rating)} | "
                f"**{c.direction}** | {weekly_context(c.direction, c.w1_rating)} |"
            )
    else:
        lines.append("| — | — | — | — | — | — | — | — | — |")

    lines += [
        "",
        "## HTF Reversal — ξεχωριστό mode",
        "",
        f"> Δεν αναμειγνύεται με το A+ Trend. Ψάχνει D1 support/resistance → H4 sweep/rejection/displacement → H1 break/retest/confirmation. Πριν από το break, ένα setup γίνεται **ARMED** μόνο όταν το H1 break απέχει έως **{REVERSAL_MAX_ARMED_BREAK_DISTANCE_ATR:.1f}× H1 ATR**. Το shortlist κρατά μόνο ενεργά contexts με **score ≥ {REVERSAL_MIN_ACTIVE_SCORE:.0f}**. Το **READY** απαιτεί φυσικό D1 target με **RR ≥ 3.0**.",
        "> **Το HTF Reversal Score μετρά συμφωνία context (/100), όχι πιθανότητα κέρδους. ΑΝΑΜΟΝΗ H1 ΕΠΙΒΕΒΑΙΩΣΗΣ / WAIT RETEST / ARMED δεν είναι είσοδος. Entry/SL/TP εμφανίζονται μόνο σε READY, με RR ≥ 3.0.**",
        "",
    ]

    if not ENABLE_HTF_REVERSAL:
        lines.append("Το mode είναι απενεργοποιημένο (`ENABLE_HTF_REVERSAL=false`).")
    elif reversals:
        lines += [
            "| # | Pair | Dir | State | D1 Zone | H4 Struct | Sweep | Reject | Displ. | H1 BRC | H1 Zone | Τιμή | Δ H1 zone | Κλεισμένο H1 (ώρα Αθήνας) | Entry | SL | TP | RR | Context score /100 | Σημείωση |",
            "|---:|---|---|---|---:|---|---:|---:|---:|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|",
        ]
        for i, pair_scan in enumerate(reversals, start=1):
            rev = pair_scan.reversal
            lines.append(
                f"| {i} | **{pair_scan.pair}** | {rev.direction} | **{reversal_display_state(rev)}** | "
                f"{fmt_zone(rev.htf_zone)} | {rev.h4_structure} | {fmt_check(rev.sweep)} | "
                f"{fmt_check(rev.rejection)} | {fmt_check(rev.displacement)} | "
                f"{rev.brc_status} | {fmt_zone(rev.h1_zone)} | "
                f"{fmt_price(pair_scan.pair, pair_scan.price)} | "
                f"{fmt_zone_distance(pair_scan.pair, pair_scan.price, rev.h1_zone)} | "
                f"{fmt_h1_closed_at(pair_scan.h1_closed_at)} | "
                f"{fmt_price(pair_scan.pair, rev.entry)} | "
                f"{fmt_price(pair_scan.pair, rev.stop_loss)} | "
                f"{fmt_price(pair_scan.pair, rev.take_profit)} | "
                f"{fmt_rr(rev.rr, rev.rr_pass)} | **{rev.score:.1f}/100** | {rev.note} |"
            )
    else:
        lines.append("Δεν υπάρχει ενεργό HTF reversal context που να περνά το αυστηρό shortlist.")

    watch_count = sum(
        1 for r in results
        if r.reversal is not None and r.reversal.status == "WATCH"
    )
    invalid_count = sum(
        1 for r in results
        if r.reversal is not None and r.reversal.status == "INVALID"
    )
    lines += [
        "",
        f"_Εκτός shortlist: WATCH {watch_count} | INVALID {invalid_count}. Δεν θεωρούνται ενεργά candidates._",
    ]

    lines += [
        "",
        "### Καταστάσεις HTF Reversal",
        "",
        "- **WATCH:** η τιμή αντέδρασε σε επιβεβαιωμένη D1 zone, αλλά δεν υπάρχει ακόμη αρκετή H4 επιβεβαίωση.",
        f"- **ΑΝΑΜΟΝΗ H1 ΕΠΙΒΕΒΑΙΩΣΗΣ:** έγινε H1 retest και περιμένει νέο κλεισμένο H1 candle να επιβεβαιώσει· δεν είναι είσοδος.",
        f"- **ARMED · ΑΝΑΜΟΝΗ BREAK:** ισχυρό HTF context με το απαιτούμενο H1 break έως {REVERSAL_MAX_ARMED_BREAK_DISTANCE_ATR:.1f}× H1 ATR· μπαίνει στο shortlist μόνο με score ≥ {REVERSAL_MIN_ACTIVE_SCORE:.0f}. Δεν είναι είσοδος.",
        "- **WAIT RETEST:** έγινε H1 break και περιμένει επιστροφή στη broken zone.",
        "- **READY:** fresh confirmation στο τελευταίο κλεισμένο H1 και RR ≥ 3.0 προς την επόμενη D1 zone.",
        "- **INVALID:** παραβίαση D1 zone, ληγμένο H1 setup, υπερβολική απομάκρυνση ή RR < 3.0.",
        "- Απενεργοποίηση χωρίς αφαίρεση κώδικα: `ENABLE_HTF_REVERSAL=false python forex_scanner.py`.",
    ]

    lines += [
        "",
        "## Όλα τα 28 Forex pairs",
        "",
        "| Pair | W1 | D1 | H4 | H1 | Dir | EMA | D1 Struct | H4 Struct | BRC | RR | Quality |",
        "|---|---|---|---|---|---|---:|---|---|---|---:|---:|",
    ]
    for r in sorted(results, key=lambda x: x.pair):
        lines.append(
            f"| {r.pair} | {rating_text(r.w1_rating)} | {rating_text(r.d1_rating)} | "
            f"{rating_text(r.h4_rating)} | {rating_text(r.h1_rating)} | {r.direction} | {r.ema_passes}/3 | "
            f"{r.d1_structure} | {r.h4_structure} | {r.brc_status} | "
            f"{fmt_rr(r.rr, r.rr_pass)} | {r.quality_score:.1f} |"
        )

    lines += [
        "",
        "## Πώς διαβάζεται",
        "",
        "- **W1 / Weekly:** ανώτερο context. SUPPORTS όταν συμφωνεί με το D1/H4/H1 direction, OPPOSES όταν είναι αντίθετο. Δεν μπλοκάρει μόνο του ένα A+ setup.",
        "- **Κατεύθυνση:** EMA50 slope/close από κλεισμένα Yahoo candles· D1 και H4 ορίζουν την κατεύθυνση, H1 είναι το timing filter. Τα TradingView ratings είναι context.",
        "- **EMA50 3/3:** τιμή και κλίση EMA50 συμφωνούν με την κατεύθυνση και στα 3 TF.",
        "- **D1/H4 Struct:** BULL ή BEAR από ολοκληρωμένα swing highs/lows.",
        "- **ADX:** πάνω από ~20 δείχνει ισχυρότερη τάση· δεν είναι μόνο του σήμα εισόδου.",
        "- **BRC:** break σε επιβεβαιωμένο H1 swing, retest στη ζώνη και confirmation με κλείσιμο πέρα από το high/low του retest candle. READY ισχύει μόνο για confirmation στο τελευταίο ή αμέσως προηγούμενο κλεισμένο H1. Ανοιχτά κεριά αποκλείονται.",
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

    if ENABLE_HTF_REVERSAL:
        reversals = reversal_candidates(results)
        print("\n" + "=" * 100)
        print("HTF REVERSAL — INDEPENDENT MODE")
        print("=" * 100)
        print(
            f"{'#':<3} {'PAIR':<8} {'DIR':<6} {'STATE':<12} {'HTF ZONE':>10} "
            f"{'SWP':>4} {'REJ':>4} {'DSP':>4} {'H1 BRC':<15} {'RR':>6} {'SCORE':>7}"
        )
        print("-" * 100)
        for i, pair_scan in enumerate(reversals, start=1):
            rev = pair_scan.reversal
            print(
                f"{i:<3} {pair_scan.pair:<8} {rev.direction:<6} {rev.status:<12} "
                f"{fmt_zone(rev.htf_zone):>10} {fmt_check(rev.sweep):>4} "
                f"{fmt_check(rev.rejection):>4} {fmt_check(rev.displacement):>4} "
                f"{rev.brc_status:<15} {fmt_num(rev.rr, 2):>6} {rev.score:>6.1f}"
            )
        print("-" * 100)
        reversal_ready = sum(
            1 for r in reversals if r.reversal.status == "READY"
        )
        print(f"Candidates: {len(reversals)} | READY: {reversal_ready}")


def main():
    print("Ξεκινά advanced scan 28 Forex pairs + BTC/ETH/SOL...")
    results = scan_all_pairs()
    crypto_results = scan_all_crypto()
    print_results(results)
    write_markdown(results, crypto_results)
    print("\nΑποθηκεύτηκε: LATEST_FOREX_SCAN.md")


if __name__ == "__main__":
    main()

# Manual scan trigger 2026-09-23 08:01 Europe/Athens