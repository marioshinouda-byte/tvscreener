# Latest Forex Scan

**Τελευταία ενημέρωση:** 20/11/2026 18:32 (Europe/Athens)

**Pairs:** 28  |  **Aligned:** 22  |  **A+ READY:** 0

**HTF Reversal mode:** ON  |  **Candidates:** 3  |  **READY:** 0

> Το score δείχνει συμφωνία των φίλτρων (/100), **όχι πιθανότητα κέρδους ή επιτυχίας**. Τιμή, EMA50, ADX, δομή, BRC και zones βασίζονται στα ίδια κλεισμένα κεριά Yahoo Finance.

> Το αρχικό μοντέλο υπολογίζει EMA50/ADX/structure/BRC από Yahoo OHLC. **Trend READY/Entry επιτρέπεται μόνο όταν το ανεξάρτητο TradingView Pine audit συμφωνεί** στο ίδιο κλεισμένο OANDA H1, κατεύθυνση, BRC zone και RR. Αν ο έλεγχος TV λείπει ή είναι παλιός, η είσοδος μπλοκάρεται ως TV UNVERIFIED. Το HTF Reversal είναι ξεχωριστό μοντέλο.
> **Δεδομένα:** τα Yahoo OHLC χρησιμοποιούνται για υπολογισμούς μόνο όταν η ώρα και το close του ίδιου κλεισμένου H1 συμφωνούν με ανεξάρτητη αναφορά OANDA (έως 8 pips). Δεν σημαίνει ταύτιση ολόκληρου του ιστορικού.
> Τα D1/H4 σχηματίζονται πλέον σε συνεδρίες Νέας Υόρκης 17:00, με αποκλεισμό των κλειστών ωρών Σαββατοκύριακου. Απαιτείται ακόμη ξεχωριστός έλεγχος ολόκληρου του ιστορικού OHLC.
> Στους πίνακες, η τιμή είναι το close του τελευταίου επαληθευμένου κλεισμένου H1. Δ zone = close μείον H1 zone σε pips (+ πάνω από τη zone, − κάτω από τη zone).

> **W1 / Weekly:** χρησιμοποιείται ως ανώτερο context και εμφανίζεται στο scan. **Δεν αλλάζει** το A+ rule: D1/H4/H1 alignment + EMA50 3/3 + D1/H4 structure + ADX + **confirmation ηλικίας έως 3 κλεισμένων H1 κεριών**, χωρίς ακύρωση ή υπερβολική απόσταση από τη zone + **RR ≥ 1.2**.

## 🟢 ENTRY READY — Trend


> **Πηγές δεδομένων:** Yahoo OHLC + OANDA H1 διασταύρωση. Επαληθευμένα: 27/28 · Απορρίφθηκαν: 1. Για πλήρη εικόνα δες τους λόγους απόρριψης παρακάτω.

| Ζευγάρι | Κατάσταση πηγής |
|---|---|
| GBPCAD | N/A |

Κανένα A+ READY στο τρέχον scan.

> Η ένδειξη απαιτεί έλεγχο στο τρέχον chart, spread, ειδήσεων και μεγέθους θέσης πριν από οποιαδήποτε είσοδο.

## OANDA — αυτόματο πρώτο φίλτρο (έως 5 ζευγάρια)

**5 ζευγάρια προς έλεγχο** — δες το [OANDA_SHORTLIST.md](OANDA_SHORTLIST.md). Μόνο ενδείξεις TradingView OANDA, χωρίς BRC/READY. Το report εμφανίζει H1 OANDA timestamps, αλλά δεν έχει επιβεβαιωμένο πλήρες OHLC ιστορικό.

## Weekly Top 5 — 2026-W47 (Europe/Athens)

Η πεντάδα διατηρείται όλη την εβδομάδα· ανανεώνονται score και κατάσταση σε κάθε scan. Μόνο νέο επιβεβαιωμένο setup με RR ≥ 1.2 μπορεί να αντικαταστήσει θέση. Νέα επιλογή γίνεται τη Δευτέρα (ώρα Ελλάδας).

