# TradingView BRC — ανεξάρτητος ωριαίος έλεγχος Trend

**Ώρα Ελλάδας:** 19/11/2026, 03:31:52 (Europe/Athens)  
**UTC:** 2026-11-19T01:31:52Z  
**Κατάσταση:** TV UNAVAILABLE / WEEKLY WATCHLIST EMPTY.

Το συνδεδεμένο TradingView MCP επέστρεψε `TOOL_QUOTA_EXCEEDED`: ημερήσιο όριο χρήσης και cooldown 10 λεπτών στην πρώτη κλήση (USDCAD), ενεργό cooldown στις υπόλοιπες 4. Και οι 5 κλήσεις αποκλείστηκαν πριν από την εκτέλεση. Δεν επιστράφηκαν metainfo ή last_values· δεν ταυτοποιήθηκε δείκτης από απόκριση και δεν επιβεβαιώθηκε TradingView READY.

**Πρόβλημα εισόδου:** το τρέχον WEEKLY_FOREX_TOP5.json έχει `top5: []`. Δεν υπάρχουν πέντε τρέχοντα εβδομαδιαία ζευγάρια για έλεγχο. Δεν αναπληρώθηκαν από παλιό watchlist. Το report εισόδου απορρίπτει 28/28 ζευγάρια ως YF-H1-MISMATCH.

**Ζητούμενος δείκτης:** BRC TV Triple TF Audit v1, `USER;ae27f010fee5413b8f5d1cc39e592cde`.  
**Παράμετροι:** OANDA:PAIR, timeframe=1h, calc_bars_count=500, return_bars=1.  
**Πηγή παραγώγων όταν είναι διαθέσιμα:** TradingView Pine.

## Κάλυψη

- Weekly Top 5: ΚΕΝΟ — κανένα τρέχον εβδομαδιαίο ζευγάρι.
- OANDA Top 5: USDCAD, EURAUD, GBPUSD, AUDJPY, AUDUSD.
- Trend TV UNVERIFIED / READY στο report εισόδου: κανένας.
- Πρόσθετοι εκτός πεντάδων: κανένας.
- Μοναδικά διαθέσιμα ζευγάρια: 5. Εξετάστηκαν όλες οι γραμμές Trend και ο πίνακας όλων των 28 Forex pairs. Crypto και HTF Reversal εξαιρούνται.

## Ανεξάρτητος πίνακας audit

| Pair | Πηγή | H1 open UTC | Direction | EMA | D1 / H4 structure | ADX H4 / H1 | BRC | Zone | Κλεισμένη H1 τιμή | tv_ready | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| USDCAD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| EURAUD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| GBPUSD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| AUDJPY | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| AUDUSD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |

UNKNOWN = μη διαθέσιμο BRC stage. Οι παύλες αντιστοιχούν σε null, όχι σε τιμές αγοράς. Δεν χρησιμοποιήθηκαν παλιά δεδομένα ή raw OHLC candles. Για κάθε tv_ready=false, Entry/SL/TP/RR παραμένουν null στο JSON.

**BRC:** 0 NO ALIGNMENT · 1 WAIT BREAK · 2 BREAK · 3 RETEST · 4 READY · 5 WAIT NEW RETEST.

## Ανεξάρτητη επιβεβαίωση

READY ισχύει μόνο όταν συμφωνούν η TradingView Pine audit και το Yahoo/OANDA Trend BRC στο **ίδιο κλεισμένο H1, direction και zone**. Το GitHub READY μόνο του δεν αρκεί.

Το tv_ready=true απαιτεί επιτυχή απόκριση, ακριβές OANDA symbol και ταυτοποιημένο δείκτη, last_values από κλεισμένο H1 με ηλικία κλεισίματος 0–2 ώρες (ανοχή 2 λεπτών), verified_ready=1, BRC=4, EMA=3/3, ίδια direction σε D1/H4 structure, ADX H4/H1 ≥20, θετικά πεπερασμένα zone/entry/SL/TP, σωστό προσανατολισμό SL/TP και RR ≥1.2. Χρησιμοποιείται αποκλειστικά last_values, ποτέ forming candle του values[].

Το JSON push εκκινεί νέο fail-closed scan. Η ολοκλήρωση και η νέα εγγραφή υγείας επαληθεύονται χωριστά μετά το push. Αυτός ο Trend έλεγχος δεν επιβεβαιώνει HTF Reversal, δεν ενεργοποιεί READY alerts και δεν δίνει εντολές συναλλαγών.

[Τελευταίο report Forex scanner](LATEST_FOREX_SCAN.md) · [Snapshot audit](TRADINGVIEW_BRC_VERIFIED.json)
