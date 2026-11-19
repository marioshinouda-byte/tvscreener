# Latest Forex Scan

**Τελευταία ενημέρωση:** 20/11/2026 01:27 (Europe/Athens)

**Pairs:** 28  |  **Aligned:** 19  |  **A+ READY:** 0

**HTF Reversal mode:** ON  |  **Candidates:** 1  |  **READY:** 0

> Το score δείχνει συμφωνία των φίλτρων (/100), **όχι πιθανότητα κέρδους ή επιτυχίας**. Τιμή, EMA50, ADX, δομή, BRC και zones βασίζονται στα ίδια κλεισμένα κεριά Yahoo Finance.

> Το αρχικό μοντέλο υπολογίζει EMA50/ADX/structure/BRC από Yahoo OHLC. **Trend READY/Entry επιτρέπεται μόνο όταν το ανεξάρτητο TradingView Pine audit συμφωνεί** στο ίδιο κλεισμένο OANDA H1, κατεύθυνση, BRC zone και RR. Αν ο έλεγχος TV λείπει ή είναι παλιός, η είσοδος μπλοκάρεται ως TV UNVERIFIED. Το HTF Reversal είναι ξεχωριστό μοντέλο.
> **Δεδομένα:** τα Yahoo OHLC χρησιμοποιούνται για υπολογισμούς μόνο όταν η ώρα και το close του ίδιου κλεισμένου H1 συμφωνούν με ανεξάρτητη αναφορά OANDA (έως 8 pips). Δεν σημαίνει ταύτιση ολόκληρου του ιστορικού.
> Τα D1/H4 σχηματίζονται πλέον σε συνεδρίες Νέας Υόρκης 17:00, με αποκλεισμό των κλειστών ωρών Σαββατοκύριακου. Απαιτείται ακόμη ξεχωριστός έλεγχος ολόκληρου του ιστορικού OHLC.
> Στους πίνακες, η τιμή είναι το close του τελευταίου επαληθευμένου κλεισμένου H1. Δ zone = close μείον H1 zone σε pips (+ πάνω από τη zone, − κάτω από τη zone).

> **W1 / Weekly:** χρησιμοποιείται ως ανώτερο context και εμφανίζεται στο scan. **Δεν αλλάζει** το A+ rule: D1/H4/H1 alignment + EMA50 3/3 + D1/H4 structure + ADX + **confirmation ηλικίας έως 3 κλεισμένων H1 κεριών**, χωρίς ακύρωση ή υπερβολική απόσταση από τη zone + **RR ≥ 1.2**.

## 🟢 ENTRY READY — Trend


> **Πηγές δεδομένων:** Yahoo OHLC + OANDA H1 διασταύρωση. Επαληθευμένα: 23/28 · Απορρίφθηκαν: 5. Για πλήρη εικόνα δες τους λόγους απόρριψης παρακάτω.

| Ζευγάρι | Κατάσταση πηγής |
|---|---|
| EURNZD | PRICE-MISMATCH |
| GBPJPY | PRICE-MISMATCH |
| GBPCAD | PRICE-MISMATCH |
| GBPNZD | PRICE-MISMATCH |
| CHFJPY | PRICE-MISMATCH |

Κανένα A+ READY στο τρέχον scan.

> Η ένδειξη απαιτεί έλεγχο στο τρέχον chart, spread, ειδήσεων και μεγέθους θέσης πριν από οποιαδήποτε είσοδο.

## OANDA — αυτόματο πρώτο φίλτρο (έως 5 ζευγάρια)

**5 ζευγάρια προς έλεγχο** — δες το [OANDA_SHORTLIST.md](OANDA_SHORTLIST.md). Μόνο ενδείξεις TradingView OANDA, χωρίς BRC/READY. Το report εμφανίζει H1 OANDA timestamps, αλλά δεν έχει επιβεβαιωμένο πλήρες OHLC ιστορικό.

## Weekly Top 5 — 2026-W47 (Europe/Athens)

