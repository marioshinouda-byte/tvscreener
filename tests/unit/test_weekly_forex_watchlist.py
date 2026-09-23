import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from forex_scanner import PairScan, ReversalScan, trend_state, weekly_trend_watchlist, write_markdown


def pair(name, score, *, grade="WATCH", brc="WAIT FOR BREAK", direction="LONG"):
    return PairScan(
        pair=name, symbol=name, provider="test", direction=direction, bias="ALIGNED",
        d1_rating=0.5, h4_rating=0.5, h1_rating=0.5, price=1.0,
        ema_passes=3, ema_total=3, adx_h4=30, adx_h1=30,
        d1_structure="BULL", h4_structure="BULL", brc_status=brc,
        zone=1.0, quality_score=score, setup_grade=grade, candles="OK",
        entry=None, stop_loss=None, take_profit=None, rr=None, rr_pass=False,
    )


class WeeklyForexWatchlistTest(unittest.TestCase):
    def test_report_prioritizes_ready_and_keeps_reversal_separate(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "LATEST_FOREX_SCAN.md"
            result = pair("EURUSD", 90, grade="A+ READY", brc="READY")
            result.reversal = ReversalScan(
                direction="SHORT", status="ARMED", score=100.0,
                brc_status="RETEST", note="H1 retest — περιμένει confirmation",
            )
            write_markdown([result], str(report))
            text = report.read_text(encoding="utf-8")
            self.assertLess(text.index("🟢 ENTRY READY — Trend"), text.index("Weekly Top 5"))
            self.assertLess(text.index("Weekly Top 5"), text.index("🔥 HOT NEW — Trend"))
            self.assertLess(text.index("🔥 HOT NEW — Trend"), text.index("HTF Reversal — ξεχωριστό mode"))
            self.assertIn("Setup Score 90.0%", text)
            self.assertIn("όχι ποσοστό πιθανότητας επιτυχίας", text)
            self.assertIn("HTF Reversal Score μετρά τη συμφωνία", text)
            self.assertIn("Context score", text)
            self.assertIn("H1 retest — περιμένει confirmation", text)
            self.assertIn("| RETEST | — | — | — | — | — | **100.0/100** |", text)

    def test_confirmed_brc_without_a_plus_filters_is_watch_not_wait(self):
        result = pair("EURUSD", 80, grade="WATCH", brc="READY")
        self.assertEqual(trend_state(result), "🟡 WATCH")

    def test_weekly_continuity_hot_new_promotion_and_rollover(self):
        athens = ZoneInfo("Europe/Athens")
        monday = datetime(2026, 9, 21, 8, tzinfo=athens)
        with tempfile.TemporaryDirectory() as directory:
            state_path = str(Path(directory) / "weekly.json")
            first = [pair(f"P{i}", 80 - i * 5) for i in range(5)]
            weekly, hot, week = weekly_trend_watchlist(first, monday, state_path)
            self.assertEqual([r.pair for r in weekly], ["P0", "P1", "P2", "P3", "P4"])
            self.assertEqual(hot, [])

            updated = [pair(f"P{i}", 30 + i) for i in range(5)] + [pair("NEW", 88)]
            weekly, hot, _ = weekly_trend_watchlist(updated, monday, state_path)
            self.assertEqual([r.pair for r in weekly], ["P0", "P1", "P2", "P3", "P4"])
            self.assertEqual([r.pair for r in hot], ["NEW"])

            confirmed = updated[:-1] + [pair("NEW", 90, grade="A+ READY", brc="READY")]
            weekly, hot, _ = weekly_trend_watchlist(confirmed, monday, state_path)
            self.assertEqual([r.pair for r in weekly], ["NEW", "P1", "P2", "P3", "P4"])
            self.assertEqual(hot, [])
            self.assertEqual(trend_state(weekly[0]), "🟢 ENTRY READY")
            self.assertEqual(len(json.loads(Path(state_path).read_text())["top5"]), 5)

            next_monday = datetime(2026, 9, 28, 8, tzinfo=athens)
            weekly, hot, new_week = weekly_trend_watchlist(updated, next_monday, state_path)
            self.assertNotEqual(week, new_week)
            self.assertEqual(weekly[0].pair, "NEW")
            self.assertEqual(hot, [])


if __name__ == "__main__":
    unittest.main()
