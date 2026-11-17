# TradingView BRC — ανεξάρτητος ωριαίος έλεγχος Trend

**Ώρα ελέγχου Ελλάδας:** 17/11/26, 4:33:12 μ.μ. EET (Europe/Athens)  
**UTC:** 2026-11-17T14:33:12Z  
**Κατάσταση:** TV UNAVAILABLE — δεν επιστράφηκαν ανεξάρτητα δεδομένα Pine.

Το συνδεδεμένο TradingView MCP επέστρεψε `TOOL_QUOTA_EXCEEDED`: συμπληρώθηκε το ημερήσιο όριο χρήσης και ενεργοποιήθηκε MCP cooldown 10 λεπτών. Η ταυτοποίηση του αποθηκευμένου δείκτη και η εκτέλεσή του ζητήθηκαν, αλλά αποκλείστηκαν από το εργαλείο. Έγινε κλήση του Pine για κάθε ένα από τα 8 ζευγάρια· όλες αποκλείστηκαν. Δεν επιβεβαιώθηκε καμία ένδειξη READY.

**Δείκτης που ζητήθηκε:** BRC TV Triple TF Audit v1, `USER;ae27f010fee5413b8f5d1cc39e592cde`.  
**Παράμετροι κάθε κλήσης:** OANDA:PAIR, timeframe `1h`, calc_bars_count `500`, return_bars `1`.

## Κάλυψη

- Εβδομαδιαίο Top 5: EURAUD, CHFJPY, NZDCAD, AUDJPY, GBPJPY.
- OANDA screener Top 5: CADJPY, CHFJPY, EURJPY, NZDJPY, AUDJPY.
- Επιπλέον Trend ζευγάρια με TV UNVERIFIED ή A+ READY στο αναγνωσμένο GitHub report: κανένα.
- Μοναδικά ζευγάρια: 8. Bitcoin/ETH/SOL και HTF Reversal εξαιρούνται από αυτόν τον Trend έλεγχο.

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
| NZDJPY | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |

Τα κενά πεδία είναι `null` στο JSON, επειδή δεν επιστράφηκαν δεδομένα. Δεν επαναχρησιμοποιούνται τιμές προηγούμενου audit και δεν δημοσιεύονται Entry/SL/TP/RR όταν `tv_ready=false`. Δεν έχουν δημοσιευθεί raw OHLC candles.

BRC στάδια όταν υπάρχουν πραγματικές τιμές Pine: 0 = NO ALIGNMENT, 1 = WAIT BREAK, 2 = BREAK, 3 = RETEST, 4 = READY, 5 = WAIT NEW RETEST. Το TV UNAVAILABLE δεν αποτελεί αριθμητικό στάδιο BRC.

## Κανόνας ανεξάρτητης επιβεβαίωσης

READY ισχύει μόνο όταν συμφωνούν η ανεξάρτητη TradingView Pine audit και το υπάρχον Yahoo/OANDA Trend BRC για **το ίδιο κλεισμένο H1, την ίδια direction και την ίδια zone**. Απαιτούνται επίσης πρόσφατο κλεισμένο H1, EMA 3/3, ευθυγραμμισμένες D1/H4 δομές, ADX H4/H1 ≥ 20, έγκυρα θετικά επίπεδα και RR ≥ 1.2. Το τρέχον audit έχει `tv_ready=false` για όλα τα ζευγάρια, ώστε ο έλεγχος να μπλοκάρει ανεπιβεβαίωτο READY.

Η ενημέρωση του συνοδευτικού JSON ζητά νέο scan μέσω του υπάρχοντος workflow. Η παρούσα αναφορά δεν ισχυρίζεται ότι το νέο scan έχει ήδη ολοκληρωθεί. Η ολοκλήρωση επαληθεύεται ξεχωριστά από το GitHub Actions και τη νέα εγγραφή υγείας.

[Τελευταίο GitHub report](LATEST_FOREX_SCAN.md) · [Machine-readable audit](TRADINGVIEW_BRC_VERIFIED.json)

Αυτός ο έλεγχος αφορά μόνο Trend. Δεν επιβεβαιώνει HTF Reversal, δεν παρέχει εντολή συναλλαγής και δεν ενεργοποιεί READY alerts.
