from contextlib import redirect_stdout
from io import StringIO
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

import forex_scanner as scanner


def candle_history():
    """Synthetic rising candles, including the most recent completed hour."""
    current_hour = pd.Timestamp.now(tz="UTC").floor("h")
    index = pd.date_range(current_hour - pd.Timedelta(days=180), current_hour,
                          freq="h", inclusive="left")
    index = index[index.day_of_week < 5]
    close = 1.0 + np.arange(len(index)) * 0.00001
    frame = pd.DataFrame(
        {"Open": close - 0.000005, "High": close + 0.00001,
         "Low": close - 0.00001, "Close": close}, index=index,
    )
    latest = float(frame["Close"].iloc[-1]) + 0.00001
    frame.loc[current_hour - pd.Timedelta(hours=1)] = [
        latest - 0.000005, latest + 0.00001, latest - 0.00001, latest,
    ]
    return frame.sort_index()


class ScannerReliabilityTest(unittest.TestCase):
    def test_keeps_last_closed_h1_and_excludes_current_open_candle(self):
        frame = candle_history()
        current_hour = pd.Timestamp.now(tz="UTC").floor("h")
        last_closed = current_hour - pd.Timedelta(hours=1)
        frame.loc[current_hour] = [2.05, 2.2, 2.0, 2.15]
        h1, h4, d1 = scanner.prepare_candle_history(frame)

        self.assertEqual(h1.index[-1], last_closed)
        self.assertNotIn(current_hour, h1.index)
        now = pd.Timestamp.now(tz="UTC")
        self.assertTrue((h4.index + pd.Timedelta(hours=4) <= now).all())
        self.assertTrue((d1.index + pd.Timedelta(days=1) <= now).all())

    def test_stale_candles_warn_and_suppress_signals(self):
        frame = candle_history()
        frame.index -= pd.Timedelta(hours=scanner.MAX_H1_DATA_AGE_HOURS + 2)
        history = scanner.prepare_candle_history(frame)
        row = pd.Series({"Symbol": "OANDA:EURUSD", "Technical Rating": 1.0,
                         "Recommend All|240": 1.0, "Recommend All|60": 1.0})
        output = StringIO()
        with patch.object(scanner, "fetch_pair", return_value=row), \
             patch.object(scanner, "fetch_candle_history", return_value=history), \
             patch.object(scanner, "ENABLE_HTF_REVERSAL", True):
            with patch.object(scanner, "MAX_H1_DATA_AGE_HOURS",
                              scanner.MAX_H1_DATA_AGE_HOURS + 24):
                reference = scanner.scan_pair("EURUSD")
            with redirect_stdout(output):
                result = scanner.scan_pair("EURUSD")

        self.assertEqual(reference.candles, "TV-REF-MISSING")
        self.assertEqual(result.candles, "YF-STALE")
        self.assertEqual(result.direction, "—")
        self.assertEqual(result.bias, "STALE DATA")
        self.assertEqual(result.setup_grade, "—")
        self.assertEqual(result.quality_score, 0.0)
        self.assertEqual(result.ema_passes, 0)
        self.assertIsNone(result.price)
        self.assertIsNone(result.reversal)
        self.assertIsNone(result.entry)
        self.assertIn("signals suppressed", output.getvalue())

        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "LATEST_FOREX_SCAN.md"
            scanner.write_markdown([result], path=str(report))
            content = report.read_text()
        self.assertIn("YF-STALE: 1 ζευγάρια (EURUSD)", content)
        self.assertIn("Δεν παράγονται σήματα από παλιά δεδομένα", content)
        self.assertNotIn("Η ανάλυση συνεχίζεται με τα παλιά δεδομένα", content)

    def test_oanda_prescreen_filters_and_ranks_without_yahoo(self):
        def tv_row(symbol, d1=0.8, h4=0.7, h1=0.5):
            return pd.Series({
                "Symbol": symbol, "Technical Rating": d1,
                "Recommend All|240": h4, "Recommend All|60": h1,
                "Price": 1.1500, "EMA50 D1": 1.10, "EMA50 D1 Prev": 1.09,
                "EMA50 H4": 1.12, "EMA50 H4 Prev": 1.11,
                "EMA50 H1": 1.13, "EMA50 H1 Prev": 1.12,
                "ADX H4": 31.0, "ADX H1": 25.0,
            })

        self.assertIsNone(scanner.oanda_prescreen_from_row(tv_row("FOREXCOM:EURUSD")))
        self.assertIsNone(scanner.oanda_prescreen_from_row(tv_row("OANDA:EURUSD", h4=-0.7)))
        self.assertIsNone(scanner.oanda_prescreen_from_row(tv_row("OANDA:EURUSD", h1=-0.3)))
        self.assertIsNone(scanner.oanda_prescreen_from_row(tv_row("OANDA:EURUSD", d1=0.8, h4=0.7, h1=0.5).where(
            lambda x: x.index != "ADX H4", 12.0)))
        preview = scanner.oanda_prescreen_from_row(tv_row("OANDA:EURUSD"))
        self.assertEqual(preview.direction, "LONG")
        self.assertEqual(preview.ema_passes, 3)
        self.assertEqual(preview.ema_checked, 3)

        with patch.object(scanner, "fetch_pair", return_value=tv_row("OANDA:EURUSD")), \
             patch.object(scanner, "fetch_candle_history", return_value=None):
            no_yahoo = scanner.scan_pair("EURUSD")
        self.assertIsNone(no_yahoo.price)
        self.assertEqual(no_yahoo.direction, "—")
        self.assertIsNotNone(no_yahoo.oanda_prescreen)
        self.assertEqual(scanner.oanda_shortlist([no_yahoo]), [no_yahoo])
        with tempfile.TemporaryDirectory() as directory:
            scanner.write_markdown([no_yahoo], path=str(Path(directory) / "LATEST_FOREX_SCAN.md"))
            shortlist = Path(directory, "OANDA_SHORTLIST.md").read_text()
            self.assertIn("EURUSD", shortlist)
            self.assertIn("WATCH ONLY", shortlist)
            self.assertNotIn("Entry {", shortlist)

    def test_oanda_shortlist_uses_at_most_five_and_never_non_oanda(self):
        rows = []
        for i in range(9):
            entry = scanner.PairScan(
                pair=f"P{i}", symbol=f"OANDA:P{i}", provider="OANDA",
                direction="—", bias="NO DATA", d1_rating=0.4,
                h4_rating=0.4, h1_rating=0.4, price=None,
                ema_passes=0, ema_total=3, adx_h4=None, adx_h1=None,
                d1_structure="N/A", h4_structure="N/A", brc_status="WAIT",
                zone=None, quality_score=0.0, setup_grade="—",
                candles="N/A", entry=None, stop_loss=None, take_profit=None,
                rr=None, rr_pass=False,
                oanda_prescreen=scanner.OandaPreScreen(
                    "LONG", 10.0 + i, 1.0, 3, 3, 25, 25),
            )
            rows.append(entry)
        shortlist = scanner.oanda_shortlist(rows)
        self.assertEqual(len(shortlist), 5)
        self.assertEqual([r.pair for r in shortlist], ["P8", "P7", "P6", "P5", "P4"])

    def test_candle_diagnostics_cover_batch_missing_and_cached_data(self):
        frame = candle_history()
        batch = pd.concat({"EURUSD=X": frame}, axis=1)
        output = StringIO()
        with patch.object(scanner, "_CANDLE_HISTORY_CACHE", {}), \
             patch.object(scanner.yf, "download", return_value=batch) as download, \
             redirect_stdout(output):
            scanner.prefetch_candle_histories(["EURUSD", "GBPUSD"])
            history = scanner.fetch_candle_history("EURUSD")
            missing = scanner.fetch_candle_history("GBPUSD")

        self.assertIsNotNone(history)
        self.assertIsNone(missing)
        download.assert_called_once()
        self.assertIn(
            f"[INFO] EURUSD | candles={len(frame)} | last={frame.index[-1]}",
            output.getvalue(),
        )
        self.assertIn("[INFO] GBPUSD | candles=0 | last=NONE", output.getvalue())
        self.assertEqual(output.getvalue().count("[INFO]"), 2)

    def scanner_command(self):
        workflow = (Path(scanner.__file__).parent / ".github/workflows/forex-scanner.yml").read_text()
        section = workflow.split("      - name: Run advanced Forex scanner\n", 1)[1]
        section = section.split("\n      - name:", 1)[0]
        return textwrap.dedent(section.split("run: |\n", 1)[1])

    def test_workflow_propagates_scanner_failure_through_tee(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "forex_scanner.py").write_text("raise SystemExit(23)\n")
            result = subprocess.run(["bash", "-e", "-c", self.scanner_command()],
                                    cwd=directory, capture_output=True, text=True)
        self.assertEqual(result.returncode, 23)

    def test_workflow_preserves_successful_scanner_output(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "forex_scanner.py").write_text("print('scan completed')\n")
            result = subprocess.run(["bash", "-e", "-c", self.scanner_command()],
                                    cwd=directory, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(Path(directory, "scan_output.txt").read_text(), "scan completed\n")


if __name__ == "__main__":
    unittest.main()
