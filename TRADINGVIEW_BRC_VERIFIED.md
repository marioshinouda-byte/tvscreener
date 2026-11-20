# TradingView BRC — ανεξάρτητος ωριαίος έλεγχος Trend

**Ώρα Ελλάδας:** 20/11/2026, 03:28:22 (Europe/Athens)  
**UTC:** 2026-11-20T01:28:22Z  
**TradingView Pine:** 2/5 επιτυχείς κλήσεις, 3/5 TV UNAVAILABLE.  
**Ανεξάρτητο TV READY:** 0/5.

Τα EURAUD και AUDCAD επέστρεψαν πραγματικά TradingView Pine δεδομένα με success=true, ακριβές OANDA symbol, ταυτοποιημένο δείκτη και σωστά metainfo.plots. Τα AUDCHF, AUDJPY και AUDUSD δεν επέστρεψαν metainfo ή last_values: η κλήση AUDCHF μπλοκαρίστηκε από ημερήσιο όριο TOOL_QUOTA_EXCEEDED και cooldown 10 λεπτών· οι δύο επόμενες από ενεργό cooldown. Για αυτά γράφονται TV UNAVAILABLE, tv_ready=false και null στα μη διαθέσιμα πεδία.

**Δείκτης:** BRC TV Triple TF Audit v1, `USER;ae27f010fee5413b8f5d1cc39e592cde`.  
**Παράμετροι:** OANDA:PAIR, timeframe=1h, calc_bars_count=500, return_bars=1.  
**Πηγή:** TradingView Pine. Παράγωγα audit signals μόνο, χωρίς raw OHLC candles.

## Κάλυψη

- WEEKLY_FOREX_TOP5.json: top5=[] — κενή εβδομαδιαία λίστα στο τρέχον GitHub αρχείο.
- OANDA Top 5: EURAUD, AUDCAD, AUDCHF, AUDJPY, AUDUSD.
- Trend TV UNVERIFIED / READY στο report εισόδου: κανένας.
- Πρόσθετοι εκτός πεντάδων: κανένας.
- Μοναδικά διαθέσιμα υποψήφια ζευγάρια: 5. Εξετάστηκαν όλες οι γραμμές Trend και ο πίνακας όλων των 28 Forex pairs. Crypto και HTF Reversal εξαιρούνται.

Το report εισόδου απέρριψε 28/28 ζευγάρια ως YF-H1-MISMATCH: δεν βρέθηκε το ίδιο κλεισμένο H1 κερί OANDA/Yahoo. Η νέα εκτέλεση μετά το JSON push θα ελεγχθεί για ολοκλήρωση, hashes και κατάσταση πηγών.

| Pair | Πηγή | H1 open UTC | Direction | EMA | D1/H4 structure | ADX H4/H1 | BRC | Zone | Κλεισμένη H1 τιμή | verified_ready | tv_ready | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EURAUD | TradingView Pine | 2026-11-20T00:00:00Z | LONG | 3/3 | 1 / 1 | 36.48 / 42.19 | 5 WAIT NEW RETEST | 1.64566 | 1.64848 | 0 | false | WATCH / WAIT NEW RETEST / NO TV READY |
| AUDCAD | TradingView Pine | 2026-11-20T00:00:00Z | SHORT | 3/3 | -1 / -1 | 45.67 / 42.92 | 5 WAIT NEW RETEST | 0.95609 | 0.95416 | 0 | false | WATCH / WAIT NEW RETEST / NO TV READY |
| AUDCHF | TradingView Pine | — | — | — | — / — | — / — | UNKNOWN | — | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: daily usage limit; MCP cooldown 10 minutes |
| AUDJPY | TradingView Pine | — | — | — | — / — | — / — | UNKNOWN | — | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |
| AUDUSD | TradingView Pine | — | — | — | — / — | — / — | UNKNOWN | — | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |

Για τις δύο επιτυχείς αποκρίσεις χρησιμοποιήθηκε αποκλειστικά το last_values από την H1 που άνοιξε 2026-11-20T00:00:00Z και έκλεισε 2026-11-20T01:00:00Z. Κατά την επικύρωση (2026-11-20T01:26:23Z) η ηλικία κλεισίματος ήταν 1583 δευτερόλεπτα, εντός 0–2 ωρών με ανοχή 2 λεπτών. Το forming candle του values[] αποκλείστηκε.

**Structure:** 1 BULL · 0 NEUTRAL · -1 BEAR. Τα ADX στον πίνακα εμφανίζονται με 2 δεκαδικά· το JSON κρατά την ακρίβεια του TradingView. UNKNOWN και παύλες σημαίνουν null, όχι τιμές αγοράς. Entry/SL/TP/RR είναι null για κάθε tv_ready=false. Δεν χρησιμοποιήθηκαν δεδομένα προηγούμενου audit.

**BRC:** 0 NO ALIGNMENT · 1 WAIT BREAK · 2 BREAK · 3 RETEST · 4 READY · 5 WAIT NEW RETEST.

READY ισχύει μόνο όταν συμφωνούν η ανεξάρτητη TradingView Pine audit και το Yahoo/OANDA Trend BRC για το **ΙΔΙΟ κλεισμένο H1, direction και zone**. Το GitHub READY μόνο του δεν αρκεί.

Το tv_ready=true απαιτεί success=true, ακριβές OANDA symbol και ταυτοποιημένο δείκτη, κλεισμένο H1 με ηλικία κλεισίματος 0–2 ώρες (ανοχή 2 λεπτών), verified_ready=1, BRC=4, EMA=3/3, ίδια direction σε D1/H4 structure, ADX H4/H1 ≥20, θετικά πεπερασμένα zone/entry/SL/TP, σωστό προσανατολισμό SL/TP και RR ≥1.2, ελεγμένο και από τις αποστάσεις entry/stop/target.

Το JSON push εκκινεί νέο fail-closed scan. Η ολοκλήρωση ελέγχεται μετά το push από το workflow και νέα εγγραφή υγείας. Το Trend audit δεν επιβεβαιώνει HTF Reversal, δεν ενεργοποιεί READY alerts και δεν δίνει εντολές συναλλαγών.

[Τελευταίο report](LATEST_FOREX_SCAN.md) · [Snapshot audit](TRADINGVIEW_BRC_VERIFIED.json)
