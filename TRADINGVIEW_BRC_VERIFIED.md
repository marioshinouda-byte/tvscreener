# TradingView BRC — ανεξάρτητος ωριαίος έλεγχος Trend

**Ώρα Ελλάδας:** 19/11/26, 03:37:53 (Europe/Athens)  
**UTC:** 2026-11-19T01:37:53Z  
**Κατάσταση:** TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED.

Το TradingView MCP μπλόκαρε τις κλήσεις λόγω ημερήσιου ορίου χρήσης και ενεργού cooldown. Δεν επιστράφηκαν metainfo ή last_values και δεν επιβεβαιώθηκε TradingView READY.

## Κάλυψη

Το πρώτο read είχε κενό εβδομαδιαίο top5. Το νέο scan αποκατέστησε το watchlist με νέα διαθέσιμα ζευγάρια. Η λίστα audit ανανεώθηκε από τα αποκατεστημένα αρχεία και κλήθηκαν επίσης τα νέα AUDCAD, GBPAUD, AUDNZD. Δεν χρησιμοποιήθηκαν προηγούμενα δεδομένα αγοράς.

- Weekly Top 5: AUDCAD, AUDJPY, GBPAUD, AUDNZD, AUDUSD.
- OANDA Top 5: AUDCAD, AUDJPY, EURAUD, GBPAUD, AUDUSD.
- Πρόσθετοι Trend TV UNVERIFIED / READY: κανένας, μετά από έλεγχο όλων των Trend γραμμών και των 28 Forex pairs.
- Αρχικό OANDA shortlist αυτού του ελέγχου: USDCAD, EURAUD, GBPUSD, AUDJPY, AUDUSD.
- Μοναδικά ζευγάρια αυτού του ελέγχου (ένωση αρχικών και αποκατεστημένων λιστών): 8. Crypto και HTF Reversal εξαιρούνται.

**Ζητούμενος δείκτης:** BRC TV Triple TF Audit v1, `USER;ae27f010fee5413b8f5d1cc39e592cde`.  
**Παράμετροι κάθε κλήσης:** OANDA:PAIR, timeframe=1h, calc_bars_count=500, return_bars=1.  
**Πηγή παραγώγων όταν είναι διαθέσιμα:** TradingView Pine.

| Pair | Πηγή | H1 open UTC | Direction | EMA | D1/H4 | ADX H4/H1 | BRC | Zone | Κλεισμένη H1 τιμή | tv_ready | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| USDCAD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| EURAUD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| GBPUSD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| AUDJPY | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| AUDUSD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| AUDCAD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| GBPAUD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| AUDNZD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |

UNKNOWN σημαίνει μη διαθέσιμο BRC stage. Οι παύλες είναι null, όχι επινοημένες τιμές. Entry/SL/TP/RR είναι null για κάθε tv_ready=false. Δεν δημοσιεύονται raw OHLC candles.

**BRC:** 0 NO ALIGNMENT · 1 WAIT BREAK · 2 BREAK · 3 RETEST · 4 READY · 5 WAIT NEW RETEST.

READY ισχύει μόνο όταν συμφωνούν η ανεξάρτητη TradingView Pine audit και το Yahoo/OANDA Trend BRC για το **ΙΔΙΟ κλεισμένο H1, direction και zone**. Το GitHub READY μόνο του δεν αρκεί.

Το tv_ready=true απαιτεί success=true, ακριβές OANDA symbol και ταυτοποιημένο δείκτη, last_values από κλεισμένο H1 με ηλικία κλεισίματος 0–2 ώρες (ανοχή 2 λεπτών), verified_ready=1, BRC=4, EMA=3/3, ίδια direction σε D1/H4 structure, ADX H4/H1 ≥20, θετικά πεπερασμένα zone/entry/SL/TP, σωστό προσανατολισμό SL/TP και RR ≥1.2. Χρησιμοποιείται μόνο last_values, ποτέ forming candle του values[].

Το JSON push εκκινεί νέο fail-closed scan. Η ολοκλήρωση ελέγχεται μετά το push από workflow και νέα εγγραφή υγείας. Το Trend audit δεν επιβεβαιώνει HTF Reversal, δεν ενεργοποιεί READY alerts και δεν δίνει εντολές συναλλαγών.

[Τελευταίο report](LATEST_FOREX_SCAN.md) · [Snapshot audit](TRADINGVIEW_BRC_VERIFIED.json)
