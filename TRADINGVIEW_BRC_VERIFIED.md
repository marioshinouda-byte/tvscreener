# TradingView BRC — ανεξάρτητος ωριαίος έλεγχος Trend

**Ώρα Ελλάδας:** 21/11/2026, 03:27:25 (Europe/Athens)  
**UTC:** 2026-11-21T01:27:25Z  
**Κατάσταση:** PARTIAL TV ACCESS / STALE H1 / TV UNAVAILABLE / NO TV READY.

Πραγματοποιήθηκαν και οι 7 απαιτούμενες κλήσεις TradingView. Οι 3 (AUDUSD, AUDCHF, AUDJPY) ολοκληρώθηκαν επιτυχώς με ακριβές σύμβολο OANDA και ταυτοποιημένο δείκτη από `script_id` και `metainfo.plots`. Οι 4 (AUDCAD, EURJPY, AUDNZD, EURAUD) μπλοκαρίστηκαν πριν από την εκτέλεση: η AUDCAD επέστρεψε `TOOL_QUOTA_EXCEEDED` λόγω ημερήσιου ορίου και cooldown 10 λεπτών, ενώ οι υπόλοιπες ενεργό cooldown. Για τις αποτυχημένες κλήσεις δεν επιστράφηκαν `metainfo` ή `last_values` και δεν επαναχρησιμοποιήθηκαν τιμές προηγούμενου audit.

Στις 3 επιτυχείς κλήσεις χρησιμοποιήθηκαν αποκλειστικά οι παράγωγες τιμές του `last_values`, όχι το forming candle από `values[]`. Η τελευταία κλεισμένη H1 έχει **άνοιγμα 20/11/2026 21:00 UTC και κλείσιμο 20/11/2026 22:00 UTC** (21/11/2026 00:00 ώρα Ελλάδας). Στον έλεγχο 2026-11-21T01:26:11Z η ηλικία από το κλείσιμο ήταν 3 ώρες και 26 λεπτά, πέρα από το όριο 2 ωρών και την ανοχή 2 λεπτών. Αυτές είναι πραγματικές τιμές της συγκεκριμένης παλαιότερης H1, όχι νέο H1. Το Pine επέστρεψε `verified_ready=0` και στις 3 διαθέσιμες αποκρίσεις. Δεν επιβεβαιώθηκε TradingView READY σε κανένα ζευγάρι.

**Ζητούμενος δείκτης:** BRC TV Triple TF Audit v1 — `USER;ae27f010fee5413b8f5d1cc39e592cde`. Η version 1.0 ταυτοποιήθηκε στις επιτυχείς αποκρίσεις.  
**Παράμετροι ανά ζευγάρι:** `OANDA:PAIR` · `timeframe=1h` · `calc_bars_count=500` · `return_bars=1`.  
**Πηγή παραγώγων όταν είναι διαθέσιμα:** TradingView Pine. Έλεγχος D1/H4/H1 με τον αποθηκευμένο δείκτη και προηγούμενα ολοκληρωμένα HTF κεριά.

## Κάλυψη από τα αρχεία εισόδου

- Report εισόδου: **Τελευταία ενημέρωση:** 21/11/2026 02:29 (Europe/Athens)
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
| AUDCAD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: daily usage limit; MCP cooldown 10 minutes |
| EURJPY | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |
| AUDNZD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |
| EURAUD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |

Τα ADX του πίνακα εμφανίζονται με 2 δεκαδικά· το JSON διατηρεί την πλήρη ακρίβεια της απόκρισης. Τα ουδέτερα structure (0) διατηρούνται όπως επιστράφηκαν. `UNKNOWN` και `—` δηλώνουν μη διαθέσιμα δεδομένα, με `null` στο JSON. Για κάθε `tv_ready=false`, Entry/SL/TP/RR παραμένουν `null`. Δημοσιεύονται μόνο παράγωγα audit signals και όχι πλήρη raw OHLC candles.

**BRC:** 0 NO ALIGNMENT · 1 WAIT BREAK · 2 BREAK · 3 RETEST · 4 READY · 5 WAIT NEW RETEST. Δεν αποδίδεται αριθμητικό στάδιο όταν το TradingView δεν το επέστρεψε.

## Κανόνας ανεξάρτητης επιβεβαίωσης

**READY ισχύει μόνο όταν συμφωνούν η TradingView Pine audit και το υπάρχον Yahoo/OANDA Trend BRC για το ΙΔΙΟ κλεισμένο H1, direction και zone.** Το GitHub READY μόνο του δεν επαρκεί. Το `tv_ready` αφορά το ανεξάρτητο σκέλος TradingView· το `tradingview_gate.py` διασταυρώνει τη συμφωνία με το Trend BRC.

Απαιτούνται επιτυχής κλήση, ακριβές σύμβολο και ταυτοποιημένος δείκτης, τελευταία κλεισμένη H1 από `last_values` με ηλικία από το κλείσιμο 0–2 ώρες (ανοχή έως 2 λεπτά), `verified_ready=1`, `brc_stage=4`, EMA 3/3, D1/H4 structure προς την ίδια κατεύθυνση, ADX H4/H1 ≥20, θετικές πεπερασμένες zone/Entry/SL/TP, σωστός προσανατολισμός SL/TP και RR ≥1.2. Το `h1_open_at` προκύπτει από το UTC unix timestamp `last_values.t`. Το `generated_at` είναι η πραγματική ώρα ενημέρωσης του snapshot και δεν αλλάζει την ηλικία της H1.

Το JSON push εκκινεί νέο fail-closed scan· η ολοκλήρωση ελέγχεται μετά το push από το workflow και νέα εγγραφή υγείας. Το Trend audit δεν επιβεβαιώνει HTF Reversal. Δεν ενεργοποιήθηκαν READY alerts και δεν δόθηκαν εντολές συναλλαγών.

[Τελευταίο report](LATEST_FOREX_SCAN.md) · [Snapshot JSON](TRADINGVIEW_BRC_VERIFIED.json)
