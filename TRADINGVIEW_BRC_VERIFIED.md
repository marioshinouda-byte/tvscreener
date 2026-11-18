# TradingView BRC — ανεξάρτητος ωριαίος έλεγχος Trend

**Ώρα Ελλάδας:** 18/11/2026, 18:35:00 (Europe/Athens)  
**UTC:** 2026-11-18T16:35:00Z  
**Κατάσταση:** TV UNAVAILABLE.

Το συνδεδεμένο TradingView MCP επέστρεψε `TOOL_QUOTA_EXCEEDED`: ημερήσιο όριο χρήσης και MCP cooldown 10 λεπτών στην πρώτη κλήση (NZDCAD), ενεργό cooldown στις επόμενες 7 κλήσεις. Και οι 8 κλήσεις αποκλείστηκαν πριν από την εκτέλεση. Δεν επιστράφηκαν metainfo ή last_values και δεν επιβεβαιώθηκε κανένα TradingView READY.

**Ζητούμενος δείκτης:** BRC TV Triple TF Audit v1, `USER;ae27f010fee5413b8f5d1cc39e592cde`.  
**Παράμετροι κάθε κλήσης:** OANDA:PAIR, timeframe=1h, calc_bars_count=500, return_bars=1.  
**Πηγή παραγώγων, όταν είναι διαθέσιμα:** TradingView Pine.

## Κάλυψη

- Εβδομαδιαίο Top 5: NZDCAD, AUDJPY, GBPJPY, AUDCHF, AUDUSD.
- OANDA shortlist Top 5: CHFJPY, CADJPY, GBPJPY, EURJPY, AUDJPY.
- Πρόσθετοι Trend υποψήφιοι με TV UNVERIFIED ή READY στο τελευταίο report: κανένας.
- Μοναδικά ζευγάρια: 8. Ελέγχθηκαν όλες οι γραμμές Trend του report, συμπεριλαμβανομένου του πίνακα όλων των 28 Forex pairs.
- Bitcoin/ETH/SOL και HTF Reversal εξαιρούνται από αυτόν τον Trend έλεγχο.

## Ανεξάρτητος πίνακας audit

| Pair | Πηγή | H1 open UTC | Direction | EMA | D1 / H4 structure | ADX H4 / H1 | BRC | Zone | Κλεισμένη H1 τιμή | tv_ready | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NZDCAD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| AUDJPY | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| GBPJPY | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| AUDCHF | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| AUDUSD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| CHFJPY | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| CADJPY | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |
| EURJPY | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED |

Το UNKNOWN σημαίνει ότι δεν επέστρεψε ο δείκτης BRC stage. Οι παύλες αντιστοιχούν σε null, όχι σε τιμές αγοράς. Δεν επαναχρησιμοποιήθηκαν προηγούμενα δεδομένα. Για όλα τα tv_ready=false τα Entry/SL/TP/RR παραμένουν null στο JSON και δεν δημοσιεύονται επίπεδα συναλλαγής. Δεν δημοσιεύονται raw OHLC candles.

**Καταστάσεις BRC:** 0 NO ALIGNMENT · 1 WAIT BREAK · 2 BREAK · 3 RETEST · 4 READY · 5 WAIT NEW RETEST.

## Κανόνας ανεξάρτητης επιβεβαίωσης

READY ισχύει μόνο όταν συμφωνούν η TradingView Pine audit και το υπάρχον Yahoo/OANDA Trend BRC για το **ίδιο κλεισμένο H1, direction και zone**. Η τρέχουσα ένδειξη GitHub READY δεν αρκεί χωρίς αυτόν τον ανεξάρτητο έλεγχο.

Το tv_ready=true απαιτεί success=true, ακριβές OANDA symbol και ταυτοποιημένο δείκτη, last_values από ολοκληρωμένο H1 με ηλικία κλεισίματος 0–2 ώρες (ανοχή 2 λεπτών), verified_ready=1, BRC=4, EMA=3/3, D1/H4 structure προς την ίδια κατεύθυνση, ADX H4/H1 ≥20, θετικά πεπερασμένα zone/entry/SL/TP, σωστό προσανατολισμό SL/TP και RR ≥1.2. Χρησιμοποιείται αποκλειστικά last_values, ποτέ το forming candle του values[].

Η απουσία TradingView δεδομένων διατηρεί tv_ready=false. Το JSON push ζητά νέο fail-closed scan· η δημοσίευση αυτού του audit δεν αποδεικνύει ολοκλήρωση του workflow. Το νέο αποτέλεσμα και η εγγραφή υγείας ελέγχονται χωριστά μετά το push.

Το Trend audit δεν επιβεβαιώνει HTF Reversal, δεν ενεργοποιεί READY alerts και δεν αποτελεί εντολή συναλλαγής.

[Τελευταίο report Forex scanner](LATEST_FOREX_SCAN.md) · [Snapshot παραγώγων audit](TRADINGVIEW_BRC_VERIFIED.json)