Η πεντάδα διατηρείται όλη την εβδομάδα· ανανεώνονται score και κατάσταση σε κάθε scan. Μόνο νέο επιβεβαιωμένο setup με RR ≥ 1.2 μπορεί να αντικαταστήσει θέση. Νέα επιλογή γίνεται τη Δευτέρα (ώρα Ελλάδας).

| # | Pair | Dir | Agreement /100 | Κατάσταση | B→R→C | H1 Zone | Τιμή | Απόσταση zone | Κλεισμένο H1 (ώρα Αθήνας) | RR |
|---:|---|---|---:|---|---|---:|---:|---:|---|---:|
| 1 | **AUDCAD** | SHORT | **55.0/100** | **⚪ WAIT** | WAIT NEW RETEST | 0.95537 | 0.95377 | -16.0 pips | 20/11 00:00–01:00 | — |
| 2 | **AUDJPY** | SHORT | **65.0/100** | **⚪ WAIT** | BREAK | 106.215 | 106.194 | -2.1 pips | 20/11 00:00–01:00 | — |
| 3 | **GBPAUD** | LONG | **55.0/100** | **⚪ WAIT** | WAIT FOR BREAK | 1.97096 | 1.96617 | -47.9 pips | 20/11 00:00–01:00 | — |
| 4 | **AUDUSD** | SHORT | **80.8/100** | **🟡 WATCH** | RETEST | 0.66653 | 0.66569 | -8.4 pips | 20/11 00:00–01:00 | — |
| 5 | **GBPUSD** | SHORT | **55.0/100** | **⚪ WAIT** | WAIT NEW RETEST | 1.31215 | 1.30904 | -31.1 pips | 20/11 00:00–01:00 | — |

## Νέοι υποψήφιοι για παρακολούθηση — Trend

Νέα ζευγάρια εκτός πεντάδας με agreement score ≥ 70/100 και D1/H4 structure + EMA50 ή setup A/A+. Είναι υποψήφια για παρακολούθηση, όχι σήματα εισόδου· είσοδος εξετάζεται μόνο σε ENTRY READY.

| Pair | Dir | Agreement /100 | Κατάσταση | B→R→C | H1 Zone | Τιμή | Απόσταση zone | Κλεισμένο H1 (ώρα Αθήνας) |
|---|---|---:|---|---|---:|---:|---:|---|
| **EURAUD** | LONG | **85.0/100** | **⚪ WAIT** | TV UNVERIFIED | 1.64561 | 1.64780 | +21.9 pips | 20/11 00:00–01:00 |

> **Agreement score /100 = βαθμός συμφωνίας φίλτρων, όχι πιθανότητα επιτυχίας.** 🔴 INVALID σημαίνει ότι χάθηκε το alignment ή δεν υπάρχουν αξιόπιστα δεδομένα στο τρέχον scan.

## Όλοι οι τρέχοντες Trend candidates

