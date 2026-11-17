"""Regression tests: no Yahoo READY is published without same-bar TV audit."""
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

from tradingview_gate import TV_SCRIPT_ID, gate_trend_results, verify_candidate


class TradingViewGateTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 17, 12, 32, tzinfo=timezone.utc)
        self.h1 = self.now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
        self.scan = SimpleNamespace(
            pair="EURUSD", direction="SHORT", h1_closed_at=self.h1,
            price=1.10000, zone=1.10100, entry=1.10000,
            stop_loss=1.10200, take_profit=1.09600, rr=2.0,
            rr_pass=True, quality_score=100.0, setup_grade="A+ READY",
            brc_status="READY",
        )
        self.row = {
            "pair": "EURUSD", "symbol": "OANDA:EURUSD",
            "source": "TradingView Pine",
            "h1_open_at": self.h1.isoformat(), "direction": "SHORT",
            "tv_ready": True, "brc_stage": 4, "ema_passes": 3,
            "d1_structure": -1, "h4_structure": -1,
            "adx_h4": 30.0, "adx_h1": 35.0,
            "zone": 1.10100, "entry": 1.10000,
            "stop": 1.10200, "target": 1.09600, "rr": 2.0,
        }
        self.report = {
            "schema_version": 1, "script_id": TV_SCRIPT_ID,
            "generated_at": self.now.isoformat(),
            "pairs": [self.row],
        }

    def test_good_same_bar_and_zone_can_pass(self):
        ok, reason = verify_candidate(self.scan, self.report, self.now)
        self.assertTrue(ok, reason)

    def test_wrong_zone_is_rejected(self):
        self.row["zone"] = 1.10300
        self.assertFalse(verify_candidate(self.scan, self.report, self.now)[0])

    def test_other_candle_is_rejected(self):
        self.row["h1_open_at"] = (self.h1 - timedelta(hours=1)).isoformat()
        self.assertFalse(verify_candidate(self.scan, self.report, self.now)[0])

    def test_stale_snapshot_is_rejected(self):
        self.report["generated_at"] = (self.now - timedelta(hours=3)).isoformat()
        self.assertFalse(verify_candidate(self.scan, self.report, self.now)[0])

    def test_no_tv_ready_is_rejected(self):
        self.row["tv_ready"] = False
        self.assertFalse(verify_candidate(self.scan, self.report, self.now)[0])

    def test_missing_file_suppresses_entry(self):
        with tempfile.TemporaryDirectory() as folder:
            gate_trend_results([self.scan], Path(folder) / "absent.json", self.now)
        self.assertEqual(self.scan.setup_grade, "WATCH")
        self.assertEqual(self.scan.brc_status, "TV UNVERIFIED")
        self.assertIsNone(self.scan.entry)
        self.assertIsNone(self.scan.stop_loss)
        self.assertIsNone(self.scan.take_profit)

    def test_verified_snapshot_keeps_entry(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "tv.json"
            target.write_text(json.dumps(self.report), encoding="utf-8")
            gate_trend_results([self.scan], target, self.now)
        self.assertEqual(self.scan.setup_grade, "A+ READY")
        self.assertEqual(self.scan.entry, 1.10000)


if __name__ == "__main__":
    unittest.main()
