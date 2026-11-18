# TradingView BRC — ανεξάρτητος ωριαίος έλεγχος Trend

**Ώρα Ελλάδας:** 18/11/2026, 02:30:25 (Europe/Athens)  
**UTC:** 2026-11-18T00:30:25Z  
**Πηγή:** TradingView Pine, μέσω του συνδεδεμένου TradingView MCP.  
**Pine κλήσεις:** 10/10 επιτυχείς. **TV READY:** 0.

Επαληθεύτηκαν το ακριβές OANDA symbol, ο αποθηκευμένος δείκτης, το timeframe και η αντιστοίχιση `metainfo.plots` για κάθε ζευγάρι. Χρησιμοποιήθηκαν αποκλειστικά τα `last_values` της τελευταίας κλεισμένης H1 μπάρας. Το forming candle του `values[]` αγνοήθηκε.

**Δείκτης:** BRC TV Triple TF Audit v1 — `USER;ae27f010fee5413b8f5d1cc39e592cde`, version 1.0. Κάθε κλήση: `OANDA:PAIR`, timeframe `1h`, calc_bars_count `500`, return_bars `1`. Οι D1/H4 ενδείξεις υπολογίζονται από τον αποθηκευμένο δείκτη με ολοκληρωμένα HTF κεριά.

**Κλεισμένο H1 (open → close UTC):** 2026-11-17T23:00:00.000Z → 2026-11-18T00:00:00.000Z. Κατά την επικύρωση, η ηλικία κλεισίματος ήταν 29.1 λεπτά και ήταν εντός 0–2 ωρών για όλα τα ζευγάρια (ανοχή 2 λεπτών).

## Κάλυψη

- Εβδομαδιαίο Top 5: NZDCAD, AUDJPY, GBPJPY, AUDCHF, AUDUSD.
- OANDA screener Top 5: USDCHF, EURGBP, USDCAD, EURUSD, CADCHF.
- Επιπλέον Trend BRC=TV UNVERIFIED ή A+ READY στο αναγνωσμένο GitHub report: κανένα.
- Σύνολο 10 μοναδικά Forex ζευγάρια. Bitcoin/ETH/SOL και HTF Reversal εξαιρούνται από το συγκεκριμένο Trend audit.

## Ανεξάρτητος πίνακας audit

| Ζευγάρι | Πηγή | Κλεισμένο H1 open UTC | Direction | EMA /3 | D1 / H4 structure | ADX H4 / H1 | BRC | Zone | Κλείσιμο H1 | tv_ready | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NZDCAD | TradingView Pine | 2026-11-17T23:00:00Z | SHORT | 3/3 | 0 / -1 | 20.85 / 33.99 | 1 WAIT BREAK | 0.7842 | 0.78608 | false | WATCH / NO TV READY: WAIT BREAK; D1/H4 structure not aligned |
| AUDJPY | TradingView Pine | 2026-11-17T23:00:00Z | SHORT | 3/3 | -1 / -1 | 53.46 / 42.22 | 1 WAIT BREAK | 106.872 | 107.508 | false | WATCH / NO TV READY: WAIT BREAK |
| GBPJPY | TradingView Pine | 2026-11-17T23:00:00Z | SHORT | 2/3 | 0 / -1 | 51.00 / 23.86 | 1 WAIT BREAK | 209.58 | 210.633 | false | WATCH / NO TV READY: WAIT BREAK; EMA 2/3; D1/H4 structure not aligned |
| AUDCHF | TradingView Pine | 2026-11-17T23:00:00Z | SHORT | 2/3 | 0 / 0 | 25.85 / 31.28 | 1 WAIT BREAK | 0.56376 | 0.56706 | false | WATCH / NO TV READY: WAIT BREAK; EMA 2/3; D1/H4 structure not aligned |
| AUDUSD | TradingView Pine | 2026-11-17T23:00:00Z | SHORT | 3/3 | -1 / -1 | 56.74 / 31.08 | 1 WAIT BREAK | 0.67201 | 0.67396 | false | WATCH / NO TV READY: WAIT BREAK |
| USDCHF | TradingView Pine | 2026-11-17T23:00:00Z | LONG | 3/3 | 0 / 1 | 34.51 / 12.61 | 1 WAIT BREAK | 0.84152 | 0.84137 | false | WATCH / NO TV READY: WAIT BREAK; D1/H4 structure not aligned; ADX H4/H1 below 20 or missing |
| EURGBP | TradingView Pine | 2026-11-17T23:00:00Z | SHORT | 3/3 | 0 / -1 | 26.86 / 29.45 | 1 WAIT BREAK | 0.83244 | 0.8325 | false | WATCH / NO TV READY: WAIT BREAK; D1/H4 structure not aligned |
| USDCAD | TradingView Pine | 2026-11-17T23:00:00Z | LONG | 3/3 | 0 / 0 | 44.27 / 23.85 | 1 WAIT BREAK | 1.43164 | 1.42999 | false | WATCH / NO TV READY: WAIT BREAK; D1/H4 structure not aligned |
| EURUSD | TradingView Pine | 2026-11-17T23:00:00Z | SHORT | 3/3 | 0 / -1 | 43.01 / 22.84 | 1 WAIT BREAK | 1.0968 | 1.09926 | false | WATCH / NO TV READY: WAIT BREAK; D1/H4 structure not aligned |
| CADCHF | TradingView Pine | 2026-11-17T23:00:00Z | LONG | 3/3 | -1 / 1 | 20.94 / 16.95 | 5 WAIT NEW RETEST | 0.58784 | 0.58842 | false | WATCH / NO TV READY: WAIT NEW RETEST; D1/H4 structure not aligned; ADX H4/H1 below 20 or missing |