| # | Pair | Dir | Setup | Bias | EMA50 | D1 Struct | H4 Struct | ADX H4 | ADX H1 | B→R→C | H1 Zone | Τιμή | Δ zone | Κλεισμένο H1 (ώρα Αθήνας) | Entry | SL | TP | RR | Agreement /100 |
|---:|---|---|---|---|---:|---|---|---:|---:|---|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 1 | **AUDUSD** | SHORT | **A** | ALIGNED | 3/3 | BEAR | BEAR | 59.6 | 35.9 | **RETEST** | 0.66653 | 0.66569 | -8.4 pips | 20/11 00:00–01:00 | — | — | — | **—** | **80.8/100** |
| 2 | **EURAUD** | LONG | **WATCH** | ALIGNED | 3/3 | BULL | BULL | 28.0 | 32.3 | **TV UNVERIFIED** | 1.64561 | 1.64780 | +21.9 pips | 20/11 00:00–01:00 | — | — | — | **—** | **85.0/100** |
| 3 | **AUDJPY** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 44.8 | 31.7 | **BREAK** | 106.215 | 106.194 | -2.1 pips | 20/11 00:00–01:00 | — | — | — | **—** | **65.0/100** |
| 4 | **NZDUSD** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BULL | 32.6 | 22.2 | **BREAK** | 0.54855 | 0.54816 | -3.9 pips | 20/11 00:00–01:00 | — | — | — | **—** | **57.0/100** |
| 5 | **AUDCAD** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 34.3 | 32.3 | **WAIT NEW RETEST** | 0.95537 | 0.95377 | -16.0 pips | 20/11 00:00–01:00 | — | — | — | **—** | **55.0/100** |
| 6 | **AUDCHF** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 18.8 | 26.9 | **WAIT FOR BREAK** | 0.56131 | 0.56138 | +0.7 pips | 20/11 00:00–01:00 | — | — | — | **—** | **55.0/100** |
| 7 | **AUDNZD** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 51.7 | 45.5 | **WAIT NEW RETEST** | 1.21309 | 1.21387 | +7.8 pips | 20/11 00:00–01:00 | — | — | — | **—** | **55.0/100** |
| 8 | **GBPAUD** | LONG | **WATCH** | ALIGNED | 3/3 | BULL | BULL | 27.3 | 17.2 | **WAIT FOR BREAK** | 1.97096 | 1.96617 | -47.9 pips | 20/11 00:00–01:00 | — | — | — | **—** | **55.0/100** |
| 9 | **GBPUSD** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 46.7 | 39.3 | **WAIT NEW RETEST** | 1.31215 | 1.30904 | -31.1 pips | 20/11 00:00–01:00 | — | — | — | **—** | **55.0/100** |
| 10 | **USDCAD** | LONG | **WATCH** | ALIGNED | 3/3 | BULL | BULL | 39.2 | 21.9 | **WAIT FOR BREAK** | 1.43573 | 1.43372 | -20.1 pips | 20/11 00:00–01:00 | — | — | — | **—** | **55.0/100** |
| 11 | **NZDJPY** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BULL | 49.1 | 28.4 | **WAIT FOR BREAK** | 87.125 | 87.430 | +30.5 pips | 20/11 00:00–01:00 | — | — | — | **—** | **51.9/100** |
| 12 | **USDJPY** | LONG | **WATCH** | ALIGNED | 3/3 | BULL | BULL | 14.5 | 19.2 | **WAIT FOR BREAK** | 159.970 | 159.612 | -35.8 pips | 20/11 00:00–01:00 | — | — | — | **—** | **50.7/100** |
| 13 | **EURUSD** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BULL | 38.4 | 19.8 | **WAIT FOR BREAK** | 1.09589 | 1.09733 | +14.4 pips | 20/11 00:00–01:00 | — | — | — | **—** | **49.1/100** |
| 14 | **EURJPY** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BULL | 42.6 | 24.8 | **WAIT FOR BREAK** | 174.432 | 175.036 | +60.4 pips | 20/11 00:00–01:00 | — | — | — | **—** | **48.9/100** |
| 15 | **CADJPY** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BULL | 31.8 | 23.9 | **WAIT FOR BREAK** | 111.057 | 111.291 | +23.4 pips | 20/11 00:00–01:00 | — | — | — | **—** | **48.7/100** |
| 16 | **USDCHF** | LONG | **WATCH** | ALIGNED | 3/3 | BEAR | BULL | 30.6 | 15.0 | **WAIT FOR BREAK** | 0.84430 | 0.84350 | -8.0 pips | 20/11 00:00–01:00 | — | — | — | **—** | **44.9/100** |
| 17 | **NZDCAD** | SHORT | **WATCH** | ALIGNED | 3/3 | BULL | BULL | 16.2 | 31.7 | **WAIT FOR BREAK** | 0.78518 | 0.78525 | +0.7 pips | 20/11 00:00–01:00 | — | — | — | **—** | **39.3/100** |
| 18 | **CADCHF** | LONG | **WATCH** | MIXED | 2/3 | BEAR | BULL | 22.6 | 14.3 | **WAIT FOR BREAK** | 0.58960 | 0.58796 | -16.4 pips | 20/11 00:00–01:00 | — | — | — | **—** | **32.3/100** |
| 19 | **EURCAD** | SHORT | **WATCH** | ALIGNED | 3/3 | BULL | BULL | 28.3 | 13.1 | **WAIT FOR BREAK** | 1.56694 | 1.57227 | +53.3 pips | 20/11 00:00–01:00 | — | — | — | **—** | **27.4/100** |

