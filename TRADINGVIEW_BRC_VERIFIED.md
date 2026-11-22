# TradingView BRC — ανεξάρτητος ωριαίος έλεγχος Trend

**Ώρα Ελλάδας:** 22/11/2026, 03:30:04 (Europe/Athens)  
**UTC:** 2026-11-22T01:30:04Z  
**Κατάσταση:** TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED.

Και οι 5 απαιτούμενες νέες κλήσεις μπλοκαρίστηκαν πριν από την εκτέλεση του Pine. Η πρώτη (AUDNZD) επέστρεψε ημερήσιο όριο χρήσης και cooldown 10 λεπτών· οι υπόλοιπες ενεργό cooldown. Δεν επιστράφηκαν metainfo ή last_values, δεν ταυτοποιήθηκε δείκτης από τις τρέχουσες αποκρίσεις και δεν επιβεβαιώθηκε TradingView READY.

Ζητούμενος δείκτης: **BRC TV Triple TF Audit v1**, `USER;ae27f010fee5413b8f5d1cc39e592cde`. Πραγματοποιήθηκε κλήση ανά ζευγάρι με `symbol=OANDA:PAIR`, `timeframe=1h`, `calc_bars_count=500`, `return_bars=1`. Πηγή παραγώγων, όταν επιστρέφονται: **TradingView Pine**.

## Κάλυψη από τα αρχεία εισόδου

- Report εισόδου: **22/11/2026 02:37 (Europe/Athens)**.
- [WEEKLY_FOREX_TOP5.json](WEEKLY_FOREX_TOP5.json), 2026-W47: **κενό**, `top5=[]`, `hot_new=[]`. Το report εισόδου απορρίπτει 28/28 ζευγάρια (28 YF-STALE). Δεν χρησιμοποιήθηκε παλιότερη εβδομαδιαία πεντάδα.
- [OANDA_SHORTLIST.md](OANDA_SHORTLIST.md): **AUDNZD, EURAUD, AUDCAD, EURJPY, AUDJPY**, 5/5 STALE στο αρχείο εισόδου.
- Ελέγχθηκαν όλες οι Trend ενότητες και ο πίνακας των 28 Forex pairs: **κανένα επιπλέον Trend A+ READY ή BRC=TV UNVERIFIED**.
- Μοναδική λίστα ελέγχου: **5 ζευγάρια**. Bitcoin/ETH/SOL και το ξεχωριστό HTF Reversal εξαιρούνται από το συγκεκριμένο Trend audit.

## Ανεξάρτητος πίνακας TradingView Pine

| Pair | Πηγή | H1 open UTC | Direction | EMA | D1/H4 structure | ADX H4/H1 | BRC | Zone | Κλεισμένη H1 τιμή | tv_ready | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AUDNZD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: daily usage limit; MCP cooldown 10 minutes |
| EURAUD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |
| AUDCAD | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |
| EURJPY | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |
| AUDJPY | TradingView Pine | — | — | — | — | — | UNKNOWN | — | — | false | TV UNAVAILABLE / TOOL_QUOTA_EXCEEDED: MCP cooldown active |

**UNKNOWN / —:** δεν επιστράφηκε τιμή από το εργαλείο, άρα καταγράφεται `null`. Δεν επαναχρησιμοποιούνται τιμές προηγούμενου audit ή του screener. Για κάθε `tv_ready=false`, τα **entry/stop/target/rr είναι null**.

Στάδια BRC: **0 NO ALIGNMENT · 1 WAIT BREAK · 2 BREAK · 3 RETEST · 4 READY · 5 WAIT NEW RETEST**. Το UNKNOWN δεν είναι αριθμητικό στάδιο BRC.

## Ανεξάρτητο TV gate

**READY ισχύει μόνο όταν συμφωνούν η TradingView Pine audit και το υπάρχον Yahoo/OANDA Trend BRC για το ΙΔΙΟ κλεισμένο H1, direction και zone.** Το GitHub READY από μόνο του δεν αποτελεί ανεξάρτητη επιβεβαίωση. Το υπάρχον `tradingview_gate.py` εφαρμόζει τη διασταύρωση στο νέο scan.

Το `tv_ready=true` απαιτεί success=true, ακριβές OANDA symbol, ταυτοποιημένο δείκτη και αντιστοίχιση metainfo.plots, πραγματικά κλεισμένο H1 με ηλικία από το κλείσιμο 0–2 ώρες και ανοχή έως 2 λεπτά, verified_ready=1, brc_stage=4, EMA 3/3, D1/H4 structure στην ίδια κατεύθυνση, ADX H4/H1 ≥20, finite positive zone/entry/SL/TP, σωστό προσανατολισμό SL/TP και RR ≥1.2. Κάθε αποτυχία διατηρεί tv_ready=false με σαφές status.

Χρησιμοποιείται μόνο το `last_values` του τελευταίου κλεισμένου H1, με `h1_open_at` από το unix-seconds `last_values.t` σε UTC ISO8601, ποτέ το forming candle του `values[]`. Το Pine υπολογίζει προηγούμενα ολοκληρωμένα HTF κεριά στα D1/H4. Στον παρόντα έλεγχο δεν επιστράφηκαν αυτά τα δεδομένα. Δημοσιεύονται μόνο παράγωγα audit signals, χωρίς πλήρη raw OHLC candles. Το `generated_at` του JSON είναι η πραγματική UTC ώρα της νέας ενημέρωσης.

Το JSON push ενεργοποιεί νέο fail-closed scan. Η ολοκλήρωση επαληθεύεται χωριστά από το νέο workflow και το FOREX_SCAN_HEALTH.json με σωστά source/report hashes. Το παρόν Trend audit δεν επιβεβαιώνει HTF Reversal και δεν ενεργοποιεί READY alerts.

[Τελευταίο report Forex](LATEST_FOREX_SCAN.md) · [Snapshot JSON](TRADINGVIEW_BRC_VERIFIED.json)
