"""Fail-closed tests for Yahoo + OANDA H1 independent cross-check."""
import unittest

import pandas as pd

from market_data_quality import verify_h1_history


class MarketDataQualityTest(unittest.TestCase):
    def setUp(self):
        self.now = pd.Timestamp("2026-11-09T10:17:00Z")
        self.current = pd.Timestamp("2026-11-09T10:00:00Z")
        self.previous = self.current - pd.Timedelta(hours=1)
        index = pd.date_range(self.previous - pd.Timedelta(hours=149), periods=150, freq="h", tz="UTC")
        close = [1.15 for _ in range(len(index))]
        self.h1 = pd.DataFrame({
            "Open": close, "High": [v + 0.0003 for v in close],
            "Low": [v - 0.0003 for v in close], "Close": close,
        }, index=index)
        self.ref = {
            "Symbol": "OANDA:EURUSD",
            "OANDA Previous H1 Open": int(self.previous.timestamp()),
            "OANDA Previous H1 Close": 1.15004,
            "Last Bar Update Time|60": int((self.now - pd.Timedelta(minutes=1)).timestamp()),
        }

    def test_matching_bar_and_price(self):
        result = verify_h1_history("EURUSD", self.h1, self.ref, now=self.now)
        self.assertTrue(result.ok)
        self.assertEqual(result.status, "YF+OANDA-H1")
        self.assertLess(result.difference_pips, 1)

    def test_trim_newer_yahoo_candles(self):
        frame = self.h1.copy()
        frame.loc[self.current] = [1.30, 1.31, 1.29, 1.30]
        result = verify_h1_history("EURUSD", frame, self.ref, now=self.now)
        self.assertTrue(result.ok)
        self.assertEqual(result.h1.index[-1], self.previous)

    def test_reject_mismatched_ohlc_price(self):
        ref = dict(self.ref, **{"OANDA Previous H1 Close": 1.1600})
        result = verify_h1_history("EURUSD", self.h1, ref, now=self.now)
        self.assertFalse(result.ok)
        self.assertEqual(result.status, "PRICE-MISMATCH")

    def test_reject_stale_reference_and_missing_data(self):
        ref = dict(self.ref, **{"Last Bar Update Time|60": int((self.now - pd.Timedelta(hours=7)).timestamp())})
        self.assertEqual(verify_h1_history("EURUSD", self.h1, ref, now=self.now).status, "TV-REF-STALE")
        ref = dict(self.ref)
        del ref["OANDA Previous H1 Open"]
        self.assertEqual(verify_h1_history("EURUSD", self.h1, ref, now=self.now).status, "TV-REF-MISSING")

    def test_reject_wrong_timestamp(self):
        ref = dict(self.ref, **{"OANDA Previous H1 Open": int((self.previous - pd.Timedelta(minutes=20)).timestamp())})
        self.assertEqual(verify_h1_history("EURUSD", self.h1, ref, now=self.now).status, "YF-H1-MISMATCH")

    def test_reject_bad_high_low(self):
        frame = self.h1.copy()
        frame.loc[self.previous, "High"] = 1.13
        self.assertEqual(verify_h1_history("EURUSD", frame, self.ref, now=self.now).status, "YF-BAD-OHLC")

    def test_do_not_accept_forexcom_instead_of_oanda(self):
        ref = dict(self.ref, Symbol="FOREXCOM:EURUSD")
        self.assertEqual(verify_h1_history("EURUSD", self.h1, ref, now=self.now).status, "NO-OANDA")


if __name__ == "__main__":
    unittest.main()
