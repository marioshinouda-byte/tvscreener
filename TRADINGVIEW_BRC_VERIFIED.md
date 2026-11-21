# TradingView BRC — ανεξάρτητος ωριαίος έλεγχος Trend

**Ώρα Ελλάδας:** 21/11/2026, 10:31:58 (Europe/Athens)  
**UTC:** 2026-11-21T08:31:58Z  
**Κατάσταση:** TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED.

Και οι 5 απαιτούμενες κλήσεις μπλοκαρίστηκαν πριν από την εκτέλεση. Η πρώτη (AUDNZD) επέστρεψε ημερήσιο όριο χρήσης και cooldown 10 λεπτών· οι υπόλοιπες ενεργό cooldown. Δεν επιστράφηκαν `metainfo` ή `last_values`, δεν ταυτοποιήθηκε δείκτης από απόκριση και δεν επιβεβαιώθηκε TradingView READY.

**Ζητούμενος δείκτης:** BRC TV Triple TF Audit v1 — `USER;ae27f010fee5413b8f5d1cc39e592cde`.  
**Παράμετροι ανά ζευγάρι:** `OANDA:PAIR` · `timeframe=1h` · `calc_bars_count=500` · `return_bars=1`.  
**Πηγή παραγώγων όταν είναι διαθέσιμα:** TradingView Pine.

## Κάλυψη από τα αρχεία εισόδου

- Report εισόδου: **Τελευταία ενημέρωση:** 21/11/2026 09:31 (Europe/Athens)
- Weekly Top 5 (2026-W47): **κενό στο τρέχον [WEEKLY_FOREX_TOP5.json](WEEKLY_FOREX_TOP5.json)** (`top5=[]`, `hot_new=[]`). Το report εισόδου απορρίπτει 28/28 Forex pairs ως `YF-STALE`.
- OANDA Top 5: AUDNZD, EURAUD, AUDCAD, EURJPY, AUDJPY. Και οι 5 γραμμές του shortlist εισόδου έχουν feed status `STALE`.
- Trend READY / TV UNVERIFIED: κανένα στο report εισόδου.
- Πρόσθετοι υποψήφιοι READY / TV UNVERIFIED εκτός πεντάδων: κανένας.
- Μοναδικά ζευγάρια προς audit: 5. Ελέγχθηκαν όλες οι γραμμές Trend και ο πίνακας των 28 Forex pairs. Η λίστα βασίζεται στα τρέχοντα αρχεία εισόδου. Crypto και HTF Reversal εξαιρούνται.

| Pair | Πηγή | H1 open UTC | Direction | EMA | D1/H4 | ADX H4/H1 | BRC | Zone | Κλεισμένη H1 τιμή | tv_ready | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AUDNZD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: daily usage limit; MCP cooldown 10 minutes |
| EURAUD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |
| AUDCAD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |
| EURJPY | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |
| AUDJPY | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |

`UNKNOWN` και `—` δηλώνουν μη διαθέσιμα δεδομένα, με `null` στο JSON. Δεν επαναχρησιμοποιήθηκαν τιμές προηγούμενου audit ούτε παρουσιάστηκαν παλιά δεδομένα ως νέα. Για κάθε `tv_ready=false`, Entry/SL/TP/RR παραμένουν `null`. Δημοσιεύονται μόνο παράγωγα audit signals, όχι πλήρη raw OHLC candles.

**BRC:** 0 NO ALIGNMENT · 1 WAIT BREAK · 2 BREAK · 3 RETEST · 4 READY · 5 WAIT NEW RETEST. Δεν αποδίδεται αριθμητικό στάδιο χωρίς απόκριση TradingView.

## Κανόνας ανεξάρτητης επιβεβαίωσης

**READY ισχύει μόνο όταν συμφωνούν η TradingView Pine audit και το υπάρχον Yahoo/OANDA Trend BRC για το ΙΔΙΟ κλεισμένο H1, direction και zone.** Το GitHub READY μόνο του δεν επαρκεί. Το `tradingview_gate.py` ελέγχει τη συμφωνία των δύο σκελών.

Το ανεξάρτητο `tv_ready=true` απαιτεί επιτυχή κλήση, ακριβές σύμβολο και ταυτοποιημένο δείκτη, τελευταία κλεισμένη H1 από `last_values` με ηλικία κλεισίματος 0–2 ώρες (ανοχή έως 2 λεπτά), `verified_ready=1`, `brc_stage=4`, EMA 3/3, D1/H4 structure προς την ίδια κατεύθυνση, ADX H4/H1 ≥20, θετικές πεπερασμένες zone/Entry/SL/TP, σωστό προσανατολισμό SL/TP και RR ≥1.2. Το `h1_open_at` είναι UTC ISO8601 από το unix seconds `last_values.t`. Δεν χρησιμοποιείται το forming candle από `values[]`. Το `generated_at` είναι η πραγματική ώρα ενημέρωσης του snapshot.

Το JSON push εκκινεί νέο fail-closed scan· η ολοκλήρωση ελέγχεται μέσω workflow και νέας εγγραφής υγείας. Το Trend audit δεν επιβεβαιώνει HTF Reversal. Δεν ενεργοποιήθηκαν READY alerts και δεν δόθηκαν εντολές συναλλαγών.

[Τελευταίο report](LATEST_FOREX_SCAN.md) · [Snapshot JSON](TRADINGVIEW_BRC_VERIFIED.json)
