# TradingView BRC — ανεξάρτητος ωριαίος έλεγχος Trend

**Ώρα Ελλάδας:** 21/11/2026, 02:28:26 (Europe/Athens)  
**UTC:** 2026-11-21T00:28:26Z  
**Κατάσταση:** TV CONNECTED / STALE H1 / NO TV READY.

Και οι 7 κλήσεις TradingView ολοκληρώθηκαν επιτυχώς, με ακριβές σύμβολο OANDA και ταυτοποιημένο δείκτη από το `script_id` και τα `metainfo.plots`. Χρησιμοποιήθηκαν αποκλειστικά οι παράγωγες τιμές του `last_values`, όχι το forming candle από `values[]`.

Η τελευταία κλεισμένη H1 και στα 7 ζευγάρια έχει **άνοιγμα 20/11/2026 21:00 UTC και κλείσιμο 20/11/2026 22:00 UTC** (21/11/2026 00:00 ώρα Ελλάδας). Στον έλεγχο 2026-11-21T00:27:15Z η ηλικία από το κλείσιμο ήταν 2 ώρες και 27 λεπτά, πέρα από το όριο 2 ωρών και την ανοχή 2 λεπτών. Αυτές είναι πραγματικές τιμές της συγκεκριμένης παλαιότερης H1, όχι νέο H1 ή επιβεβαιωμένο READY. Το Pine επέστρεψε `verified_ready=0` σε όλα τα ζευγάρια.

**Δείκτης:** BRC TV Triple TF Audit v1 — `USER;ae27f010fee5413b8f5d1cc39e592cde`, version 1.0.  
**Παράμετροι ανά ζευγάρι:** `OANDA:PAIR` · `timeframe=1h` · `calc_bars_count=500` · `return_bars=1`.  
**Πηγή παραγώγων:** TradingView Pine. Έλεγχος D1/H4/H1 με τον αποθηκευμένο δείκτη και προηγούμενα ολοκληρωμένα HTF κεριά.

## Κάλυψη από τα αρχεία εισόδου

- Report εισόδου: **Τελευταία ενημέρωση:** 21/11/2026 01:29 (Europe/Athens)
- Weekly Top 5: AUDUSD, AUDCHF, AUDJPY, AUDCAD, EURJPY.
- OANDA Top 5: AUDNZD, EURAUD, AUDCAD, EURJPY, AUDJPY.
- Trend READY / TV UNVERIFIED: κανένα στο report εισόδου.
- Πρόσθετοι υποψήφιοι READY / TV UNVERIFIED εκτός πεντάδων: κανένας.
- Μοναδικά ζευγάρια: 7. Ελέγχθηκαν όλες οι γραμμές Trend και ο πίνακας των 28 Forex pairs. Crypto και HTF Reversal εξαιρούνται από το συγκεκριμένο Trend audit.

