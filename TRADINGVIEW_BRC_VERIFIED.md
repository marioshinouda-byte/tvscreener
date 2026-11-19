# TradingView BRC — ανεξάρτητος ωριαίος έλεγχος Trend

**Ώρα Ελλάδας:** 19/11/2026, 02:32:12 (Europe/Athens)  
**UTC:** 2026-11-19T00:32:12Z  
**Πηγή:** TradingView Pine μέσω του συνδεδεμένου TradingView MCP.  
**Αποκρίσεις:** 10/10 επιτυχείς, με ταυτοποιημένο δείκτη και έγκυρα metainfo.plots. Δεν χρησιμοποιήθηκαν προηγούμενα snapshots.

**Δείκτης:** BRC TV Triple TF Audit v1, `USER;ae27f010fee5413b8f5d1cc39e592cde`.  
**Παράμετροι:** OANDA:PAIR, timeframe=1h, calc_bars_count=500, return_bars=1.  
**Κλεισμένο H1:** open 2026-11-18T23:00:00.000Z, close 2026-11-19T00:00:00.000Z. Ηλικία κλεισίματος κατά τη δημοσίευση περίπου 32.2 λεπτά. Χρησιμοποιήθηκε αποκλειστικά last_values, ποτέ το forming candle από values[].

## Κάλυψη

- Weekly Top 5: NZDCAD, AUDJPY, AUDCHF, AUDUSD, AUDNZD.
- OANDA Top 5: USDCHF, NZDUSD, CADCHF, USDCAD, GBPUSD.
- Trend TV UNVERIFIED / READY στο report εισόδου: AUDNZD.
- Πρόσθετοι εκτός πεντάδων: κανένας.
- Μοναδικά ζευγάρια: 10. Εξετάστηκαν όλες οι γραμμές Trend και ο πίνακας όλων των 28 Forex pairs. Crypto και HTF Reversal εξαιρούνται.

## Ανεξάρτητος πίνακας audit

Οι τιμές EMA/structure/ADX/BRC/zone/κλεισμένης H1 προέρχονται από τα plots του Pine. Structure: +1 BULL, -1 BEAR, 0 MIXED.

| Pair | Direction | EMA | D1 | H4 | ADX H4 | ADX H1 | BRC | Zone | Κλεισμένη H1 τιμή | tv_ready (Pine μόνο) |
|---|---|---|---|---|---|---|---|---|---|---|
| NZDCAD | SHORT | 3/3 | 1 | 1 | 15.79 | 10.92 | 1 WAIT BREAK | 0.7854 | 0.78635 | false |
| AUDJPY | SHORT | 3/3 | -1 | -1 | 50.02 | 32.81 | 1 WAIT BREAK | 106.872 | 106.988 | false |
| AUDCHF | SHORT | 3/3 | 1 | 1 | 18.83 | 12.82 | 1 WAIT BREAK | 0.56448 | 0.56622 | false |
| AUDUSD | SHORT | 3/3 | -1 | -1 | 57.73 | 35.05 | 5 WAIT NEW RETEST | 0.67201 | 0.67128 | false |
| AUDNZD | SHORT | 3/3 | -1 | -1 | 32.52 | 31.27 | 4 READY | 1.22304 | 1.22322 | true |
| USDCHF | LONG | 3/3 | 0 | 1 | 38.35 | 21.18 | 5 WAIT NEW RETEST | 0.84152 | 0.84352 | false |
| NZDUSD | SHORT | 3/3 | -1 | -1 | 35.11 | 23.24 | 1 WAIT BREAK | 0.5482 | 0.54878 | false |
| CADCHF | LONG | 3/3 | -1 | 1 | 24.7 | 11.54 | 1 WAIT BREAK | 0.58965 | 0.58866 | false |
| USDCAD | LONG | 3/3 | 0 | 1 | 41.57 | 20.39 | 5 WAIT NEW RETEST | 1.43164 | 1.43316 | false |
| GBPUSD | SHORT | 3/3 | 0 | 0 | 46.38 | 44.86 | 5 WAIT NEW RETEST | 1.31732 | 1.31462 | false |

**BRC:** 0 NO ALIGNMENT · 1 WAIT BREAK · 2 BREAK · 3 RETEST · 4 READY · 5 WAIT NEW RETEST.

- **NZDCAD:** WATCH / NO TV READY / BRC WAIT BREAK; D1/H4 structure mismatch; ADX below 20.
- **AUDJPY:** WATCH / NO TV READY / BRC WAIT BREAK.
- **AUDCHF:** WATCH / NO TV READY / BRC WAIT BREAK; D1/H4 structure mismatch; ADX below 20.
- **AUDUSD:** WATCH / NO TV READY / BRC WAIT NEW RETEST.
- **AUDNZD:** TV READY / REQUIRES YAHOO-OANDA SAME H1 DIRECTION ZONE AGREEMENT.
- **USDCHF:** WATCH / NO TV READY / BRC WAIT NEW RETEST; D1/H4 structure mismatch.
- **NZDUSD:** WATCH / NO TV READY / BRC WAIT BREAK.
- **CADCHF:** WATCH / NO TV READY / BRC WAIT BREAK; D1/H4 structure mismatch; ADX below 20.
- **USDCAD:** WATCH / NO TV READY / BRC WAIT NEW RETEST; D1/H4 structure mismatch.
- **GBPUSD:** WATCH / NO TV READY / BRC WAIT NEW RETEST; D1/H4 structure mismatch.

## Κανόνας τελικού READY

READY ισχύει μόνο όταν συμφωνούν η ανεξάρτητη TradingView Pine audit και το υπάρχον Yahoo/OANDA Trend BRC για το **ΙΔΙΟ κλεισμένο H1, direction και zone**. Το tv_ready=true σημαίνει επιτυχία των ανεξάρτητων Pine φίλτρων· δεν αποτελεί από μόνο του επιβεβαιωμένο trade ή τελικό Trend READY. Η τελική απόφαση βρίσκεται στο [LATEST_FOREX_SCAN.md](LATEST_FOREX_SCAN.md), μετά το νέο scan.

Το tv_ready=true απαιτεί success=true, ακριβές OANDA symbol και ταυτοποιημένο δείκτη, κλεισμένο ωριαίο last_values με ηλικία κλεισίματος 0–2 ώρες (ανοχή 2 λεπτών), verified_ready=1, BRC=4, EMA=3/3, ίδια direction σε D1/H4 structure, ADX H4/H1 ≥20, θετικά πεπερασμένα zone/entry/SL/TP, σωστό προσανατολισμό SL/TP και RR ≥1.2. Ελέγχθηκε επίσης το RR από τις ίδιες τιμές entry/stop/target.

Για όλα τα tv_ready=false, Entry/SL/TP/RR παραμένουν null. Το [JSON snapshot](TRADINGVIEW_BRC_VERIFIED.json) κρατά μόνο παράγωγα audit signals και τις πλήρεις αριθμητικές τιμές που επέστρεψε το Pine· δεν δημοσιεύονται raw OHLC candles.

Η ενημέρωση JSON εκκινεί νέο scan για το τελικό gate. Η ολοκλήρωση επαληθεύεται χωριστά μέσω workflow και νέας εγγραφής υγείας. Το Trend audit δεν επιβεβαιώνει HTF Reversal, δεν ενεργοποιεί READY alerts και δεν δίνει εντολές συναλλαγών.
