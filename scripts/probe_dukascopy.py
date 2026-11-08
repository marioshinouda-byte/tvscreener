"""One-off live smoke test of Dukascopy's public H1 candle source."""
import lzma
import struct
from datetime import datetime, timezone

import requests


def probe(pair, year, month):
    month_zero_based = month - 1
    url = f"https://datafeed.dukascopy.com/datafeed/{pair}/{year}/{month_zero_based:02d}/BID_candles_hour_1.bi5"
    response = requests.get(url, timeout=18, headers={"User-Agent": "ForexScanner-MarketDataProbe/1.0"})
    print(f"{pair} {year}-{month:02d}: HTTP {response.status_code}, bytes={len(response.content)}", flush=True)
    if response.status_code != 200 or not response.content:
        return
    data = lzma.decompress(response.content)
    print("raw bytes:", len(data), "records:", len(data) // 24, "remainder:", len(data) % 24, flush=True)
    if len(data) < 24:
        return
    sec, opened, closed, low, high, volume = struct.unpack_from(">IIIIIf", data, len(data) - 24)
    when = datetime(year, month, 1, tzinfo=timezone.utc)
    from datetime import timedelta
    when += timedelta(seconds=sec)
    divider = 1000 if pair.endswith("JPY") else 100000
    print("last record:", when.isoformat(), "OHLC=", [v / divider for v in (opened, high, low, closed)], "vol=", volume, flush=True)


if __name__ == "__main__":
    for pair in ("EURUSD", "USDJPY"):
        for y, m in ((2026, 10), (2026, 11)):
            try:
                probe(pair, y, m)
            except Exception as exc:
                print(f"FAILED {pair} {y}-{m}: {exc!r}", flush=True)
