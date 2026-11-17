# TradingView — ανεξάρτητος ωριαίος έλεγχος Trend BRC

**Ώρα Ελλάδας:** 17/11/2026, 14:27:08 (Europe/Athens)  
**Έλεγχος UTC:** 2026-11-17T12:27:08Z  
**Πηγή:** TradingView Pine · OANDA · BRC TV Triple TF Audit v1, version 1.0.  
**Script ID:** `USER;ae27f010fee5413b8f5d1cc39e592cde`

**Κάλυψη: 9 μοναδικά ζευγάρια.** Weekly Top 5: EURAUD, CHFJPY, NZDCAD, AUDJPY, GBPJPY. OANDA Top 5: CHFJPY, EURUSD, EURJPY, CADJPY, NZDJPY. Πρόσθετα Trend TV UNVERIFIED / A+ READY στο αναγνωσμένο report: κανένα.

**Αποτέλεσμα: 0 TV READY.** Η σύνδεση και η ταυτότητα του δείκτη επιβεβαιώθηκαν για όλα τα ζευγάρια.

Χρησιμοποιήθηκε μόνο το `last_values` του εργαλείου, δηλαδή το τελευταίο κλεισμένο H1, όχι το forming candle του `values[]`. D1/H4: μόνο προηγούμενα ολοκληρωμένα HTF κεριά από τον αποθηκευμένο δείκτη. Η ηλικία μετριέται από το κλείσιμο H1 (άνοιγμα + 1 ώρα), με αποδεκτό εύρος 0–2 ώρες και ανοχή 2 λεπτών.

| Pair | TV direction | EMA | D1 / H4 δομή | ADX H4 / H1 | BRC | Zone | Κλεισμένο H1 close | H1 open UTC | H1 close UTC | TV READY | Status / αιτία |
|---|---|---:|---|---|---|---:|---:|---|---|---|---|
| EURAUD | LONG | 3/3 | 1 / 1 | 43.69 / 33.06 | WAIT NEW RETEST | 1.63262 | 1.63031 | 2026-11-17T11:00:00.000Z | 2026-11-17T12:00:00.000Z | NO | WATCH / NO TV READY: WAIT NEW RETEST |
| CHFJPY | SHORT | 3/3 | 0 / -1 | 49.47 / 31.19 | WAIT NEW RETEST | 189.752 | 189.526 | 2026-11-17T11:00:00.000Z | 2026-11-17T12:00:00.000Z | NO | WATCH / NO TV READY: WAIT NEW RETEST; D1/H4 structure not aligned |
| NZDCAD | SHORT | 3/3 | 0 / -1 | 16.81 / 30.71 | WAIT BREAK | 0.78471 | 0.78628 | 2026-11-17T11:00:00.000Z | 2026-11-17T12:00:00.000Z | NO | WATCH / NO TV READY: WAIT BREAK; D1/H4 structure not aligned; ADX below 20 or missing |
| AUDJPY | SHORT | 3/3 | -1 / -1 | 52.63 / 64.20 | WAIT NEW RETEST | 107.586 | 107.350 | 2026-11-17T11:00:00.000Z | 2026-11-17T12:00:00.000Z | NO | WATCH / NO TV READY: WAIT NEW RETEST |
| GBPJPY | SHORT | 3/3 | 0 / -1 | 49.91 / 40.68 | WAIT NEW RETEST | 210.820 | 210.039 | 2026-11-17T11:00:00.000Z | 2026-11-17T12:00:00.000Z | NO | WATCH / NO TV READY: WAIT NEW RETEST; D1/H4 structure not aligned |
| EURUSD | SHORT | 3/3 | 0 / -1 | 43.31 / 26.56 | WAIT BREAK | 1.09850 | 1.09914 | 2026-11-17T11:00:00.000Z | 2026-11-17T12:00:00.000Z | NO | WATCH / NO TV READY: WAIT BREAK; D1/H4 structure not aligned |
| EURJPY | SHORT | 3/3 | 0 / -1 | 51.12 / 49.41 | WAIT NEW RETEST | 176.245 | 175.010 | 2026-11-17T11:00:00.000Z | 2026-11-17T12:00:00.000Z | NO | WATCH / NO TV READY: WAIT NEW RETEST; D1/H4 structure not aligned |
| CADJPY | SHORT | 3/3 | -1 / -1 | 43.88 / 36.66 | WAIT NEW RETEST | 111.832 | 111.362 | 2026-11-17T11:00:00.000Z | 2026-11-17T12:00:00.000Z | NO | WATCH / NO TV READY: WAIT NEW RETEST |
| NZDJPY | SHORT | 3/3 | -1 / 0 | 40.02 / 59.55 | WAIT NEW RETEST | 88.389 | 87.560 | 2026-11-17T11:00:00.000Z | 2026-11-17T12:00:00.000Z | NO | WATCH / NO TV READY: WAIT NEW RETEST; D1/H4 structure not aligned |

**READY ισχύει μόνο όταν συμφωνούν η ανεξάρτητη TradingView Pine audit και το υπάρχον Yahoo/OANDA Trend BRC για το ΙΔΙΟ κλεισμένο H1, direction και zone.** Το scanner gate διασταυρώνει επίσης την τιμή, τη φρεσκάδα και το RR. Το τρέχον GitHub READY από μόνο του δεν είναι επαληθευμένο.

TV READY απαιτεί: success=true, ακριβές OANDA symbol και αναγνωρισμένο script/plots, πρόσφατο κλεισμένο H1, verified_ready=1, BRC stage=4, EMA50 3/3, D1/H4 δομή προς την ίδια κατεύθυνση, ADX H4/H1 ≥20, θετικά πεπερασμένα zone/Entry/SL/TP, σωστό προσανατολισμό SL/TP και RR≥1.2. Διαφωνία, ελλιπή ή παλιά δεδομένα σημαίνουν tv_ready=false. Για tv_ready=false τα Entry/SL/TP/RR παραμένουν null στο JSON.

**BRC:** 0 NO ALIGNMENT · 1 WAIT BREAK · 2 BREAK · 3 RETEST · 4 READY · 5 WAIT NEW RETEST. **Δομή:** 1 BULL, −1 BEAR, 0 χωρίς επιβεβαιωμένη κατεύθυνση. WATCH/BREAK/RETEST δεν είναι READY.

[LATEST_FOREX_SCAN.md](https://github.com/marioshinouda-byte/tvscreener/blob/main/LATEST_FOREX_SCAN.md) · [TRADINGVIEW_BRC_VERIFIED.json](https://github.com/marioshinouda-byte/tvscreener/blob/main/TRADINGVIEW_BRC_VERIFIED.json)

Πεδίο ελέγχου: αποκλειστικά Trend BRC. Το ξεχωριστό HTF Reversal δεν επαληθεύεται εδώ και BTC/ETH/SOL αποκλείονται. Δημοσιεύονται μόνο παράγωγες ενδείξεις, χωρίς πλήρη raw OHLC. Δεν δίνονται εντολές συναλλαγών ούτε ενεργοποιούνται READY alerts. Η ολοκλήρωση του νέου scanner workflow ελέγχεται χωριστά μετά το JSON push.