### Rating detail

| Pair | W1 | D1 | H4 | H1 | Direction |
|---|---|---|---|---|---|
| AUDUSD | STRONG SELL | SELL | STRONG SELL | STRONG SELL | SHORT |
| EURAUD | BUY | STRONG BUY | STRONG BUY | STRONG BUY | LONG |
| AUDJPY | SELL | SELL | STRONG SELL | SELL | SHORT |
| NZDUSD | STRONG SELL | SELL | SELL | SELL | SHORT |
| AUDCAD | SELL | STRONG SELL | STRONG SELL | STRONG SELL | SHORT |
| AUDCHF | SELL | STRONG SELL | STRONG SELL | STRONG SELL | SHORT |
| AUDNZD | SELL | SELL | SELL | SELL | SHORT |
| GBPAUD | BUY | BUY | STRONG BUY | STRONG BUY | LONG |
| GBPUSD | STRONG SELL | SELL | SELL | SELL | SHORT |
| USDCAD | STRONG BUY | BUY | BUY | BUY | LONG |
| NZDJPY | STRONG SELL | SELL | SELL | SELL | SHORT |
| USDJPY | STRONG BUY | BUY | BUY | BUY | LONG |
| EURUSD | STRONG SELL | SELL | SELL | SELL | SHORT |
| EURJPY | SELL | SELL | SELL | SELL | SHORT |
| CADJPY | SELL | SELL | SELL | SELL | SHORT |
| USDCHF | BUY | BUY | BUY | BUY | LONG |
| NZDCAD | SELL | SELL | STRONG SELL | STRONG SELL | SHORT |
| CADCHF | BUY | BUY | BUY | NEUTRAL | LONG |
| EURCAD | SELL | SELL | NEUTRAL | BUY | SHORT |

## Crypto Watch — BTC / ETH / SOL

> Crypto δεδομένα από TradingView Crypto Screener. Το W1 είναι context· η κατεύθυνση εξακολουθεί να απαιτεί D1/H4/H1 alignment.

| Asset | Market | Price | W1 | D1 | H4 | H1 | Direction | W1 Context |
|---|---|---:|---|---|---|---|---|---|
| **BTC** | COINBASE:BTCUSD | 61,839.95 | STRONG SELL | STRONG SELL | STRONG SELL | SELL | **SHORT** | ✅ SUPPORTS |
| **ETH** | COINBASE:ETHUSD | 1,750.98 | STRONG SELL | STRONG SELL | STRONG SELL | SELL | **SHORT** | ✅ SUPPORTS |
| **SOL** | COINBASE:SOLUSD | 72.9700 | SELL | STRONG SELL | SELL | SELL | **SHORT** | ✅ SUPPORTS |

## HTF Reversal — ξεχωριστό mode

> Δεν αναμειγνύεται με το A+ Trend. Απαιτεί επιβεβαιωμένο D1 pivot με τουλάχιστον 2 ανεξάρτητες επαφές, H4 δομή προς την αναστροφή και H1 BRC. Όταν η H4 δομή είναι αντίθετη, μένει WATCH με score έως 65. Πριν από το break, ARMED απαιτεί απόσταση έως 1.5× H1 ATR. Το shortlist κρατά score ≥ 75. READY απαιτεί RR ≥ 3.0.
> **Το HTF Reversal Score μετρά συμφωνία context (/100), όχι πιθανότητα κέρδους. ΑΝΑΜΟΝΗ H1 ΕΠΙΒΕΒΑΙΩΣΗΣ / WAIT RETEST / ARMED δεν είναι είσοδος. Entry/SL/TP εμφανίζονται μόνο σε READY, με RR ≥ 3.0.**

