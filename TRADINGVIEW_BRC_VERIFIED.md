# TradingView — ανεξάρτητος ωριαίος έλεγχος Trend BRC

**Ώρα ελέγχου Ελλάδας:** 17/11/26, 1:29:26 μ.μ. (Europe/Athens)  
**Ώρα ελέγχου UTC:** 2026-11-17T11:29:26Z  
**Πηγή:** TradingView Pine, OANDA · δείκτης **BRC TV Triple TF Audit v1**, version 1.0.  
**Script ID:** `USER;ae27f010fee5413b8f5d1cc39e592cde`

Ελέγχθηκαν **8 μοναδικά Forex ζευγάρια**: τα 5 του εβδομαδιαίου watchlist (EURAUD, CHFJPY, NZDCAD, AUDJPY, GBPJPY), τα 5 του OANDA shortlist (CHFJPY, EURUSD, EURJPY, GBPUSD, GBPJPY) και όλοι οι επιπλέον Trend TV UNVERIFIED / A+ READY υποψήφιοι (κανένας στο αναγνωσμένο report).

**Αποτέλεσμα ανεξάρτητου TV audit: 0 TV READY.** Η σύνδεση και ο δείκτης ελέγχθηκαν επιτυχώς για όλα τα ζευγάρια. Δεν δημοσιεύονται Entry/SL/TP/RR για `tv_ready=false`.

Χρησιμοποιήθηκε αποκλειστικά το `last_values` του εργαλείου (τελευταίο κλεισμένο H1), όχι το forming candle του `values[]`. Για όλες τις γραμμές: H1 άνοιγμα **17/11/2026 10:00 UTC**, κλείσιμο **11:00 UTC** (12:00–13:00 Ελλάδας). Τα προηγούμενα ολοκληρωμένα D1/H4 υπολογίζονται από τον αποθηκευμένο δείκτη. Η ηλικία υπολογίζεται από το **κλείσιμο** H1 και ελέγχεται για 0–2 ώρες με ανοχή 2 λεπτών.

| Pair | TV direction | EMA | D1 / H4 structure | ADX H4 / H1 | BRC | Zone | Κλεισμένο H1 close | H1 open UTC | TV READY | Status / αιτία |
|---|---|---:|---|---|---|---:|---:|---|---|---|
| EURAUD | LONG | 3/3 | 1 / 1 | 43.69 / 35.12 | WAIT NEW RETEST | 1.63262 | 1.63065 | 2026-11-17T10:00:00.000Z | NO | WATCH / NO TV READY: WAIT NEW RETEST |
| CHFJPY | SHORT | 3/3 | 0 / -1 | 49.47 / 30.17 | WAIT NEW RETEST | 189.752 | 189.612 | 2026-11-17T10:00:00.000Z | NO | WATCH / NO TV READY: WAIT NEW RETEST; D1/H4 structure not aligned |
| NZDCAD | SHORT | 3/3 | 0 / -1 | 16.81 / 30.95 | WAIT BREAK | 0.78471 | 0.78605 | 2026-11-17T10:00:00.000Z | NO | WATCH / NO TV READY: WAIT BREAK; D1/H4 structure not aligned; ADX below 20 or missing |
| AUDJPY | SHORT | 3/3 | -1 / -1 | 52.63 / 65.66 | WAIT NEW RETEST | 107.586 | 107.237 | 2026-11-17T10:00:00.000Z | NO | WATCH / NO TV READY: WAIT NEW RETEST |
| GBPJPY | SHORT | 3/3 | 0 / -1 | 49.91 / 41.27 | WAIT NEW RETEST | 210.820 | 209.886 | 2026-11-17T10:00:00.000Z | NO | WATCH / NO TV READY: WAIT NEW RETEST; D1/H4 structure not aligned |
| EURUSD | SHORT | 3/3 | 0 / -1 | 43.31 / 25.70 | WAIT BREAK | 1.09850 | 1.09872 | 2026-11-17T10:00:00.000Z | NO | WATCH / NO TV READY: WAIT BREAK; D1/H4 structure not aligned |
| EURJPY | SHORT | 3/3 | 0 / -1 | 51.12 / 50.22 | WAIT NEW RETEST | 176.245 | 174.869 | 2026-11-17T10:00:00.000Z | NO | WATCH / NO TV READY: WAIT NEW RETEST; D1/H4 structure not aligned |
| GBPUSD | SHORT | 3/3 | 0 / 0 | 51.32 / 18.87 | WAIT BREAK | 1.31688 | 1.31878 | 2026-11-17T10:00:00.000Z | NO | WATCH / NO TV READY: WAIT BREAK; D1/H4 structure not aligned; ADX below 20 or missing |

**READY ισχύει μόνο όταν συμφωνούν και τα δύο μοντέλα:** η ανεξάρτητη TradingView Pine audit και το υπάρχον Yahoo/OANDA **Trend BRC**, για το **ίδιο κλεισμένο H1, direction και zone**. Το gate ελέγχει επίσης τη συμφωνία τιμής, φρέσκο snapshot, EMA50 3/3, D1/H4 δομή ίδιας κατεύθυνσης, ADX H4/H1 ≥ 20, έγκυρα θετικά επίπεδα και προσανατολισμό SL/TP, RR ≥ 1.2. Η απλή ένδειξη GitHub READY ή η παρουσία του snapshot δεν αρκεί. Απουσία/διαφωνία/παλαιότητα TV κρατά το Trend READY μπλοκαρισμένο ως TV UNVERIFIED.

**Καταστάσεις BRC:** 0 NO ALIGNMENT · 1 WAIT BREAK · 2 BREAK · 3 RETEST · 4 READY · 5 WAIT NEW RETEST. Δομή: 1 BULL, −1 BEAR, 0 χωρίς επιβεβαιωμένη κατεύθυνση. WATCH, BREAK και RETEST δεν είναι READY.

[Τελευταίο GitHub Forex scan](https://github.com/marioshinouda-byte/tvscreener/blob/main/LATEST_FOREX_SCAN.md) · [Snapshot JSON](https://github.com/marioshinouda-byte/tvscreener/blob/main/TRADINGVIEW_BRC_VERIFIED.json)

Το audit αφορά αποκλειστικά το **Trend BRC**. Δεν επαληθεύει το ξεχωριστό **HTF Reversal** και δεν περιλαμβάνει BTC/ETH/SOL. Περιέχει μόνο παράγωγες ενδείξεις, χωρίς πλήρη raw OHLC. Δεν αποτελεί εντολή συναλλαγής. Δεν ενεργοποιούνται READY alerts. Η επιτυχής ολοκλήρωση του νέου scanner workflow επαληθεύεται ξεχωριστά μετά το JSON push.
