# TradingView BRC — ανεξάρτητος ωριαίος έλεγχος Trend

**Ώρα Ελλάδας:** 20/11/2026, 02:29:49 (Europe/Athens)  
**UTC:** 2026-11-20T00:29:49Z  
**Πρόσβαση TradingView Pine:** επιτυχής για 7/7 ζευγάρια.  
**Ανεξάρτητο TV READY:** 0/7.

Όλες οι κλήσεις επέστρεψαν success=true, το ακριβές ζητούμενο σύμβολο OANDA, τον ταυτοποιημένο δείκτη και τα αναμενόμενα metainfo.plots. Χρησιμοποιήθηκε αποκλειστικά το last_values της τελευταίας κλεισμένης H1, όχι το τελευταίο forming candle του values[].

**Δείκτης:** BRC TV Triple TF Audit v1, `USER;ae27f010fee5413b8f5d1cc39e592cde`.  
**Παράμετροι:** OANDA:PAIR, timeframe=1h, calc_bars_count=500, return_bars=1.  
**Πηγή:** TradingView Pine. Παράγωγα audit signals μόνο, χωρίς raw OHLC candles.

## Κάλυψη

- Weekly Top 5: AUDCAD, AUDJPY, GBPAUD, AUDUSD, GBPUSD.
- OANDA Top 5: AUDCAD, EURAUD, AUDUSD, AUDCHF, AUDJPY.
- Trend TV UNVERIFIED / READY στο report εισόδου: EURAUD (TV UNVERIFIED).
- Πρόσθετοι εκτός πεντάδων: κανένας.
- Μοναδικά ζευγάρια: 7. Εξετάστηκαν όλες οι γραμμές Trend και ο πίνακας όλων των 28 Forex pairs. Crypto και HTF Reversal εξαιρούνται.

## Ανεξάρτητος πίνακας TradingView Pine

| Pair | Πηγή | H1 open UTC | Direction | EMA | D1/H4 structure | ADX H4/H1 | BRC | Zone | Κλεισμένη H1 τιμή | verified_ready | tv_ready | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AUDCAD | TradingView Pine | 2026-11-19T23:00:00Z | SHORT | 3/3 | -1 / -1 | 45.67 / 42.12 | 5 WAIT NEW RETEST | 0.95609 | 0.9547 | 0 | false | WATCH / WAIT NEW RETEST / NO TV READY |
| AUDJPY | TradingView Pine | 2026-11-19T23:00:00Z | SHORT | 3/3 | -1 / 0 | 46.95 / 34.13 | 1 WAIT BREAK | 106.22 | 106.307 | 0 | false | WATCH / WAIT BREAK / NO TV READY |
| GBPAUD | TradingView Pine | 2026-11-19T23:00:00Z | LONG | 3/3 | 0 / 0 | 37.67 / 25.32 | 1 WAIT BREAK | 1.97104 | 1.96606 | 0 | false | WATCH / WAIT BREAK / NO TV READY |
| AUDUSD | TradingView Pine | 2026-11-19T23:00:00Z | SHORT | 3/3 | -1 / -1 | 57.66 / 38.30 | 3 RETEST | 0.66618 | 0.66559 | 0 | false | WATCH / RETEST / NO TV READY |
| GBPUSD | TradingView Pine | 2026-11-19T23:00:00Z | SHORT | 3/3 | 0 / -1 | 46.30 / 41.76 | 5 WAIT NEW RETEST | 1.31203 | 1.3086 | 0 | false | WATCH / WAIT NEW RETEST / NO TV READY |
| EURAUD | TradingView Pine | 2026-11-19T23:00:00Z | LONG | 3/3 | 1 / 1 | 36.48 / 40.63 | 5 WAIT NEW RETEST | 1.64566 | 1.64782 | 0 | false | WATCH / WAIT NEW RETEST / NO TV READY |
| AUDCHF | TradingView Pine | 2026-11-19T23:00:00Z | SHORT | 3/3 | 0 / -1 | 23.07 / 31.93 | 3 RETEST | 0.56202 | 0.56194 | 0 | false | WATCH / RETEST / NO TV READY |

Η κοινή H1 άνοιξε 2026-11-19T23:00:00Z και έκλεισε 2026-11-20T00:00:00Z. Κατά την επικύρωση (2026-11-20T00:28:40Z) η ηλικία κλεισίματος ήταν 1720 δευτερόλεπτα, εντός του ορίου 0–2 ωρών με ανοχή 2 λεπτών. Οι αποκρίσεις δήλωσαν ότι το τελευταίο bar σχηματιζόταν ακόμη· αυτό αποκλείστηκε.

**Structure:** 1 BULL · 0 NEUTRAL · -1 BEAR. Τα ADX στον πίνακα εμφανίζονται στρογγυλοποιημένα σε 2 δεκαδικά· το JSON διατηρεί την ακρίβεια του TradingView. Entry/SL/TP/RR είναι null για κάθε tv_ready=false. Δεν χρησιμοποιήθηκαν δεδομένα προηγούμενου audit.

**BRC:** 0 NO ALIGNMENT · 1 WAIT BREAK · 2 BREAK · 3 RETEST · 4 READY · 5 WAIT NEW RETEST.

READY ισχύει μόνο όταν συμφωνούν η ανεξάρτητη TradingView Pine audit και το Yahoo/OANDA Trend BRC για το **ΙΔΙΟ κλεισμένο H1, direction και zone**. Το GitHub READY μόνο του δεν αρκεί. Το EURAUD επέστρεψε WAIT NEW RETEST και verified_ready=0 στο ανεξάρτητο Pine audit.

Το tv_ready=true απαιτεί success=true, ακριβές OANDA symbol και ταυτοποιημένο δείκτη, last_values από κλεισμένο H1 με ηλικία κλεισίματος 0–2 ώρες (ανοχή 2 λεπτών), verified_ready=1, BRC=4, EMA=3/3, ίδια direction σε D1/H4 structure, ADX H4/H1 ≥20, θετικά πεπερασμένα zone/entry/SL/TP, σωστό προσανατολισμό SL/TP και RR ≥1.2, ελεγμένο και από τις αποστάσεις entry/stop/target.

Το JSON push εκκινεί νέο scan με το TradingView gate. Η ολοκλήρωση ελέγχεται μετά το push από το workflow και νέα εγγραφή υγείας. Το Trend audit δεν επιβεβαιώνει HTF Reversal, δεν ενεργοποιεί READY alerts και δεν δίνει εντολές συναλλαγών.

[Τελευταίο report](LATEST_FOREX_SCAN.md) · [Snapshot audit](TRADINGVIEW_BRC_VERIFIED.json)