| # | Pair | Dir | State | D1 Zone | H4 Struct | Sweep | Reject | Displ. | H1 BRC | H1 Zone | Τιμή | Δ H1 zone | Κλεισμένο H1 (ώρα Αθήνας) | Entry | SL | TP | RR | Context score /100 | Σημείωση |
|---:|---|---|---|---:|---|---:|---:|---:|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|
| 1 | **CADCHF** | LONG | **ARMED · ΑΝΑΜΟΝΗ BREAK** | 0.58614 | BULL | ✅ | ✅ | ✅ | WAIT FOR BREAK | 0.58960 | 0.58796 | -16.4 pips | 20/11 00:00–01:00 | — | — | — | — | **89.6/100** | HTF αντίδραση — H1 break κοντά (1.1 ATR) |

_Εκτός shortlist: WATCH 5 | INVALID 12. Δεν θεωρούνται ενεργά candidates._

### Καταστάσεις HTF Reversal

- **WATCH:** η τιμή αντέδρασε σε επιβεβαιωμένη D1 zone, αλλά δεν υπάρχει ακόμη αρκετή H4 επιβεβαίωση.
- **ΑΝΑΜΟΝΗ H1 ΕΠΙΒΕΒΑΙΩΣΗΣ:** έγινε H1 retest και περιμένει νέο κλεισμένο H1 candle να επιβεβαιώσει· δεν είναι είσοδος.
- **ARMED · ΑΝΑΜΟΝΗ BREAK:** ισχυρό HTF context με το απαιτούμενο H1 break έως 1.5× H1 ATR· μπαίνει στο shortlist μόνο με score ≥ 75. Δεν είναι είσοδος.
- **WAIT RETEST:** έγινε H1 break και περιμένει επιστροφή στη broken zone.
- **READY:** fresh confirmation στο τελευταίο κλεισμένο H1 και RR ≥ 3.0 προς την επόμενη D1 zone.
- **INVALID:** παραβίαση D1 zone, ληγμένο H1 setup, υπερβολική απομάκρυνση ή RR < 3.0.
- Απενεργοποίηση χωρίς αφαίρεση κώδικα: `ENABLE_HTF_REVERSAL=false python forex_scanner.py`.

## Όλα τα 28 Forex pairs

| Pair | W1 | D1 | H4 | H1 | Dir | EMA | D1 Struct | H4 Struct | BRC | RR | Quality |
|---|---|---|---|---|---|---:|---|---|---|---:|---:|
| AUDCAD | SELL | STRONG SELL | STRONG SELL | STRONG SELL | SHORT | 3/3 | BEAR | BEAR | WAIT NEW RETEST | — | 55.0 |
| AUDCHF | SELL | STRONG SELL | STRONG SELL | STRONG SELL | SHORT | 3/3 | BEAR | BEAR | WAIT FOR BREAK | — | 55.0 |
| AUDJPY | SELL | SELL | STRONG SELL | SELL | SHORT | 3/3 | BEAR | BEAR | BREAK | — | 65.0 |
| AUDNZD | SELL | SELL | SELL | SELL | SHORT | 3/3 | BEAR | BEAR | WAIT NEW RETEST | — | 55.0 |
| AUDUSD | STRONG SELL | SELL | STRONG SELL | STRONG SELL | SHORT | 3/3 | BEAR | BEAR | RETEST | — | 80.8 |
| CADCHF | BUY | BUY | BUY | NEUTRAL | LONG | 2/3 | BEAR | BULL | WAIT FOR BREAK | — | 32.3 |
| CADJPY | SELL | SELL | SELL | SELL | SHORT | 3/3 | BEAR | BULL | WAIT FOR BREAK | — | 48.7 |
| CHFJPY | SELL | SELL | SELL | SELL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| EURAUD | BUY | STRONG BUY | STRONG BUY | STRONG BUY | LONG | 3/3 | BULL | BULL | TV UNVERIFIED | — | 85.0 |
| EURCAD | SELL | SELL | NEUTRAL | BUY | SHORT | 3/3 | BULL | BULL | WAIT FOR BREAK | — | 27.4 |
| EURCHF | SELL | NEUTRAL | BUY | NEUTRAL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| EURGBP | SELL | NEUTRAL | BUY | BUY | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| EURJPY | SELL | SELL | SELL | SELL | SHORT | 3/3 | BEAR | BULL | WAIT FOR BREAK | — | 48.9 |
| EURNZD | STRONG BUY | BUY | STRONG BUY | BUY | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| EURUSD | STRONG SELL | SELL | SELL | SELL | SHORT | 3/3 | BEAR | BULL | WAIT FOR BREAK | — | 49.1 |
| GBPAUD | BUY | BUY | STRONG BUY | STRONG BUY | LONG | 3/3 | BULL | BULL | WAIT FOR BREAK | — | 55.0 |
| GBPCAD | NEUTRAL | SELL | SELL | STRONG SELL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| GBPCHF | BUY | BUY | SELL | SELL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| GBPJPY | SELL | SELL | SELL | SELL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| GBPNZD | BUY | BUY | NEUTRAL | NEUTRAL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| GBPUSD | STRONG SELL | SELL | SELL | SELL | SHORT | 3/3 | BEAR | BEAR | WAIT NEW RETEST | — | 55.0 |
| NZDCAD | SELL | SELL | STRONG SELL | STRONG SELL | SHORT | 3/3 | BULL | BULL | WAIT FOR BREAK | — | 39.3 |
| NZDCHF | SELL | SELL | SELL | SELL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| NZDJPY | STRONG SELL | SELL | SELL | SELL | SHORT | 3/3 | BEAR | BULL | WAIT FOR BREAK | — | 51.9 |
| NZDUSD | STRONG SELL | SELL | SELL | SELL | SHORT | 3/3 | BEAR | BULL | BREAK | — | 57.0 |
| USDCAD | STRONG BUY | BUY | BUY | BUY | LONG | 3/3 | BULL | BULL | WAIT FOR BREAK | — | 55.0 |
| USDCHF | BUY | BUY | BUY | BUY | LONG | 3/3 | BEAR | BULL | WAIT FOR BREAK | — | 44.9 |
| USDJPY | STRONG BUY | BUY | BUY | BUY | LONG | 3/3 | BULL | BULL | WAIT FOR BREAK | — | 50.7 |

