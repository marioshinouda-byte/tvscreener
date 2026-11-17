# TradingView BRC — ανεξάρτητος ωριαίος έλεγχος Trend

**Ώρα Ελλάδας:** 18/11/2026, 00:26:37 (Europe/Athens)  
**UTC:** 2026-11-17T22:26:37Z  
**Κατάσταση:** TV UNAVAILABLE.

Το συνδεδεμένο TradingView MCP επέστρεψε `TOOL_QUOTA_EXCEEDED`: ημερήσιο όριο χρήσης και MCP cooldown 10 λεπτών. Οι κλήσεις για όλα τα 10 μοναδικά ζευγάρια αποκλείστηκαν. Δεν επιστράφηκαν metadata ή last_values· δεν επιβεβαιώθηκε READY.

**Ζητούμενος δείκτης:** BRC TV Triple TF Audit v1, `USER;ae27f010fee5413b8f5d1cc39e592cde`. Κάθε κλήση: `OANDA:PAIR`, timeframe `1h`, calc_bars_count `500`, return_bars `1`.

## Κάλυψη

- Εβδομαδιαίο Top 5: CHFJPY, NZDCAD, AUDJPY, GBPJPY, AUDCHF.
- OANDA screener Top 5: CADJPY, EURJPY, USDCAD, GBPNZD, EURUSD.
- Επιπλέον Trend BRC=TV UNVERIFIED ή A+ READY στο αναγνωσμένο GitHub report: κανένα.
- Σύνολο 10 μοναδικά Forex ζευγάρια. Bitcoin/ETH/SOL και HTF Reversal εξαιρούνται.

## Ανεξάρτητος πίνακας audit

| Ζευγάρι | Πηγή | Κλεισμένο H1 open UTC | Direction | EMA /3 | D1 / H4 structure | ADX H4 / H1 | BRC | Zone | Κλείσιμο H1 | tv_ready | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CHFJPY | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |
| NZDCAD | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |
| AUDJPY | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |
| GBPJPY | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |
| AUDCHF | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |
| CADJPY | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |
| EURJPY | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |
| USDCAD | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |
| GBPNZD | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |
| EURUSD | TradingView Pine | — | — | — | — | — | TV UNAVAILABLE | — | — | false | TOOL_QUOTA_EXCEEDED / MCP cooldown |

Τα μη διαθέσιμα πεδία και όλα τα Entry/SL/TP/RR είναι `null` στο JSON. Δεν επαναχρησιμοποιούνται τιμές προηγούμενου audit. Δημοσιεύονται μόνο παράγωγα audit signals, ποτέ raw OHLC candles.

BRC: 0 = NO ALIGNMENT, 1 = WAIT BREAK, 2 = BREAK, 3 = RETEST, 4 = READY, 5 = WAIT NEW RETEST. Το TV UNAVAILABLE είναι σφάλμα πρόσβασης, όχι αριθμητικό στάδιο BRC.

## Κανόνας READY

READY ισχύει μόνο όταν συμφωνούν η ανεξάρτητη TradingView Pine audit και το υπάρχον Yahoo/OANDA Trend BRC για **το ίδιο κλεισμένο H1, την ίδια direction και την ίδια zone**. Το GitHub READY μόνο του δεν αρκεί.

Απαιτούνται επιτυχής κλήση με ταυτοποιημένο δείκτη και σωστό symbol, ηλικία κλεισίματος H1 0–2 ώρες (ανοχή 2 λεπτών), verified_ready=1, BRC=4, EMA=3/3, D1/H4 structure προς ίδια κατεύθυνση, ADX H4/H1 ≥20, πεπερασμένα θετικά zone/entry/SL/TP, έγκυρος προσανατολισμός επιπέδων και RR≥1.2.

Όλα τα `tv_ready` είναι `false`. Το JSON push ζητά νέο scan ώστε το gate να μπλοκάρει ανεπιβεβαίωτο READY. Η ολοκλήρωση του νέου scan ελέγχεται χωριστά μέσω GitHub Actions και νέας εγγραφής υγείας· η δημοσίευση του audit δεν την αποδεικνύει.

[Τελευταίο GitHub report](LATEST_FOREX_SCAN.md) · [Machine-readable audit](TRADINGVIEW_BRC_VERIFIED.json)

Το Trend audit δεν επιβεβαιώνει HTF Reversal, δεν δίνει εντολές συναλλαγών και δεν ενεργοποιεί READY alerts.
