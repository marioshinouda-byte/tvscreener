"""Independent OANDA-versus-Yahoo H1 validation before calculating Forex BRC.

OANDA's TradingView screener gives the previous H1 bar's UTC open timestamp
and close, plus the latest update time. Yahoo provides full historical OHLC.
Both are used only when the SAME completed H1 bar matches in timestamp and
price. This is not an OANDA OHLC history feed; no match means no signal.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Optional

import pandas as pd


MAX_OANDA_REF_AGE_HOURS = 4
MAX_YAHOO_REF_AGE_HOURS = 4
MAX_CLOSE_DIFF_PIPS = 8.0


@dataclass
class HistoryValidation:
    ok: bool
    status: str
    detail: str
    h1: Optional[pd.DataFrame] = None
    difference_pips: Optional[float] = None


def _timestamp(value):
    """TradingView dates are Unix seconds (accept milliseconds defensively)."""
    try:
        seconds = float(value)
        if not math.isfinite(seconds):
            return None
        if seconds > 1e12:
            seconds /= 1000
        result = pd.to_datetime(seconds, unit="s", utc=True)
        if result.year < 2000 or result.year > 2100:
            return None
        return result
    except (ValueError, TypeError, OverflowError, OSError):
        return None


def _positive_number(value):
    try:
        result = float(value)
        return result if math.isfinite(result) and result > 0 else None
    except (ValueError, TypeError):
        return None


def verify_h1_history(pair: str, h1: pd.DataFrame, row, now=None) -> HistoryValidation:
    """Confirm Yahoo completed H1 matches the same OANDA H1 in time and price.

    OANDA's 'Time|60' may represent a *forming* H1 candle, so use only
    'OANDA Previous H1 Open' and 'OANDA Previous H1 Close'. The screener's
    last-update timestamp must also be recent; old snapshots never validate
    a freshly downloaded candle. Newer Yahoo bars are deliberately trimmed
    to this independently confirmed completed-candle boundary.
    """
    now = pd.Timestamp.now(tz="UTC") if now is None else pd.Timestamp(now)
    now = now.tz_localize("UTC") if now.tzinfo is None else now.tz_convert("UTC")

    if row is None or not str(row.get("Symbol", "")).startswith("OANDA:"):
        return HistoryValidation(False, "NO-OANDA", "Ο provider δεν είναι OANDA")
    tv_start = _timestamp(row.get("OANDA Previous H1 Open"))
    tv_update = _timestamp(row.get("Last Bar Update Time|60"))
    tv_close = _positive_number(row.get("OANDA Previous H1 Close"))
    if tv_start is None or tv_update is None or tv_close is None:
        return HistoryValidation(False, "TV-REF-MISSING", "Δεν δόθηκε πλήρες κλεισμένο OANDA H1")

    if tv_start + pd.Timedelta(hours=1) > now + pd.Timedelta(minutes=2):
        return HistoryValidation(False, "TV-FUTURE-BAR", "OANDA H1 δεν έχει κλείσει")
    update_age = now - tv_update
    if update_age < -pd.Timedelta(minutes=2) or update_age > pd.Timedelta(hours=MAX_OANDA_REF_AGE_HOURS):
        return HistoryValidation(False, "TV-REF-STALE", "Το OANDA H1 update είναι παλιό ή μελλοντικό")

    if h1 is None or h1.empty or not all(c in h1.columns for c in ("Open", "High", "Low", "Close")):
        return HistoryValidation(False, "YF-NO-OHLC", "Απουσιάζουν OHLC του Yahoo")

    frame = h1.copy()
    ix = pd.DatetimeIndex(frame.index)
    ix = ix.tz_localize("UTC") if ix.tz is None else ix.tz_convert("UTC")
    frame.index = ix
    if frame.index.has_duplicates or not frame.index.is_monotonic_increasing:
        return HistoryValidation(False, "YF-BAD-TIMES", "Διπλά ή μη ταξινομημένα H1 timestamps")

    frame = frame.loc[frame.index <= tv_start]
    if frame.empty or frame.index[-1] != tv_start:
        return HistoryValidation(False, "YF-H1-MISMATCH", "Δεν βρέθηκε το ίδιο κλεισμένο H1 κερί OANDA/Yahoo")

    yahoo_age = now - (frame.index[-1] + pd.Timedelta(hours=1))
    if yahoo_age < -pd.Timedelta(minutes=2) or yahoo_age > pd.Timedelta(hours=MAX_YAHOO_REF_AGE_HOURS):
        return HistoryValidation(False, "YF-STALE", "Η τελευταία συμφωνημένη H1 ώρα είναι παλιά")

    sample = frame[["Open", "High", "Low", "Close"]].tail(100).astype(float)
    if not (sample.notna().all().all() and (sample > 0).all().all()):
        return HistoryValidation(False, "YF-BAD-OHLC", "Άκυρες ή μη θετικές τιμές OHLC")
    if not (
        (sample["High"] >= sample[["Open", "Close", "Low"]].max(axis=1)).all()
        and (sample["Low"] <= sample[["Open", "Close", "High"]].min(axis=1)).all()
    ):
        return HistoryValidation(False, "YF-BAD-OHLC", "Μη έγκυρα όρια High/Low")

    pip = 0.01 if pair.endswith("JPY") else 0.0001
    difference = abs(float(frame["Close"].iloc[-1]) - tv_close) / pip
    if difference > MAX_CLOSE_DIFF_PIPS:
        return HistoryValidation(
            False, "PRICE-MISMATCH",
            f"Yahoo/OANDA διαφορά {difference:.1f} pips πάνω από {MAX_CLOSE_DIFF_PIPS:.1f}",
            difference_pips=round(difference, 1),
        )

    return HistoryValidation(
        True, "YF+OANDA-H1",
        f"Έλεγχος ίδιου κλεισμένου H1, διαφορά {difference:.1f} pips "
        "(το πλήρες ιστορικό παραμένει Yahoo)",
        h1=frame,
        difference_pips=round(difference, 1),
    )
