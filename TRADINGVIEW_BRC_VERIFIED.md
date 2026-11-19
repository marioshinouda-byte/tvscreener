# TradingView BRC — ανεξάρτητος ωριαίος έλεγχος Trend

**Ώρα Ελλάδας:** 19/11/2026, 23:28:31 (Europe/Athens)  
**UTC:** 2026-11-19T21:28:31Z  
**Κατάσταση:** TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED.

Το συνδεδεμένο TradingView MCP μπλόκαρε και τις 7 κλήσεις πριν από την εκτέλεση. Η πρώτη (AUDCAD) επέστρεψε ημερήσιο όριο χρήσης και cooldown 10 λεπτών, οι υπόλοιπες ενεργό cooldown. Δεν επιστράφηκαν metainfo ή last_values· δεν ταυτοποιήθηκε δείκτης από απόκριση και δεν επιβεβαιώθηκε TradingView READY.

**Ζητούμενος δείκτης:** BRC TV Triple TF Audit v1, `USER;ae27f010fee5413b8f5d1cc39e592cde`.  
**Παράμετροι:** OANDA:PAIR, timeframe=1h, calc_bars_count=500, return_bars=1.  
**Πηγή παραγώγων όταν είναι διαθέσιμα:** TradingView Pine.

## Κάλυψη

- Weekly Top 5: AUDCAD, AUDJPY, GBPAUD, AUDUSD, GBPUSD.
- OANDA Top 5: GBPUSD, AUDUSD, EURAUD, AUDCAD, AUDCHF.
- Trend TV UNVERIFIED / READY στο report εισόδου: κανένας.
- Πρόσθετοι εκτός πεντάδων: κανένας.
- Μοναδικά ζευγάρια: 7. Εξετάστηκαν όλες οι γραμμές Trend και ο πίνακας όλων των 28 Forex pairs. Crypto και HTF Reversal εξαιρούνται.

| Pair | Πηγή | H1 open UTC | Direction | EMA | D1/H4 | ADX H4/H1 | BRC | Zone | Κλεισμένη H1 τιμή | tv_ready | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AUDCAD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: daily usage limit; MCP cooldown 10 minutes |
| AUDJPY | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |
| GBPAUD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |
| AUDUSD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |
| GBPUSD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |
| EURAUD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |
| AUDCHF | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |

UNKNOWN σημαίνει μη διαθέσιμο BRC stage. Οι παύλες είναι null, όχι τιμές αγοράς. Δεν χρησιμοποιήθηκαν παλιά δεδομένα ή raw OHLC candles. Entry/SL/TP/RR είναι null για όλα τα tv_ready=false.

**BRC:** 0 NO ALIGNMENT · 1 WAIT BREAK · 2 BREAK · 3 RETEST · 4 READY · 5 WAIT NEW RETEST.

READY ισχύει μόνο όταν συμφωνούν η ανεξάρτητη TradingView Pine audit και το Yahoo/OANDA Trend BRC για το **ΙΔΙΟ κλεισμένο H1, direction και zone**. Το GitHub READY μόνο του δεν αρκεί.

Το tv_ready=true απαιτεί success=true, ακριβές OANDA symbol και ταυτοποιημένο δείκτη, last_values από κλεισμένο H1 με ηλικία κλεισίματος 0–2 ώρες (ανοχή 2 λεπτών), verified_ready=1, BRC=4, EMA=3/3, ίδια direction σε D1/H4 structure, ADX H4/H1 ≥20, θετικά πεπερασμένα zone/entry/SL/TP, σωστό προσανατολισμό SL/TP και RR ≥1.2. Χρησιμοποιείται μόνο last_values, ποτέ forming candle του values[].

Το JSON push εκκινεί νέο fail-closed scan. Η ολοκλήρωση ελέγχεται μετά το push από το workflow και νέα εγγραφή υγείας. Το Trend audit δεν επιβεβαιώνει HTF Reversal, δεν ενεργοποιεί READY alerts και δεν δίνει εντολές συναλλαγών.

[Τελευταίο report](LATEST_FOREX_SCAN.md) · [Snapshot audit](TRADINGVIEW_BRC_VERIFIED.json)