| Pair | Πηγή | H1 open UTC | Direction | EMA | D1/H4 structure | ADX H4/H1 | BRC | Zone | Κλεισμένη H1 τιμή | Pine verified_ready | tv_ready | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AUDUSD | TradingView Pine | 2026-11-20T21:00:00Z | SHORT | 3/3 | BEAR (-1) / BEAR (-1) | 54.75 / 38.63 | 2 BREAK | 0.66456 | 0.66198 | 0 | false | STALE H1 / NO TV READY: H1 close 2026-11-20T22:00:00Z exceeds 2h freshness limit (+2m tolerance); BRC=BREAK; verified_ready=0 |
| AUDCHF | TradingView Pine | 2026-11-20T21:00:00Z | SHORT | 3/3 | NEUTRAL (0) / BEAR (-1) | 29.65 / 56.99 | 5 WAIT NEW RETEST | 0.56202 | 0.55611 | 0 | false | STALE H1 / NO TV READY: H1 close 2026-11-20T22:00:00Z exceeds 2h freshness limit (+2m tolerance); BRC=WAIT NEW RETEST; verified_ready=0; D1/H4 structure not aligned |
| AUDJPY | TradingView Pine | 2026-11-20T21:00:00Z | SHORT | 3/3 | BEAR (-1) / BEAR (-1) | 46.60 / 51.17 | 5 WAIT NEW RETEST | 106.22 | 104.962 | 0 | false | STALE H1 / NO TV READY: H1 close 2026-11-20T22:00:00Z exceeds 2h freshness limit (+2m tolerance); BRC=WAIT NEW RETEST; verified_ready=0 |
| AUDCAD | TradingView Pine | 2026-11-20T21:00:00Z | SHORT | 3/3 | BEAR (-1) / BEAR (-1) | 49.23 / 51.44 | 5 WAIT NEW RETEST | 0.95278 | 0.94952 | 0 | false | STALE H1 / NO TV READY: H1 close 2026-11-20T22:00:00Z exceeds 2h freshness limit (+2m tolerance); BRC=WAIT NEW RETEST; verified_ready=0 |
| EURJPY | TradingView Pine | 2026-11-20T21:00:00Z | SHORT | 3/3 | BEAR (-1) / BEAR (-1) | 40.67 / 35.26 | 5 WAIT NEW RETEST | 174.442 | 173.912 | 0 | false | STALE H1 / NO TV READY: H1 close 2026-11-20T22:00:00Z exceeds 2h freshness limit (+2m tolerance); BRC=WAIT NEW RETEST; verified_ready=0 |
| AUDNZD | TradingView Pine | 2026-11-20T21:00:00Z | SHORT | 3/3 | BEAR (-1) / NEUTRAL (0) | 47.43 / 44.07 | 5 WAIT NEW RETEST | 1.21164 | 1.20998 | 0 | false | STALE H1 / NO TV READY: H1 close 2026-11-20T22:00:00Z exceeds 2h freshness limit (+2m tolerance); BRC=WAIT NEW RETEST; verified_ready=0; D1/H4 structure not aligned |
| EURAUD | TradingView Pine | 2026-11-20T21:00:00Z | LONG | 3/3 | BULL (1) / BULL (1) | 40.29 / 53.83 | 5 WAIT NEW RETEST | 1.65089 | 1.65681 | 0 | false | STALE H1 / NO TV READY: H1 close 2026-11-20T22:00:00Z exceeds 2h freshness limit (+2m tolerance); BRC=WAIT NEW RETEST; verified_ready=0 |

Τα ADX του πίνακα εμφανίζονται με 2 δεκαδικά· το JSON διατηρεί την πλήρη ακρίβεια της απόκρισης. Τα ουδέτερα structure (0) διατηρούνται όπως επιστράφηκαν. Για κάθε `tv_ready=false`, Entry/SL/TP/RR παραμένουν `null`. Δημοσιεύονται μόνο παράγωγα audit signals και όχι πλήρη raw OHLC candles.

**BRC:** 0 NO ALIGNMENT · 1 WAIT BREAK · 2 BREAK · 3 RETEST · 4 READY · 5 WAIT NEW RETEST.

## Κανόνας ανεξάρτητης επιβεβαίωσης

**READY ισχύει μόνο όταν συμφωνούν η TradingView Pine audit και το υπάρχον Yahoo/OANDA Trend BRC για το ΙΔΙΟ κλεισμένο H1, direction και zone.** Το GitHub READY μόνο του δεν επαρκεί. Το `tv_ready` αφορά το ανεξάρτητο σκέλος TradingView· το `tradingview_gate.py` διασταυρώνει τη συμφωνία με το Trend BRC.

Απαιτούνται επιτυχής κλήση, ακριβές σύμβολο και ταυτοποιημένος δείκτης, τελευταία κλεισμένη H1 από `last_values` με ηλικία από το κλείσιμο 0–2 ώρες (ανοχή έως 2 λεπτά), `verified_ready=1`, `brc_stage=4`, EMA 3/3, D1/H4 structure προς την ίδια κατεύθυνση, ADX H4/H1 ≥20, θετικές πεπερασμένες zone/Entry/SL/TP, σωστός προσανατολισμός SL/TP και RR ≥1.2. Το `h1_open_at` προκύπτει από το UTC unix timestamp `last_values.t`. Το `generated_at` είναι η πραγματική ώρα ενημέρωσης του snapshot και δεν αλλάζει την ηλικία της H1.

Το JSON push εκκινεί νέο fail-closed scan· η ολοκλήρωση ελέγχεται μετά το push από το workflow και νέα εγγραφή υγείας. Το Trend audit δεν επιβεβαιώνει HTF Reversal. Δεν ενεργοποιήθηκαν READY alerts και δεν δόθηκαν εντολές συναλλαγών.

[Τελευταίο report](LATEST_FOREX_SCAN.md) · [Snapshot JSON](TRADINGVIEW_BRC_VERIFIED.json)
