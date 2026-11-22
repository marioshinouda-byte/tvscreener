# TradingView BRC — ανεξάρτητος ωριαίος έλεγχος Trend

**Ώρα Ελλάδας:** 22/11/2026, 02:29:07 (Europe/Athens)  
**UTC:** 2026-11-22T00:29:07Z  
**Κατάσταση:** TradingView Pine διαθέσιμο · 5/5 επιτυχείς κλήσεις · κανένα TV READY.

Ο συνδεδεμένος TradingView MCP επέστρεψε πραγματικά `last_values` και `metainfo.plots` για κάθε ζευγάρι. Ταυτοποιήθηκε ο αποθηκευμένος δείκτης **BRC TV Triple TF Audit v1**, `USER;ae27f010fee5413b8f5d1cc39e592cde`, version `1.0`, με τα 14 αναμενόμενα plots και ακριβές OANDA symbol ανά απόκριση. Κάθε κλήση χρησιμοποίησε `timeframe=1h`, `calc_bars_count=500`, `return_bars=1`.

**Και τα 5 ζευγάρια: BRC=5 WAIT NEW RETEST, verified_ready=0 και tv_ready=false.** Το τελευταίο κλεισμένο H1 που επέστρεψε το Pine άνοιξε **2026-11-20T21:00:00Z** και έκλεισε **2026-11-20T22:00:00Z**. Κατά τον έλεγχο στις **2026-11-22T00:28:03Z** η ηλικία από το κλείσιμο ήταν **26.47 ώρες**, πάνω από το όριο 0–2 ωρών με ανοχή έως 2 λεπτά. Οι παλιές τιμές του κλεισμένου H1 δεν παρουσιάζονται ως νέο κερί. Το AUDNZD έχει επιπλέον H4 structure **0 (NEUTRAL)**, όχι ευθυγραμμισμένο με SHORT.

## Κάλυψη από τα αρχεία εισόδου

- Report εισόδου: **22/11/2026 01:30 (Europe/Athens)**.
- Εβδομαδιαίο [WEEKLY_FOREX_TOP5.json](WEEKLY_FOREX_TOP5.json), 2026-W47: **κενό**, `top5=[]`, `hot_new=[]`. Το report εισόδου απορρίπτει 28/28 ζευγάρια (28 YF-STALE). Δεν χρησιμοποιήθηκε παλιότερη εβδομαδιαία πεντάδα.
- [OANDA_SHORTLIST.md](OANDA_SHORTLIST.md): **AUDNZD, EURAUD, AUDCAD, EURJPY, AUDJPY**. Και τα 5 έχουν STALE στο αρχείο εισόδου. Οι τιμές του screener δεν χρησιμοποιήθηκαν ως Pine audit.
- Ελέγχθηκαν όλες οι Trend ενότητες και ο πίνακας και των 28 Forex pairs: **κανένα επιπλέον Trend A+ READY ή BRC=TV UNVERIFIED**.
- Μοναδική λίστα ελέγχου: **5 ζευγάρια**. Bitcoin/ETH/SOL και το ξεχωριστό HTF Reversal εξαιρούνται.

## Ανεξάρτητος πίνακας TradingView Pine

| Pair | Πηγή | H1 open UTC | Direction | EMA | D1/H4 structure | ADX H4/H1 | BRC | Zone | Κλεισμένη H1 τιμή | tv_ready | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AUDNZD | TradingView Pine | 2026-11-20T21:00:00Z | SHORT | 3/3 | -1 (BEAR) / 0 (NEUTRAL) | 47.43 / 44.07 | 5 WAIT NEW RETEST | 1.21164 | 1.20998 | false | STALE H1 / WAIT NEW RETEST / NO TV READY; verified_ready=0; closed H1 age 26.47h; H4 structure not aligned |
| EURAUD | TradingView Pine | 2026-11-20T21:00:00Z | LONG | 3/3 | 1 (BULL) / 1 (BULL) | 40.29 / 53.83 | 5 WAIT NEW RETEST | 1.65089 | 1.65681 | false | STALE H1 / WAIT NEW RETEST / NO TV READY; verified_ready=0; closed H1 age 26.47h |
| AUDCAD | TradingView Pine | 2026-11-20T21:00:00Z | SHORT | 3/3 | -1 (BEAR) / -1 (BEAR) | 49.23 / 51.44 | 5 WAIT NEW RETEST | 0.95278 | 0.94952 | false | STALE H1 / WAIT NEW RETEST / NO TV READY; verified_ready=0; closed H1 age 26.47h |
| EURJPY | TradingView Pine | 2026-11-20T21:00:00Z | SHORT | 3/3 | -1 (BEAR) / -1 (BEAR) | 40.67 / 35.26 | 5 WAIT NEW RETEST | 174.442 | 173.912 | false | STALE H1 / WAIT NEW RETEST / NO TV READY; verified_ready=0; closed H1 age 26.47h |
| AUDJPY | TradingView Pine | 2026-11-20T21:00:00Z | SHORT | 3/3 | -1 (BEAR) / -1 (BEAR) | 46.60 / 51.17 | 5 WAIT NEW RETEST | 106.22 | 104.962 | false | STALE H1 / WAIT NEW RETEST / NO TV READY; verified_ready=0; closed H1 age 26.47h |

