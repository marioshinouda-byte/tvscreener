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

    def test_stale_candles_cannot_produce_ready_even_with_aligned_ratings(self):
        frame = candle_history()
        frame.index -= pd.Timedelta(hours=scanner.MAX_H1_DATA_AGE_HOURS + 2)
        history = scanner.prepare_candle_history(frame)
        row = pd.Series({"Symbol": "OANDA:EURUSD", "Technical Rating": 1.0,
                         "Recommend All|240": 1.0, "Recommend All|60": 1.0})
        with patch.object(scanner, "fetch_pair", return_value=row), \
             patch.object(scanner, "fetch_candle_history", return_value=history), \
             patch.object(scanner, "ENABLE_HTF_REVERSAL", True):
            result = scanner.scan_pair("EURUSD")

        self.assertEqual(result.candles, "STALE")
        self.assertEqual(result.direction, "—")
        self.assertNotEqual(result.setup_grade, "A+ READY")
        self.assertEqual(result.reversal.status, "INVALID")
        self.assertIsNone(result.entry)

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
