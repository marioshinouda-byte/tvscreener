# TradingView BRC — ανεξάρτητος ωριαίος έλεγχος Trend

**Ώρα Ελλάδας:** 17/11/2026, 17:28:06 (Europe/Athens)  
**UTC:** 2026-11-17T15:28:06Z  
**Κατάσταση:** TV UNAVAILABLE — δεν επιστράφηκαν ανεξάρτητα δεδομένα Pine.

Το συνδεδεμένο TradingView MCP επέστρεψε `TOOL_QUOTA_EXCEEDED`: συμπληρώθηκε το ημερήσιο όριο χρήσης και ενεργοποιήθηκε MCP cooldown 10 λεπτών. Ζητήθηκε εκτέλεση του αποθηκευμένου δείκτη για κάθε ένα από τα 8 μοναδικά ζευγάρια· όλες οι κλήσεις αποκλείστηκαν. Δεν επιστράφηκαν metadata ή last_values και δεν επιβεβαιώθηκε καμία ένδειξη READY.

**Ζητούμενος δείκτης:** BRC TV Triple TF Audit v1 — `USER;ae27f010fee5413b8f5d1cc39e592cde`.  
**Παράμετροι κάθε κλήσης:** symbol `OANDA:PAIR`, timeframe `1h`, calc_bars_count `500`, return_bars `1`.

## Κάλυψη

- Εβδομαδιαίο Top 5: EURAUD, CHFJPY, NZDCAD, AUDJPY, GBPJPY.
- OANDA screener Top 5: CADJPY, EURJPY, AUDJPY, CHFJPY, GBPAUD.
- Επιπλέον Trend ζευγάρια με BRC=TV UNVERIFIED ή A+ READY στο αναγνωσμένο GitHub report: κανένα.
- Σύνολο: 8 μοναδικά ζευγάρια. Bitcoin/ETH/SOL και HTF Reversal εξαιρούνται από το συγκεκριμένο Trend audit.

## Ανεξάρτητος πίνακας audit

| Ζευγάρι | Πηγή | Κλεισμένο H1 open UTC | Direction | EMA /3 | D1 / H4 structure | ADX H4 / H1 | BRC | Zone | Κλείσιμο H1 | tv_ready | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EURAUD | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |
| CHFJPY | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |
| NZDCAD | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |
| AUDJPY | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |
| GBPJPY | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |
| CADJPY | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |
| EURJPY | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |
| GBPAUD | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |

Τα κενά πεδία είναι `null` στο JSON, επειδή δεν επιστράφηκαν δεδομένα. Δεν χρησιμοποιούνται τιμές προηγούμενου audit. Όλα τα Entry/SL/TP/RR είναι `null`, καθώς `tv_ready=false`. Δημοσιεύονται μόνο παράγωγα audit signals όταν υπάρχουν· κανένα raw OHLC candle.

BRC στάδια όταν επιστρέφονται πραγματικές τιμές Pine: 0 = NO ALIGNMENT, 1 = WAIT BREAK, 2 = BREAK, 3 = RETEST, 4 = READY, 5 = WAIT NEW RETEST. Το TV UNAVAILABLE δεν αποτελεί αριθμητικό στάδιο BRC.

## Κανόνας READY

READY ισχύει μόνο όταν συμφωνούν η ανεξάρτητη TradingView Pine audit και το υπάρχον Yahoo/OANDA Trend BRC για **το ίδιο κλεισμένο H1, την ίδια direction και την ίδια zone**. Το GitHub READY από μόνο του δεν αρκεί.

Η Pine audit απαιτεί ταυτοποιημένο δείκτη και σωστό OANDA symbol, τελευταίο κλεισμένο H1 με ηλικία κλεισίματος 0–2 ώρες (ανοχή 2 λεπτών), verified_ready=1, BRC=4, EMA=3/3, D1/H4 structure προς την ίδια κατεύθυνση, ADX H4/H1 ≥20, πεπερασμένα θετικά zone/entry/SL/TP, σωστό προσανατολισμό επιπέδων και RR≥1.2.

Εδώ όλα τα `tv_ready` είναι `false`. Η ενημέρωση του συνοδευτικού JSON ενεργοποιεί νέο scan με το υπάρχον workflow, ώστε το gate να μπλοκάρει ανεπιβεβαίωτο READY. Η δημοσίευση αυτού του audit δεν αποτελεί απόδειξη ολοκλήρωσης του νέου scan· η ολοκλήρωση ελέγχεται χωριστά από το GitHub Actions και τη νέα εγγραφή υγείας.

[Τελευταίο GitHub report](LATEST_FOREX_SCAN.md) · [Machine-readable audit](TRADINGVIEW_BRC_VERIFIED.json)

Αφορά μόνο Trend και δεν επιβεβαιώνει HTF Reversal. Δεν δίνει εντολές συναλλαγών και δεν ενεργοποιεί READY alerts.