Τα ADX στρογγυλοποιούνται σε 2 δεκαδικά μόνο για εμφάνιση· το JSON διατηρεί τις πραγματικές τιμές που επέστρεψε το Pine. Κατεύθυνση και zone είναι ενδείξεις ελέγχου, όχι εντολές συναλλαγής. Για κάθε `tv_ready=false`, τα `entry`, `stop`, `target`, `rr` είναι `null`. Το Pine επίσης επέστρεψε αυτά τα τέσσερα πεδία ως `null` και στα 5 ζευγάρια.

Στάδια BRC: **0 NO ALIGNMENT · 1 WAIT BREAK · 2 BREAK · 3 RETEST · 4 READY · 5 WAIT NEW RETEST**. Το `UNKNOWN / —` σημαίνει μη διαθέσιμη τιμή, όχι αριθμητικό μηδέν.

## Κανόνας ανεξάρτητης επιβεβαίωσης

**READY ισχύει μόνο όταν συμφωνούν η TradingView Pine audit και το υπάρχον Yahoo/OANDA Trend BRC για το ΙΔΙΟ κλεισμένο H1, direction και zone.** Το GitHub READY από μόνο του δεν αποτελεί ανεξάρτητη επιβεβαίωση. Το `tradingview_gate.py` εφαρμόζει τη διασταύρωση στο νέο scan.

Το `tv_ready=true` απαιτεί επιτυχή απόκριση, ακριβές OANDA symbol, ταυτοποιημένο δείκτη και αντιστοίχιση metainfo.plots, πραγματικά κλεισμένο H1 με ηλικία από το κλείσιμο 0–2 ώρες και ανοχή έως 2 λεπτά, `verified_ready=1`, `brc_stage=4`, EMA 3/3, D1/H4 structure στην ίδια κατεύθυνση, ADX H4/H1 ≥20, finite positive zone/entry/SL/TP, σωστό προσανατολισμό SL/TP και RR ≥1.2. Κάθε αποτυχία διατηρεί `tv_ready=false` με σαφές status.

Χρησιμοποιήθηκε αποκλειστικά το `last_values` του τελευταίου κλεισμένου H1, με `h1_open_at` από το unix-seconds `last_values.t` σε UTC ISO8601. Δεν χρησιμοποιήθηκε το forming candle του `values[]`. Το Pine υπολογίζει D1/H4 με προηγούμενα ολοκληρωμένα HTF κεριά. Δημοσιεύονται μόνο παράγωγα audit signals, χωρίς πλήρη raw OHLC candles. Το `generated_at` του JSON είναι η πραγματική UTC ώρα της νέας ενημέρωσης, ξεχωριστή από την ώρα του παλιού H1.

Η αλλαγή του JSON ενεργοποιεί νέο scan με το ανεξάρτητο TV gate. Η ολοκλήρωσή του επαληθεύεται χωριστά από το workflow και τη νέα εγγραφή FOREX_SCAN_HEALTH.json με source/report hashes. Το παρόν Trend audit δεν επιβεβαιώνει HTF Reversal. READY alerts δεν ενεργοποιούνται.

[Τελευταίο report Forex](LATEST_FOREX_SCAN.md) · [Snapshot JSON](TRADINGVIEW_BRC_VERIFIED.json)