| # | Pair | Dir | Agreement /100 | Κατάσταση | B→R→C | H1 Zone | Τιμή | Απόσταση zone | Κλεισμένο H1 (ώρα Αθήνας) | RR |
|---:|---|---|---:|---|---|---:|---:|---:|---|---:|
| 1 | **AUDUSD** | SHORT | **65.0/100** | **⚪ WAIT** | BREAK | 0.66489 | 0.66476 | -1.3 pips | 20/11 17:00–18:00 | — |
| 2 | **AUDCHF** | SHORT | **55.0/100** | **⚪ WAIT** | WAIT NEW RETEST | 0.56131 | 0.55771 | -36.0 pips | 20/11 17:00–18:00 | — |
| 3 | **AUDJPY** | SHORT | **55.0/100** | **⚪ WAIT** | WAIT NEW RETEST | 106.215 | 105.475 | -74.0 pips | 20/11 17:00–18:00 | — |
| 4 | **AUDCAD** | SHORT | **65.0/100** | **⚪ WAIT** | BREAK | 0.95204 | 0.95173 | -3.1 pips | 20/11 17:00–18:00 | — |
| 5 | **EURJPY** | SHORT | **55.0/100** | **⚪ WAIT** | WAIT NEW RETEST | 174.432 | 174.334 | -9.8 pips | 20/11 17:00–18:00 | — |

## Νέοι υποψήφιοι για παρακολούθηση — Trend

Νέα ζευγάρια εκτός πεντάδας με agreement score ≥ 70/100 και D1/H4 structure + EMA50 ή setup A/A+. Είναι υποψήφια για παρακολούθηση, όχι σήματα εισόδου· είσοδος εξετάζεται μόνο σε ENTRY READY.

Κανένα νέο ζευγάρι που να περνά τα κριτήρια.

> **Agreement score /100 = βαθμός συμφωνίας φίλτρων, όχι πιθανότητα επιτυχίας.** 🔴 INVALID σημαίνει ότι χάθηκε το alignment ή δεν υπάρχουν αξιόπιστα δεδομένα στο τρέχον scan.

## Όλοι οι τρέχοντες Trend candidates

