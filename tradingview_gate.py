"""Fail-closed TradingView Pine audit for the GitHub Yahoo/OANDA Forex scan.

An independent ChatGPT TradingView connection publishes derived verification
signals to TRADINGVIEW_BRC_VERIFIED.json. This module cannot fetch TradingView.
The input is NEVER assumed trustworthy merely because a file exists.
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path

TV_SCRIPT_ID = "USER;ae27f010fee5413b8f5d1cc39e592cde"
TV_VERIFICATION_PATH = "TRADINGVIEW_BRC_VERIFIED.json"
MAX_REPORT_AGE = timedelta(minutes=85)
MAX_CANDLE_AGE = timedelta(hours=2)
MAX_PRICE_DIFFERENCE_PIPS = 8.0
MAX_ZONE_DIFFERENCE_PIPS = 8.0


def utc_time(value):
    if value is None:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except (TypeError, ValueError, OverflowError):
        return None


def finite_positive(value):
    if isinstance(value, bool):
        return None
    try:
        result = float(value)
        return result if math.isfinite(result) and result > 0 else None
    except (ValueError, TypeError, OverflowError):
        return None


def verify_candidate(scan, report, now):
    """Require identical symbol, completed H1, direction, price and BRC zone."""
    if not isinstance(report, dict) or report.get("schema_version") != 1:
        return False, "Missing or wrong TradingView verification schema"
    if report.get("script_id") != TV_SCRIPT_ID:
        return False, "Unrecognized TradingView indicator"
    run_at = utc_time(report.get("generated_at"))
    if run_at is None or not timedelta(minutes=-2) <= now - run_at <= MAX_REPORT_AGE:
        return False, "TradingView verification snapshot stale"
    rows = report.get("pairs")
    if not isinstance(rows, list):
        return False, "No TradingView verification records"
    row = next((x for x in rows if isinstance(x, dict) and x.get("pair") == scan.pair), None)
    if row is None:
        return False, "Pair not checked on TradingView"
    if row.get("symbol") != f"OANDA:{scan.pair}" or row.get("source") != "TradingView Pine":
        return False, "Wrong or untrusted TradingView symbol/source"
    if row.get("tv_ready") is not True or row.get("brc_stage") != 4:
        return False, "TradingView did not confirm a full BRC"
    if row.get("direction") != scan.direction or row.get("ema_passes") != 3:
        return False, "TradingView direction/EMA disagreement"
    expected_structure = 1 if scan.direction == "LONG" else -1
    if scan.direction not in ("LONG", "SHORT"):
        return False, "No direction"
    if row.get("d1_structure") != expected_structure or row.get("h4_structure") != expected_structure:
        return False, "TradingView HTF structure disagreement"
    for key in ("adx_h4", "adx_h1"):
        value = finite_positive(row.get(key))
        if value is None or value < 20:
            return False, f"Insufficient TradingView {key}"
    if finite_positive(row.get("rr")) is None or float(row["rr"]) < 1.2:
        return False, "TradingView RR below 1.2"
    tv_h1_open = utc_time(row.get("h1_open_at"))
    yahoo_h1_open = utc_time(scan.h1_closed_at)
    if tv_h1_open is None or yahoo_h1_open is None or tv_h1_open != yahoo_h1_open:
        return False, "TradingView and Yahoo use different H1 bars"
    candle_age = now - (tv_h1_open + timedelta(hours=1))
    if not timedelta(minutes=-2) <= candle_age <= MAX_CANDLE_AGE:
        return False, "TradingView H1 candle is not recent and closed"
    entry, stop, target, zone = (finite_positive(row.get(k)) for k in ("entry", "stop", "target", "zone"))
    if None in (entry, stop, target, zone):
        return False, "Missing TradingView trade levels"
    signed = 1 if scan.direction == "LONG" else -1
    risk = signed * (entry - stop)
    reward = signed * (target - entry)
    if risk <= 0 or reward <= 0 or reward / risk < 1.2:
        return False, "Invalid TradingView trade plan"
    pip = 0.01 if scan.pair.endswith("JPY") else 0.0001
    scan_entry, scan_zone = finite_positive(scan.entry), finite_positive(scan.zone)
    if scan_entry is None or scan_zone is None:
        return False, "Yahoo has no comparable READY entry/zone"
    if abs(entry - scan_entry) / pip > MAX_PRICE_DIFFERENCE_PIPS:
        return False, "Yahoo and TradingView entry closes do not agree"
    if abs(zone - scan_zone) / pip > MAX_ZONE_DIFFERENCE_PIPS:
        return False, "Yahoo and TradingView BRC zones do not agree"
    return True, "Both models confirm the same closed H1, direction and zone"


def gate_trend_results(results, path=TV_VERIFICATION_PATH, now=None):
    """Demote unverified READY signals. Other Trend/HTF watch states unchanged."""
    now = utc_time(now) if now is not None else datetime.now(timezone.utc)
    try:
        report = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        report = {}
    for scan in results:
        if scan.brc_status != "READY" and scan.entry is None:
            continue
        passed, reason = verify_candidate(scan, report, now)
        if not passed:
            print(f"[TV-GATE] {scan.pair}: blocked READY: {reason}")
            scan.setup_grade = "WATCH"
            scan.brc_status = "TV UNVERIFIED"
            scan.entry = None
            scan.stop_loss = None
            scan.take_profit = None
            scan.rr = None
            scan.rr_pass = False
            scan.quality_score = min(scan.quality_score, 85.0)
        else:
            print(f"[TV-GATE] {scan.pair}: independently VERIFIED on TradingView")
    return results