## Πώς διαβάζεται

- **W1 / Weekly:** ανώτερο context. SUPPORTS όταν συμφωνεί με το D1/H4/H1 direction, OPPOSES όταν είναι αντίθετο. Δεν μπλοκάρει μόνο του ένα A+ setup.
- **Κατεύθυνση:** EMA50 slope/close από κλεισμένα Yahoo candles· D1 και H4 ορίζουν την κατεύθυνση, H1 είναι το timing filter. Τα TradingView ratings είναι context.
- **EMA50 3/3:** τιμή και κλίση EMA50 συμφωνούν με την κατεύθυνση και στα 3 TF.
- **D1/H4 Struct:** BULL ή BEAR από ολοκληρωμένα swing highs/lows.
- **ADX:** πάνω από ~20 δείχνει ισχυρότερη τάση· δεν είναι μόνο του σήμα εισόδου.
- **BRC:** break σε επιβεβαιωμένο H1 swing, retest στη ζώνη και confirmation με κλείσιμο πέρα από το high/low του retest candle. READY ισχύει μόνο για confirmation στο τελευταίο ή αμέσως προηγούμενο κλεισμένο H1. Ανοιχτά κεριά αποκλείονται.
- **Entry/SL/TP:** εμφανίζονται μόνο όταν το BRC είναι READY. Entry = τελευταίο κλεισμένο H1, SL = H1 zone ± 0.35×ATR, TP = κοντινότερο ολοκληρωμένο H4 swing target.
- **RR:** ✅ όταν RR ≥ 1.2, ❌ όταν είναι χαμηλότερο. Το A+ READY απαιτεί RR pass.
- **A+ READY (Trend):** απαιτεί συμφωνία Yahoo/OANDA H1 και ανεξάρτητο TradingView Pine audit στα D1/H4/H1 με ίδιο H1/zone/κατεύθυνση. Χωρίς φρέσκια ανεξάρτητη επιβεβαίωση δεν εμφανίζεται Entry. Πριν από trade χρειάζεται οπτικός έλεγχος chart, spread/news και sizing.