| # | Pair | Dir | Setup | Bias | EMA50 | D1 Struct | H4 Struct | ADX H4 | ADX H1 | B→R→C | H1 Zone | Τιμή | Δ zone | Κλεισμένο H1 (ώρα Αθήνας) | Entry | SL | TP | RR | Agreement /100 |
|---:|---|---|---|---|---:|---|---|---:|---:|---|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 1 | **AUDCAD** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 39.1 | 36.4 | **BREAK** | 0.95204 | 0.95173 | -3.1 pips | 20/11 17:00–18:00 | — | — | — | **—** | **65.0/100** |
| 2 | **AUDUSD** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 58.1 | 26.8 | **BREAK** | 0.66489 | 0.66476 | -1.3 pips | 20/11 17:00–18:00 | — | — | — | **—** | **65.0/100** |
| 3 | **EURAUD** | LONG | **WATCH** | ALIGNED | 3/3 | BULL | BULL | 32.8 | 35.7 | **BREAK** | 1.65085 | 1.65260 | +17.5 pips | 20/11 17:00–18:00 | — | — | — | **—** | **65.0/100** |
| 4 | **GBPAUD** | LONG | **WATCH** | ALIGNED | 3/3 | BULL | BULL | 27.8 | 19.7 | **BREAK** | 1.97051 | 1.97138 | +8.7 pips | 20/11 17:00–18:00 | — | — | — | **—** | **65.0/100** |
| 5 | **EURCHF** | SHORT | **WATCH** | ALIGNED | 3/3 | BULL | BEAR | 13.8 | 32.4 | **BREAK** | 0.92200 | 0.92174 | -2.6 pips | 20/11 17:00–18:00 | — | — | — | **—** | **55.2/100** |
| 6 | **AUDCHF** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 23.8 | 48.2 | **WAIT NEW RETEST** | 0.56131 | 0.55771 | -36.0 pips | 20/11 17:00–18:00 | — | — | — | **—** | **55.0/100** |
| 7 | **AUDJPY** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 44.6 | 40.6 | **WAIT NEW RETEST** | 106.215 | 105.475 | -74.0 pips | 20/11 17:00–18:00 | — | — | — | **—** | **55.0/100** |
| 8 | **AUDNZD** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 55.8 | 53.3 | **WAIT FOR BREAK** | 1.20953 | 1.21052 | +9.9 pips | 20/11 17:00–18:00 | — | — | — | **—** | **55.0/100** |
| 9 | **CADJPY** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 30.7 | 33.5 | **WAIT NEW RETEST** | 111.057 | 110.828 | -22.9 pips | 20/11 17:00–18:00 | — | — | — | **—** | **55.0/100** |
| 10 | **EURJPY** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 40.5 | 32.8 | **WAIT NEW RETEST** | 174.432 | 174.334 | -9.8 pips | 20/11 17:00–18:00 | — | — | — | **—** | **55.0/100** |
| 11 | **GBPJPY** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 55.0 | 43.2 | **WAIT NEW RETEST** | 209.134 | 207.956 | -117.8 pips | 20/11 17:00–18:00 | — | — | — | **—** | **55.0/100** |
| 12 | **GBPUSD** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 45.3 | 22.4 | **WAIT FOR BREAK** | 1.30808 | 1.31017 | +20.9 pips | 20/11 17:00–18:00 | — | — | — | **—** | **55.0/100** |
| 13 | **NZDCHF** | SHORT | **WATCH** | ALIGNED | 3/3 | BULL | BEAR | 47.1 | 39.0 | **WAIT FOR BREAK** | 0.45995 | 0.46067 | +7.2 pips | 20/11 17:00–18:00 | — | — | — | **—** | **55.0/100** |
| 14 | **NZDJPY** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 46.6 | 30.7 | **WAIT FOR BREAK** | 87.074 | 87.128 | +5.4 pips | 20/11 17:00–18:00 | — | — | — | **—** | **55.0/100** |
| 15 | **NZDUSD** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 28.1 | 13.5 | **WAIT FOR BREAK** | 0.54777 | 0.54906 | +12.9 pips | 20/11 17:00–18:00 | — | — | — | **—** | **55.0/100** |
| 16 | **CHFJPY** | SHORT | **WATCH** | ALIGNED | 3/3 | BULL | BEAR | 51.7 | 18.1 | **WAIT FOR BREAK** | 188.328 | 189.135 | +80.7 pips | 20/11 17:00–18:00 | — | — | — | **—** | **46.6/100** |
| 17 | **NZDCAD** | SHORT | **WATCH** | ALIGNED | 3/3 | BULL | BEAR | 14.7 | 20.3 | **WAIT FOR BREAK** | 0.78448 | 0.78609 | +16.1 pips | 20/11 17:00–18:00 | — | — | — | **—** | **45.4/100** |
| 18 | **EURNZD** | LONG | **WATCH** | ALIGNED | 3/3 | BEAR | BULL | 16.2 | 17.6 | **WAIT FOR BREAK** | 2.00301 | 2.00054 | -24.7 pips | 20/11 17:00–18:00 | — | — | — | **—** | **45.0/100** |
| 19 | **USDCAD** | LONG | **WATCH** | ALIGNED | 3/3 | BULL | BEAR | 33.0 | 14.0 | **WAIT FOR BREAK** | 1.43513 | 1.43223 | -29.0 pips | 20/11 17:00–18:00 | — | — | — | **—** | **44.3/100** |
| 20 | **EURUSD** | SHORT | **WATCH** | MIXED | 2/3 | BEAR | MIXED | 33.4 | 17.1 | **WAIT FOR BREAK** | 1.09577 | 1.09842 | +26.5 pips | 20/11 17:00–18:00 | — | — | — | **—** | **36.9/100** |
| 21 | **EURCAD** | SHORT | **WATCH** | MIXED | 2/3 | BULL | BEAR | 28.0 | 13.5 | **WAIT FOR BREAK** | 1.56996 | 1.57287 | +29.1 pips | 20/11 17:00–18:00 | — | — | — | **—** | **31.0/100** |
| 22 | **USDCHF** | LONG | **WATCH** | MIXED | 2/3 | BEAR | BEAR | 25.8 | 28.5 | **WAIT FOR BREAK** | 0.84440 | 0.83930 | -51.0 pips | 20/11 17:00–18:00 | — | — | — | **—** | **24.6/100** |

### Rating detail

