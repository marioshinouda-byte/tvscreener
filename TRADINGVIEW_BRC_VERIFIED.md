# TradingView — ανεξάρτητος έλεγχος Trend BRC

**Ώρα Ελλάδας:** 17/11/2026, 15:25:58 (Europe/Athens)  
**Έλεγχος UTC:** 2026-11-17T13:25:58Z  
**Πηγή:** TradingView Pine · OANDA · BRC TV Triple TF Audit v1, version 1.0.  
**Script ID:** `USER;ae27f010fee5413b8f5d1cc39e592cde`

**Κάλυψη: 9 μοναδικά ζευγάρια.** Weekly Top 5: EURAUD, CHFJPY, NZDCAD, AUDJPY, GBPJPY. OANDA Top 5: AUDCAD, EURUSD, CHFJPY, EURCAD, USDCHF. Επιπλέον Trend TV UNVERIFIED / A+ READY: κανένα στο αναγνωσμένο report.

**Αποτέλεσμα: 0 TV READY.** Η σύνδεση και η ταυτότητα του δείκτη επιβεβαιώθηκαν για όλα τα ζευγάρια.

Αποκλειστικά `last_values` (τελευταίο ΚΛΕΙΣΜΕΝΟ H1), ποτέ forming candle από `values[]`. Τα D1/H4 είναι προηγούμενα ολοκληρωμένα κεριά από τον δείκτη. Ηλικία από το κλείσιμο H1 = άνοιγμα + 1 ώρα: 0–2 ώρες, με ανοχή 2 λεπτών.

| Pair | Direction | EMA | D1/H4 δομή | ADX H4/H1 | BRC | Zone | H1 close price | H1 open UTC | H1 close UTC | TV READY | Status / αιτία |
|---|---|---:|---|---|---|---:|---:|---|---|---|---|
| EURAUD | LONG | 3/3 | 1/1 | 43.69/31.54 | WAIT NEW RETEST | 1.63262 | 1.63218 | 2026-11-17T12:00:00.000Z | 2026-11-17T13:00:00.000Z | NO | WATCH / NO TV READY: WAIT NEW RETEST |
| CHFJPY | SHORT | 3/3 | 0/-1 | 49.47/31.88 | WAIT NEW RETEST | 189.752 | 189.668 | 2026-11-17T12:00:00.000Z | 2026-11-17T13:00:00.000Z | NO | WATCH / NO TV READY: WAIT NEW RETEST; D1/H4 structure not aligned |
| NZDCAD | SHORT | 3/3 | 0/-1 | 16.81/31.18 | WAIT BREAK | 0.78471 | 0.78584 | 2026-11-17T12:00:00.000Z | 2026-11-17T13:00:00.000Z | NO | WATCH / NO TV READY: WAIT BREAK; D1/H4 structure not aligned; ADX below 20 or missing |
| AUDJPY | SHORT | 3/3 | -1/-1 | 52.63/63.09 | WAIT NEW RETEST | 107.586 | 107.273 | 2026-11-17T12:00:00.000Z | 2026-11-17T13:00:00.000Z | NO | WATCH / NO TV READY: WAIT NEW RETEST |
| GBPJPY | SHORT | 3/3 | 0/-1 | 49.91/38.89 | WAIT NEW RETEST | 210.820 | 210.184 | 2026-11-17T12:00:00.000Z | 2026-11-17T13:00:00.000Z | NO | WATCH / NO TV READY: WAIT NEW RETEST; D1/H4 structure not aligned |
| AUDCAD | SHORT | 3/3 | -1/-1 | 41.86/39.13 | WAIT NEW RETEST | 0.96352 | 0.96254 | 2026-11-17T12:00:00.000Z | 2026-11-17T13:00:00.000Z | NO | WATCH / NO TV READY: WAIT NEW RETEST |
| EURUSD | SHORT | 3/3 | 0/-1 | 43.31/27.45 | WAIT BREAK | 1.09850 | 1.09927 | 2026-11-17T12:00:00.000Z | 2026-11-17T13:00:00.000Z | NO | WATCH / NO TV READY: WAIT BREAK; D1/H4 structure not aligned |
| EURCAD | SHORT | 3/3 | 1/-1 | 22.23/20.62 | RETEST | 1.57164 | 1.57105 | 2026-11-17T12:00:00.000Z | 2026-11-17T13:00:00.000Z | NO | WATCH / NO TV READY: RETEST; D1/H4 structure not aligned |
| USDCHF | LONG | 3/3 | 0/0 | 35.88/11.78 | WAIT BREAK | 0.84136 | 0.83977 | 2026-11-17T12:00:00.000Z | 2026-11-17T13:00:00.000Z | NO | WATCH / NO TV READY: WAIT BREAK; D1/H4 structure not aligned; ADX below 20 or missing |

**READY ισχύει μόνο όταν συμφωνούν η ανεξάρτητη TradingView Pine audit και το υπάρχον Yahoo/OANDA Trend BRC για το ΙΔΙΟ κλεισμένο H1, direction και zone.** Το GitHub READY από μόνο του δεν είναι επαληθευμένο. Το gate ελέγχει επίσης συμφωνία τιμής και RR.

Το TV READY απαιτεί success=true, ακριβές symbol/indicator/plots, πρόσφατο κλεισμένο H1, verified_ready=1, brc_stage=4, EMA50 3/3, ίδια κατεύθυνση D1/H4 structure, ADX H4/H1≥20, θετικά πεπερασμένα zone/Entry/SL/TP, σωστό προσανατολισμό SL/TP και RR≥1.2. Διαφωνία, έλλειψη ή παλαιότητα κρατά tv_ready=false. Για false τα Entry/SL/TP/RR παραμένουν null στο JSON.

**BRC:** 0 NO ALIGNMENT · 1 WAIT BREAK · 2 BREAK · 3 RETEST · 4 READY · 5 WAIT NEW RETEST. **Δομή:** 1 BULL, −1 BEAR, 0 χωρίς επιβεβαιωμένη κατεύθυνση. WATCH/BREAK/RETEST δεν είναι READY.

[LATEST_FOREX_SCAN.md](https://github.com/marioshinouda-byte/tvscreener/blob/main/LATEST_FOREX_SCAN.md) · [Snapshot JSON](https://github.com/marioshinouda-byte/tvscreener/blob/main/TRADINGVIEW_BRC_VERIFIED.json)

Μόνο Trend audit: δεν επαληθεύεται το ξεχωριστό HTF Reversal και δεν περιλαμβάνονται BTC/ETH/SOL. Μόνο παράγωγες ενδείξεις, χωρίς πλήρη raw OHLC. Δεν δίνονται εντολές συναλλαγών και δεν ενεργοποιούνται READY alerts. Η ολοκλήρωση του νέου scanner workflow επαληθεύεται χωριστά μετά το JSON push.