D1/H4 structure: 1 = ανοδική, -1 = καθοδική, 0 = μη καθορισμένη κατεύθυνση δομής. ADX εμφανίζεται με 2 δεκαδικά· το JSON διατηρεί τις επιστραφείσες τιμές χωρίς στρογγυλοποίηση.

BRC: 0 = NO ALIGNMENT, 1 = WAIT BREAK, 2 = BREAK, 3 = RETEST, 4 = READY, 5 = WAIT NEW RETEST.

Κανένα ζευγάρι δεν έχει TV READY. Τα Entry/SL/TP/RR παραμένουν null σε όλα τα ζευγάρια με tv_ready=false. Δημοσιεύονται μόνο παράγωγα audit signals, όχι raw OHLC candles.

## Κανόνας READY

READY ισχύει μόνο όταν συμφωνούν η ανεξάρτητη TradingView Pine audit και το υπάρχον Yahoo/OANDA Trend BRC για **το ίδιο κλεισμένο H1, την ίδια direction και την ίδια zone**. Το GitHub READY μόνο του δεν αρκεί.

Η Pine audit απαιτεί επιτυχή κλήση με ταυτοποιημένο δείκτη και σωστό symbol, κλεισμένο H1 ηλικίας 0–2 ωρών (ανοχή 2 λεπτών), verified_ready=1, BRC=4, EMA=3/3, D1/H4 structure προς ίδια κατεύθυνση, ADX H4/H1 ≥20, πεπερασμένα θετικά zone/entry/SL/TP, σωστό προσανατολισμό SL/TP και RR≥1.2. Ελέγχεται επίσης το RR που προκύπτει από Entry/SL/TP.

Το συνοδευτικό JSON push ζητά νέο scan και διασταύρωση μέσω του υπάρχοντος tradingview_gate.py. Η ολοκλήρωση της νέας εκτέλεσης επαληθεύεται χωριστά μέσω GitHub Actions και νέας εγγραφής υγείας· η δημοσίευση του audit δεν την αποδεικνύει.

[Τελευταίο GitHub report](LATEST_FOREX_SCAN.md) · [Machine-readable audit](TRADINGVIEW_BRC_VERIFIED.json)

Αφορά μόνο Trend. Δεν επιβεβαιώνει HTF Reversal, δεν δίνει εντολές συναλλαγών και δεν ενεργοποιεί READY alerts.