| Pair | W1 | D1 | H4 | H1 | Direction |
|---|---|---|---|---|---|
| AUDCAD | SELL | STRONG SELL | STRONG SELL | STRONG SELL | SHORT |
| AUDUSD | STRONG SELL | STRONG SELL | SELL | STRONG SELL | SHORT |
| EURAUD | BUY | STRONG BUY | STRONG BUY | STRONG BUY | LONG |
| GBPAUD | STRONG BUY | STRONG BUY | STRONG BUY | STRONG BUY | LONG |
| EURCHF | SELL | SELL | STRONG SELL | STRONG SELL | SHORT |
| AUDCHF | SELL | STRONG SELL | STRONG SELL | STRONG SELL | SHORT |
| AUDJPY | SELL | STRONG SELL | SELL | STRONG SELL | SHORT |
| AUDNZD | SELL | STRONG SELL | SELL | SELL | SHORT |
| CADJPY | SELL | STRONG SELL | SELL | STRONG SELL | SHORT |
| EURJPY | SELL | STRONG SELL | SELL | STRONG SELL | SHORT |
| GBPJPY | SELL | STRONG SELL | SELL | STRONG SELL | SHORT |
| GBPUSD | STRONG SELL | SELL | SELL | SELL | SHORT |
| NZDCHF | STRONG SELL | STRONG SELL | STRONG SELL | STRONG SELL | SHORT |
| NZDJPY | STRONG SELL | STRONG SELL | STRONG SELL | STRONG SELL | SHORT |
| NZDUSD | SELL | SELL | STRONG SELL | STRONG SELL | SHORT |
| CHFJPY | SELL | SELL | SELL | SELL | SHORT |
| NZDCAD | SELL | SELL | STRONG SELL | STRONG SELL | SHORT |
| EURNZD | STRONG BUY | STRONG BUY | STRONG BUY | STRONG BUY | LONG |
| USDCAD | STRONG BUY | BUY | BUY | BUY | LONG |
| EURUSD | STRONG SELL | SELL | SELL | BUY | SHORT |
| EURCAD | SELL | SELL | NEUTRAL | BUY | SHORT |
| USDCHF | BUY | BUY | NEUTRAL | SELL | LONG |

## Crypto Watch — BTC / ETH / SOL

> Crypto δεδομένα από TradingView Crypto Screener. Το W1 είναι context· η κατεύθυνση εξακολουθεί να απαιτεί D1/H4/H1 alignment.

| Asset | Market | Price | W1 | D1 | H4 | H1 | Direction | W1 Context |
|---|---|---:|---|---|---|---|---|---|
| **BTC** | COINBASE:BTCUSD | 59,182.23 | STRONG SELL | STRONG SELL | STRONG SELL | STRONG SELL | **SHORT** | ✅ SUPPORTS |
| **ETH** | COINBASE:ETHUSD | 1,642.37 | STRONG SELL | STRONG SELL | STRONG SELL | STRONG SELL | **SHORT** | ✅ SUPPORTS |
| **SOL** | COINBASE:SOLUSD | 68.7700 | STRONG SELL | STRONG SELL | SELL | SELL | **SHORT** | ✅ SUPPORTS |

## HTF Reversal — ξεχωριστό mode

> Δεν αναμειγνύεται με το A+ Trend. Απαιτεί επιβεβαιωμένο D1 pivot με τουλάχιστον 2 ανεξάρτητες επαφές, H4 δομή προς την αναστροφή και H1 BRC. Όταν η H4 δομή είναι αντίθετη, μένει WATCH με score έως 65. Πριν από το break, ARMED απαιτεί απόσταση έως 1.5× H1 ATR. Το shortlist κρατά score ≥ 75. READY απαιτεί RR ≥ 3.0.
> **Το HTF Reversal Score μετρά συμφωνία context (/100), όχι πιθανότητα κέρδους. ΑΝΑΜΟΝΗ H1 ΕΠΙΒΕΒΑΙΩΣΗΣ / WAIT RETEST / ARMED δεν είναι είσοδος. Entry/SL/TP εμφανίζονται μόνο σε READY, με RR ≥ 3.0.**

| # | Pair | Dir | State | D1 Zone | H4 Struct | Sweep | Reject | Displ. | H1 BRC | H1 Zone | Τιμή | Δ H1 zone | Κλεισμένο H1 (ώρα Αθήνας) | Entry | SL | TP | RR | Context score /100 | Σημείωση |
|---:|---|---|---|---:|---|---:|---:|---:|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|
| 1 | **CADCHF** | SHORT | **WAIT RETEST** | 0.58800 | BEAR | ✅ | ✅ | — | BREAK | 0.58631 | 0.58598 | -3.3 pips | 20/11 17:00–18:00 | — | — | — | — | **83.0/100** | H1 break — περιμένει retest |
| 2 | **EURNZD** | LONG | **ARMED · ΑΝΑΜΟΝΗ BREAK** | 1.98692 | BULL | ✅ | ✅ | ✅ | WAIT FOR BREAK | 2.00301 | 2.00054 | -24.7 pips | 20/11 17:00–18:00 | — | — | — | — | **89.8/100** | HTF αντίδραση — H1 break κοντά (0.9 ATR) |
| 3 | **EURGBP** | LONG | **ARMED · ΑΝΑΜΟΝΗ BREAK** | 0.83215 | BULL | ✅ | ✅ | ✅ | WAIT FOR BREAK | 0.83850 | 0.83823 | -2.7 pips | 20/11 17:00–18:00 | — | — | — | — | **89.5/100** | HTF αντίδραση — H1 break κοντά (0.4 ATR) |

