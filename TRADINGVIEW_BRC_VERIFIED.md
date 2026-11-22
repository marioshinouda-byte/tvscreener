# TradingView BRC — ανεξάρτητος ωριαίος έλεγχος Trend

**Ώρα Ελλάδας:** 22/11/2026, 02:35:49 (Europe/Athens)  
**UTC:** 2026-11-22T00:35:49Z  
**Κατάσταση:** TradingView Pine διαθέσιμο · 5/5 επιτυχείς νέες κλήσεις · κανένα TV READY.

Ταυτοποιήθηκε σε κάθε απόκριση ο δείκτης **BRC TV Triple TF Audit v1**, `USER;ae27f010fee5413b8f5d1cc39e592cde`, version `1.0`, με ακριβές `OANDA:PAIR` και αντιστοίχιση των 14 `metainfo.plots`. Κλήση ανά ζευγάρι: `timeframe=1h`, `calc_bars_count=500`, `return_bars=1`. Πηγή: **TradingView Pine**.

Και τα 5 αποτελέσματα έχουν **BRC=5 WAIT NEW RETEST**, **verified_ready=0**, **tv_ready=false**. Το τελευταίο κλεισμένο H1 άνοιξε **2026-11-20T21:00:00Z** και έκλεισε **2026-11-20T22:00:00Z**. Στις **2026-11-22T00:34:49Z** είχε ηλικία **26.58 ώρες από το κλείσιμο**, εκτός ορίου 0–2 ωρών ±2 λεπτά. Οι παλιές τιμές του H1 δεν παρουσιάζονται ως νέο κερί. Το AUDNZD έχει επιπλέον H4 structure **0 NEUTRAL**, χωρίς συμφωνία με SHORT.

## Κάλυψη υποψηφίων

- Report εισόδου: **22/11/2026 02:30 (Europe/Athens)**.
- [WEEKLY_FOREX_TOP5.json](WEEKLY_FOREX_TOP5.json), 2026-W47: **κενό**, `top5=[]`, `hot_new=[]`. Το report εισόδου απορρίπτει 28/28 ζευγάρια (27 YF-STALE · USDCHF: N/A). Δεν ανακτήθηκε παλιότερη πεντάδα.
- [OANDA_SHORTLIST.md](OANDA_SHORTLIST.md): **AUDNZD, EURAUD, AUDCAD, EURJPY, AUDJPY**, 5/5 STALE. Οι ενδείξεις του screener δεν αντικαθιστούν το ανεξάρτητο Pine audit.
- Ελέγχθηκαν όλες οι Trend ενότητες και ο πίνακας των 28 Forex pairs: **κανένα επιπλέον A+ READY Trend ή BRC=TV UNVERIFIED**.
- Μοναδική λίστα: **5 ζευγάρια**. Bitcoin/ETH/SOL και HTF Reversal εξαιρούνται από αυτό το Trend audit.

## Ανεξάρτητος πίνακας TradingView Pine

| Pair | Πηγή | H1 open UTC | Direction | EMA | D1/H4 structure | ADX H4/H1 | BRC | Zone | Κλεισμένη H1 τιμή | tv_ready | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AUDNZD | TradingView Pine | 2026-11-20T21:00:00Z | SHORT | 3/3 | -1 BEAR / 0 NEUTRAL | 47.43 / 44.07 | 5 WAIT NEW RETEST | 1.21164 | 1.20998 | false | STALE H1 / WAIT NEW RETEST / NO TV READY; verified_ready=0; closed H1 age 26.58h; H4 structure not aligned |
| EURAUD | TradingView Pine | 2026-11-20T21:00:00Z | LONG | 3/3 | 1 BULL / 1 BULL | 40.29 / 53.83 | 5 WAIT NEW RETEST | 1.65089 | 1.65681 | false | STALE H1 / WAIT NEW RETEST / NO TV READY; verified_ready=0; closed H1 age 26.58h |
| AUDCAD | TradingView Pine | 2026-11-20T21:00:00Z | SHORT | 3/3 | -1 BEAR / -1 BEAR | 49.23 / 51.44 | 5 WAIT NEW RETEST | 0.95278 | 0.94952 | false | STALE H1 / WAIT NEW RETEST / NO TV READY; verified_ready=0; closed H1 age 26.58h |
| EURJPY | TradingView Pine | 2026-11-20T21:00:00Z | SHORT | 3/3 | -1 BEAR / -1 BEAR | 40.67 / 35.26 | 5 WAIT NEW RETEST | 174.442 | 173.912 | false | STALE H1 / WAIT NEW RETEST / NO TV READY; verified_ready=0; closed H1 age 26.58h |
| AUDJPY | TradingView Pine | 2026-11-20T21:00:00Z | SHORT | 3/3 | -1 BEAR / -1 BEAR | 46.60 / 51.17 | 5 WAIT NEW RETEST | 106.22 | 104.962 | false | STALE H1 / WAIT NEW RETEST / NO TV READY; verified_ready=0; closed H1 age 26.58h |

