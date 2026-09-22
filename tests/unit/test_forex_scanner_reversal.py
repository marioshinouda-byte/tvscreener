import os
import subprocess
import sys

import numpy as np
import pandas as pd

import forex_scanner as scanner


def reversal_frames():
    rng = np.random.default_rng(7)

    d1_index = pd.date_range("2026-07-01", periods=60, freq="D", tz="UTC")
    d1_close = 1.215 + 0.012 * np.sin(np.arange(60) / 4)
    d1 = pd.DataFrame(index=d1_index)
    d1["Open"] = d1_close + rng.normal(0, 0.001, 60)
    d1["Close"] = d1_close
    d1["High"] = d1[["Open", "Close"]].max(axis=1) + 0.006
    d1["Low"] = d1[["Open", "Close"]].min(axis=1) - 0.006
    d1.loc[d1.index[38], "High"] = 1.2500

    h4_index = pd.date_range("2026-08-10", periods=100, freq="4h", tz="UTC")
    h4_close = np.linspace(1.222, 1.238, 100)
    h4 = pd.DataFrame(index=h4_index)
    h4["Open"] = h4_close - 0.0005
    h4["Close"] = h4_close
    h4["High"] = h4[["Open", "Close"]].max(axis=1) + 0.0020
    h4["Low"] = h4[["Open", "Close"]].min(axis=1) - 0.0020

    reaction = {
        -5: {"Open": 1.2440, "High": 1.2510, "Low": 1.2410, "Close": 1.2430},
        -4: {"Open": 1.2430, "High": 1.2440, "Low": 1.2330, "Close": 1.2340},
        -3: {"Open": 1.2340, "High": 1.2360, "Low": 1.2310, "Close": 1.2320},
        -2: {"Open": 1.2320, "High": 1.2340, "Low": 1.2290, "Close": 1.2310},
        -1: {"Open": 1.2310, "High": 1.2330, "Low": 1.2280, "Close": 1.2300},
    }
    for offset, values in reaction.items():
        for column, value in values.items():
            h4.loc[h4.index[offset], column] = value

    h1_index = pd.date_range("2026-08-20", periods=220, freq="h", tz="UTC")
    h1_close = 1.229 + 0.0015 * np.sin(np.arange(220) / 6)
    h1 = pd.DataFrame(index=h1_index)
    h1["Open"] = h1_close - 0.0002
    h1["Close"] = h1_close
    h1["High"] = h1[["Open", "Close"]].max(axis=1) + 0.0008
    h1["Low"] = h1[["Open", "Close"]].min(axis=1) - 0.0008

    return h1, h4, d1


def test_reversal_mode_can_be_disabled_without_code_changes():
    output = subprocess.check_output(
        [
            sys.executable,
            "-c",
            "import forex_scanner as scanner; print(scanner.ENABLE_HTF_REVERSAL)",
        ],
        env={**os.environ, "ENABLE_HTF_REVERSAL": "false"},
        text=True,
    ).strip()
    assert output == "False"


def test_h4_sweep_rejection_and_displacement_arm_short_context():
    h1, h4, d1 = reversal_frames()

    reversal = scanner.analyze_htf_reversal(h1, h4, d1)

    assert reversal.direction == "SHORT"
    assert reversal.status == "ARMED"
    assert reversal.htf_zone == 1.2500
    assert reversal.sweep is True
    assert reversal.rejection is True
    assert reversal.displacement is True


def test_h4_close_through_d1_zone_invalidates_context():
    h1, h4, d1 = reversal_frames()
    d1["High"] = np.minimum(d1["High"], 1.2300)
    d1.loc[d1.index[38], "High"] = 1.2500
    h4.loc[h4.index[-1], ["Open", "High", "Low", "Close"]] = [
        1.2570,
        1.2620,
        1.2560,
        1.2600,
    ]

    reversal = scanner.analyze_htf_reversal(h1, h4, d1)

    assert reversal.direction == "SHORT"
    assert reversal.status == "INVALID"
    assert "πέρα από" in reversal.note