_Εκτός shortlist: WATCH 7 | INVALID 10. Δεν θεωρούνται ενεργά candidates._

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
| AUDCAD | SELL | STRONG SELL | STRONG SELL | STRONG SELL | SHORT | 3/3 | BEAR | BEAR | BREAK | — | 65.0 |
| AUDCHF | SELL | STRONG SELL | STRONG SELL | STRONG SELL | SHORT | 3/3 | BEAR | BEAR | WAIT NEW RETEST | — | 55.0 |
| AUDJPY | SELL | STRONG SELL | SELL | STRONG SELL | SHORT | 3/3 | BEAR | BEAR | WAIT NEW RETEST | — | 55.0 |
| AUDNZD | SELL | STRONG SELL | SELL | SELL | SHORT | 3/3 | BEAR | BEAR | WAIT FOR BREAK | — | 55.0 |
| AUDUSD | STRONG SELL | STRONG SELL | SELL | STRONG SELL | SHORT | 3/3 | BEAR | BEAR | BREAK | — | 65.0 |
| CADCHF | BUY | SELL | SELL | SELL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| CADJPY | SELL | STRONG SELL | SELL | STRONG SELL | SHORT | 3/3 | BEAR | BEAR | WAIT NEW RETEST | — | 55.0 |
| CHFJPY | SELL | SELL | SELL | SELL | SHORT | 3/3 | BULL | BEAR | WAIT FOR BREAK | — | 46.6 |
| EURAUD | BUY | STRONG BUY | STRONG BUY | STRONG BUY | LONG | 3/3 | BULL | BULL | BREAK | — | 65.0 |
| EURCAD | SELL | SELL | NEUTRAL | BUY | SHORT | 2/3 | BULL | BEAR | WAIT FOR BREAK | — | 31.0 |
| EURCHF | SELL | SELL | STRONG SELL | STRONG SELL | SHORT | 3/3 | BULL | BEAR | BREAK | — | 55.2 |
| EURGBP | SELL | NEUTRAL | BUY | BUY | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| EURJPY | SELL | STRONG SELL | SELL | STRONG SELL | SHORT | 3/3 | BEAR | BEAR | WAIT NEW RETEST | — | 55.0 |
| EURNZD | STRONG BUY | STRONG BUY | STRONG BUY | STRONG BUY | LONG | 3/3 | BEAR | BULL | WAIT FOR BREAK | — | 45.0 |
| EURUSD | STRONG SELL | SELL | SELL | BUY | SHORT | 2/3 | BEAR | MIXED | WAIT FOR BREAK | — | 36.9 |
| GBPAUD | STRONG BUY | STRONG BUY | STRONG BUY | STRONG BUY | LONG | 3/3 | BULL | BULL | BREAK | — | 65.0 |
| GBPCAD | NEUTRAL | SELL | STRONG SELL | STRONG SELL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| GBPCHF | NEUTRAL | SELL | STRONG SELL | STRONG SELL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| GBPJPY | SELL | STRONG SELL | SELL | STRONG SELL | SHORT | 3/3 | BEAR | BEAR | WAIT NEW RETEST | — | 55.0 |
| GBPNZD | BUY | BUY | NEUTRAL | BUY | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| GBPUSD | STRONG SELL | SELL | SELL | SELL | SHORT | 3/3 | BEAR | BEAR | WAIT FOR BREAK | — | 55.0 |
| NZDCAD | SELL | SELL | STRONG SELL | STRONG SELL | SHORT | 3/3 | BULL | BEAR | WAIT FOR BREAK | — | 45.4 |
| NZDCHF | STRONG SELL | STRONG SELL | STRONG SELL | STRONG SELL | SHORT | 3/3 | BULL | BEAR | WAIT FOR BREAK | — | 55.0 |
| NZDJPY | STRONG SELL | STRONG SELL | STRONG SELL | STRONG SELL | SHORT | 3/3 | BEAR | BEAR | WAIT FOR BREAK | — | 55.0 |
| NZDUSD | SELL | SELL | STRONG SELL | STRONG SELL | SHORT | 3/3 | BEAR | BEAR | WAIT FOR BREAK | — | 55.0 |
| USDCAD | STRONG BUY | BUY | BUY | BUY | LONG | 3/3 | BULL | BEAR | WAIT FOR BREAK | — | 44.3 |
| USDCHF | BUY | BUY | NEUTRAL | SELL | LONG | 2/3 | BEAR | BEAR | WAIT FOR BREAK | — | 24.6 |
| USDJPY | BUY | NEUTRAL | NEUTRAL | STRONG SELL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |

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