Τα ADX στρογγυλοποιούνται σε 2 δεκαδικά μόνο στον πίνακα· το JSON διατηρεί την ακρίβεια των πραγματικών αποτελεσμάτων Pine. Για κάθε `tv_ready=false`, **entry/stop/target/rr=null**. Το εργαλείο επέστρεψε και τα τέσσερα ως `null` και στα 5 ζευγάρια. Direction και zone είναι ενδείξεις ελέγχου, όχι εντολές συναλλαγής.

Στάδια BRC: **0 NO ALIGNMENT · 1 WAIT BREAK · 2 BREAK · 3 RETEST · 4 READY · 5 WAIT NEW RETEST**. Το UNKNOWN/— δηλώνει μη διαθέσιμη τιμή, όχι μηδέν.

## Ανεξάρτητο TV gate

**READY ισχύει μόνο όταν συμφωνούν η TradingView Pine audit και το υπάρχον Yahoo/OANDA Trend BRC για το ΙΔΙΟ κλεισμένο H1, direction και zone.** Το τρέχον GitHub READY δεν αρκεί χωρίς ανεξάρτητη TV επιβεβαίωση. Η διασταύρωση γίνεται από το υπάρχον `tradingview_gate.py` στο νέο scan.

Το `tv_ready=true` απαιτεί: success=true, ακριβές OANDA symbol, ταυτοποιημένο δείκτη και plot map, πραγματικά κλεισμένο H1 με ηλικία κλεισίματος 0–2 ώρες ±2 λεπτά, verified_ready=1, brc_stage=4, EMA 3/3, D1/H4 structure στην ίδια κατεύθυνση, ADX H4/H1 ≥20, finite positive zone/entry/SL/TP, έγκυρο προσανατολισμό SL/TP και RR ≥1.2. Κάθε αποτυχία διατηρεί tv_ready=false με σαφές status.

Χρησιμοποιήθηκε μόνο το `last_values` του τελευταίου κλεισμένου H1 και `h1_open_at` από το unix-seconds `last_values.t` σε UTC ISO8601, ποτέ forming candle από `values[]`. Το Pine υπολογίζει προηγούμενα ολοκληρωμένα HTF κεριά στα D1/H4. Δημοσιεύονται μόνο παράγωγα audit signals, χωρίς πλήρη raw OHLC candles. Το `generated_at` του JSON είναι η πραγματική UTC ώρα της νέας ενημέρωσης, ξεχωριστή από την ώρα του H1.

Το JSON push ενεργοποιεί νέο scan με το ανεξάρτητο gate. Η ολοκλήρωση επαληθεύεται χωριστά μέσω του νέου workflow run και του FOREX_SCAN_HEALTH.json με σωστά source/report hashes. Αυτό το Trend audit δεν επιβεβαιώνει HTF Reversal και δεν ενεργοποιεί READY alerts.

[Τελευταίο report Forex](LATEST_FOREX_SCAN.md) · [Snapshot JSON](TRADINGVIEW_BRC_VERIFIED.json)
