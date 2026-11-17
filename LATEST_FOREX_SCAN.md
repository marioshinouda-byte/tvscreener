# Latest Forex Scan

**Τελευταία ενημέρωση:** 18/11/2026 01:31 (Europe/Athens)

**Pairs:** 28  |  **Aligned:** 25  |  **A+ READY:** 0

**HTF Reversal mode:** ON  |  **Candidates:** 0  |  **READY:** 0

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
| CHFJPY | PRICE-MISMATCH |

Κανένα A+ READY στο τρέχον scan.

> Η ένδειξη απαιτεί έλεγχο στο τρέχον chart, spread, ειδήσεων και μεγέθους θέσης πριν από οποιαδήποτε είσοδο.

## OANDA — αυτόματο πρώτο φίλτρο (έως 5 ζευγάρια)

**5 ζευγάρια προς έλεγχο** — δες το [OANDA_SHORTLIST.md](OANDA_SHORTLIST.md). Μόνο ενδείξεις TradingView OANDA, χωρίς BRC/READY. Το report εμφανίζει H1 OANDA timestamps, αλλά δεν έχει επιβεβαιωμένο πλήρες OHLC ιστορικό.

## Weekly Top 5 — 2026-W47 (Europe/Athens)

Η πεντάδα διατηρείται όλη την εβδομάδα· ανανεώνονται score και κατάσταση σε κάθε scan. Μόνο νέο επιβεβαιωμένο setup με RR ≥ 1.2 μπορεί να αντικαταστήσει θέση. Νέα επιλογή γίνεται τη Δευτέρα (ώρα Ελλάδας).

| # | Pair | Dir | Agreement /100 | Κατάσταση | B→R→C | H1 Zone | Τιμή | Απόσταση zone | Κλεισμένο H1 (ώρα Αθήνας) | RR |
|---:|---|---|---:|---|---|---:|---:|---:|---|---:|
| 1 | **NZDCAD** | SHORT | **48.0/100** | **⚪ WAIT** | WAIT FOR BREAK | 0.78399 | 0.78467 | +6.8 pips | 18/11 00:00–01:00 | — |
| 2 | **AUDJPY** | SHORT | **55.0/100** | **⚪ WAIT** | WAIT FOR BREAK | 106.865 | 107.365 | +50.0 pips | 18/11 00:00–01:00 | — |
| 3 | **GBPJPY** | SHORT | **50.4/100** | **⚪ WAIT** | WAIT FOR BREAK | 209.570 | 210.532 | +96.2 pips | 18/11 00:00–01:00 | — |
| 4 | **AUDCHF** | SHORT | **52.8/100** | **⚪ WAIT** | WAIT FOR BREAK | 0.56309 | 0.56621 | +31.2 pips | 18/11 00:00–01:00 | — |
| 5 | **AUDUSD** | SHORT | **55.0/100** | **⚪ WAIT** | WAIT FOR BREAK | 0.67231 | 0.67376 | +14.5 pips | 18/11 00:00–01:00 | — |

## Νέοι υποψήφιοι για παρακολούθηση — Trend

Νέα ζευγάρια εκτός πεντάδας με agreement score ≥ 70/100 και D1/H4 structure + EMA50 ή setup A/A+. Είναι υποψήφια για παρακολούθηση, όχι σήματα εισόδου· είσοδος εξετάζεται μόνο σε ENTRY READY.

Κανένα νέο ζευγάρι που να περνά τα κριτήρια.

> **Agreement score /100 = βαθμός συμφωνίας φίλτρων, όχι πιθανότητα επιτυχίας.** 🔴 INVALID σημαίνει ότι χάθηκε το alignment ή δεν υπάρχουν αξιόπιστα δεδομένα στο τρέχον scan.

## Όλοι οι τρέχοντες Trend candidates

| # | Pair | Dir | Setup | Bias | EMA50 | D1 Struct | H4 Struct | ADX H4 | ADX H1 | B→R→C | H1 Zone | Τιμή | Δ zone | Κλεισμένο H1 (ώρα Αθήνας) | Entry | SL | TP | RR | Agreement /100 |
|---:|---|---|---|---|---:|---|---|---:|---:|---|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 1 | **AUDJPY** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 49.8 | 45.6 | **WAIT FOR BREAK** | 106.865 | 107.365 | +50.0 pips | 18/11 00:00–01:00 | — | — | — | **—** | **55.0/100** |
| 2 | **AUDUSD** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 58.0 | 28.7 | **WAIT FOR BREAK** | 0.67231 | 0.67376 | +14.5 pips | 18/11 00:00–01:00 | — | — | — | **—** | **55.0/100** |
| 3 | **EURGBP** | SHORT | **WATCH** | ALIGNED | 3/3 | BULL | BEAR | 29.1 | 40.8 | **WAIT NEW RETEST** | 0.83307 | 0.83226 | -8.1 pips | 18/11 00:00–01:00 | — | — | — | **—** | **55.0/100** |
| 4 | **EURUSD** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 42.4 | 22.2 | **WAIT FOR BREAK** | 1.09721 | 1.10023 | +30.2 pips | 18/11 00:00–01:00 | — | — | — | **—** | **55.0/100** |
| 5 | **GBPAUD** | LONG | **WATCH** | ALIGNED | 3/3 | BULL | BULL | 32.0 | 40.5 | **WAIT NEW RETEST** | 1.95685 | 1.96062 | +37.7 pips | 18/11 00:00–01:00 | — | — | — | **—** | **55.0/100** |
| 6 | **GBPNZD** | LONG | **WATCH** | ALIGNED | 3/3 | BULL | BULL | 23.7 | 27.0 | **WAIT FOR BREAK** | 2.40417 | 2.40418 | +0.1 pips | 18/11 00:00–01:00 | — | — | — | **—** | **55.0/100** |
| 7 | **NZDCHF** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 58.6 | 46.2 | **WAIT FOR BREAK** | 0.45906 | 0.46133 | +22.7 pips | 18/11 00:00–01:00 | — | — | — | **—** | **55.0/100** |
| 8 | **NZDJPY** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 54.7 | 56.2 | **WAIT FOR BREAK** | 87.309 | 87.521 | +21.2 pips | 18/11 00:00–01:00 | — | — | — | **—** | **55.0/100** |
| 9 | **NZDUSD** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 38.0 | 28.9 | **WAIT FOR BREAK** | 0.54840 | 0.54918 | +7.8 pips | 18/11 00:00–01:00 | — | — | — | **—** | **55.0/100** |
| 10 | **CADJPY** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 40.3 | 21.1 | **WAIT FOR BREAK** | 111.119 | 111.508 | +38.9 pips | 18/11 00:00–01:00 | — | — | — | **—** | **54.6/100** |
| 11 | **AUDCHF** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 20.4 | 33.7 | **WAIT FOR BREAK** | 0.56309 | 0.56621 | +31.2 pips | 18/11 00:00–01:00 | — | — | — | **—** | **52.8/100** |
| 12 | **EURNZD** | LONG | **WATCH** | ALIGNED | 3/3 | BULL | BULL | 16.9 | 25.4 | **WAIT FOR BREAK** | 2.00597 | 2.00170 | -42.7 pips | 18/11 00:00–01:00 | — | — | — | **—** | **52.4/100** |
| 13 | **USDCAD** | LONG | **WATCH** | ALIGNED | 3/3 | BULL | BEAR | 48.7 | 23.0 | **WAIT FOR BREAK** | 1.43161 | 1.42933 | -22.8 pips | 18/11 00:00–01:00 | — | — | — | **—** | **51.4/100** |
| 14 | **GBPJPY** | SHORT | **WATCH** | MIXED | 2/3 | BEAR | BEAR | 55.0 | 28.7 | **WAIT FOR BREAK** | 209.570 | 210.532 | +96.2 pips | 18/11 00:00–01:00 | — | — | — | **—** | **50.4/100** |
| 15 | **EURJPY** | SHORT | **WATCH** | ALIGNED | 3/3 | MIXED | BEAR | 51.9 | 32.0 | **WAIT FOR BREAK** | 174.759 | 175.330 | +57.1 pips | 18/11 00:00–01:00 | — | — | — | **—** | **50.0/100** |
| 16 | **AUDCAD** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 25.8 | 15.9 | **WAIT FOR BREAK** | 0.96050 | 0.96251 | +20.1 pips | 18/11 00:00–01:00 | — | — | — | **—** | **49.9/100** |
| 17 | **NZDCAD** | SHORT | **WATCH** | ALIGNED | 3/3 | BULL | BEAR | 23.2 | 62.4 | **WAIT FOR BREAK** | 0.78399 | 0.78467 | +6.8 pips | 18/11 00:00–01:00 | — | — | — | **—** | **48.0/100** |
| 18 | **USDCHF** | LONG | **WATCH** | ALIGNED | 3/3 | BEAR | BULL | 28.1 | 14.5 | **WAIT FOR BREAK** | 0.84152 | 0.84084 | -6.8 pips | 18/11 00:00–01:00 | — | — | — | **—** | **46.8/100** |
| 19 | **GBPUSD** | SHORT | **WATCH** | MIXED | 2/3 | BEAR | BEAR | 47.9 | 13.6 | **WAIT FOR BREAK** | 1.31759 | 1.32090 | +33.1 pips | 18/11 00:00–01:00 | — | — | — | **—** | **46.6/100** |
| 20 | **EURCAD** | SHORT | **WATCH** | ALIGNED | 3/3 | BULL | BEAR | 25.1 | 18.7 | **WAIT FOR BREAK** | 1.56870 | 1.57191 | +32.1 pips | 18/11 00:00–01:00 | — | — | — | **—** | **45.2/100** |
| 21 | **GBPCHF** | LONG | **WATCH** | ALIGNED | 3/3 | BULL | BEAR | 13.9 | 16.6 | **WAIT NEW RETEST** | 1.10825 | 1.11039 | +21.4 pips | 18/11 00:00–01:00 | — | — | — | **—** | **41.3/100** |
| 22 | **EURAUD** | LONG | **WATCH** | ALIGNED | 3/3 | BULL | BEAR | 27.6 | 21.1 | **WAIT FOR BREAK** | 1.63596 | 1.63282 | -31.4 pips | 18/11 00:00–01:00 | — | — | — | **—** | **40.7/100** |
| 23 | **USDJPY** | LONG | **WATCH** | MIXED | 2/3 | BULL | BEAR | 18.9 | 20.1 | **WAIT FOR BREAK** | 159.470 | 159.405 | -6.5 pips | 18/11 00:00–01:00 | — | — | — | **—** | **37.1/100** |
| 24 | **AUDNZD** | SHORT | **WATCH** | MIXED | 2/3 | BEAR | BULL | 49.9 | 20.6 | **WAIT FOR BREAK** | 1.22318 | 1.22562 | +24.4 pips | 18/11 00:00–01:00 | — | — | — | **—** | **34.2/100** |
| 25 | **CADCHF** | LONG | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 10.4 | 16.2 | **WAIT NEW RETEST** | 0.58780 | 0.58796 | +1.6 pips | 18/11 00:00–01:00 | — | — | — | **—** | **32.3/100** |

### Rating detail

| Pair | W1 | D1 | H4 | H1 | Direction |
|---|---|---|---|---|---|
| AUDJPY | SELL | SELL | SELL | BUY | SHORT |
| AUDUSD | SELL | SELL | SELL | NEUTRAL | SHORT |
| EURGBP | SELL | SELL | STRONG SELL | STRONG SELL | SHORT |
| EURUSD | STRONG SELL | SELL | SELL | SELL | SHORT |
| GBPAUD | BUY | BUY | STRONG BUY | NEUTRAL | LONG |
| GBPNZD | BUY | STRONG BUY | BUY | BUY | LONG |
| NZDCHF | SELL | SELL | NEUTRAL | STRONG BUY | SHORT |
| NZDJPY | STRONG SELL | SELL | SELL | BUY | SHORT |
| NZDUSD | SELL | SELL | SELL | SELL | SHORT |
| CADJPY | SELL | SELL | SELL | BUY | SHORT |
| AUDCHF | SELL | SELL | SELL | BUY | SHORT |
| EURNZD | STRONG BUY | STRONG BUY | BUY | SELL | LONG |
| USDCAD | BUY | BUY | BUY | BUY | LONG |
| GBPJPY | NEUTRAL | SELL | SELL | BUY | SHORT |
| EURJPY | SELL | SELL | SELL | BUY | SHORT |
| AUDCAD | SELL | SELL | SELL | BUY | SHORT |
| NZDCAD | SELL | SELL | SELL | NEUTRAL | SHORT |
| USDCHF | BUY | STRONG BUY | BUY | BUY | LONG |
| GBPUSD | SELL | SELL | SELL | BUY | SHORT |
| EURCAD | SELL | SELL | SELL | SELL | SHORT |
| GBPCHF | STRONG BUY | BUY | BUY | BUY | LONG |
| EURAUD | NEUTRAL | BUY | BUY | SELL | LONG |
| USDJPY | STRONG BUY | BUY | BUY | BUY | LONG |
| AUDNZD | BUY | NEUTRAL | SELL | BUY | SHORT |
| CADCHF | BUY | BUY | BUY | BUY | LONG |

## Crypto Watch — BTC / ETH / SOL

> Crypto δεδομένα από TradingView Crypto Screener. Το W1 είναι context· η κατεύθυνση εξακολουθεί να απαιτεί D1/H4/H1 alignment.

| Asset | Market | Price | W1 | D1 | H4 | H1 | Direction | W1 Context |
|---|---|---:|---|---|---|---|---|---|
| **BTC** | COINBASE:BTCUSD | 64,902.82 | STRONG SELL | SELL | NEUTRAL | BUY | **—** | NEUTRAL |
| **ETH** | COINBASE:ETHUSD | 1,821.68 | STRONG SELL | SELL | NEUTRAL | BUY | **—** | NEUTRAL |
| **SOL** | COINBASE:SOLUSD | 75.0100 | SELL | SELL | BUY | BUY | **—** | NEUTRAL |

## HTF Reversal — ξεχωριστό mode

> Δεν αναμειγνύεται με το A+ Trend. Απαιτεί επιβεβαιωμένο D1 pivot με τουλάχιστον 2 ανεξάρτητες επαφές, H4 δομή προς την αναστροφή και H1 BRC. Όταν η H4 δομή είναι αντίθετη, μένει WATCH με score έως 65. Πριν από το break, ARMED απαιτεί απόσταση έως 1.5× H1 ATR. Το shortlist κρατά score ≥ 75. READY απαιτεί RR ≥ 3.0.
> **Το HTF Reversal Score μετρά συμφωνία context (/100), όχι πιθανότητα κέρδους. ΑΝΑΜΟΝΗ H1 ΕΠΙΒΕΒΑΙΩΣΗΣ / WAIT RETEST / ARMED δεν είναι είσοδος. Entry/SL/TP εμφανίζονται μόνο σε READY, με RR ≥ 3.0.**

Δεν υπάρχει ενεργό HTF reversal context που να περνά το αυστηρό shortlist.

_Εκτός shortlist: WATCH 14 | INVALID 5. Δεν θεωρούνται ενεργά candidates._

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
| AUDCAD | SELL | SELL | SELL | BUY | SHORT | 3/3 | BEAR | BEAR | WAIT FOR BREAK | — | 49.9 |
| AUDCHF | SELL | SELL | SELL | BUY | SHORT | 3/3 | BEAR | BEAR | WAIT FOR BREAK | — | 52.8 |
| AUDJPY | SELL | SELL | SELL | BUY | SHORT | 3/3 | BEAR | BEAR | WAIT FOR BREAK | — | 55.0 |
| AUDNZD | BUY | NEUTRAL | SELL | BUY | SHORT | 2/3 | BEAR | BULL | WAIT FOR BREAK | — | 34.2 |
| AUDUSD | SELL | SELL | SELL | NEUTRAL | SHORT | 3/3 | BEAR | BEAR | WAIT FOR BREAK | — | 55.0 |
| CADCHF | BUY | BUY | BUY | BUY | LONG | 3/3 | BEAR | BEAR | WAIT NEW RETEST | — | 32.3 |
| CADJPY | SELL | SELL | SELL | BUY | SHORT | 3/3 | BEAR | BEAR | WAIT FOR BREAK | — | 54.6 |
| CHFJPY | SELL | SELL | SELL | SELL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| EURAUD | NEUTRAL | BUY | BUY | SELL | LONG | 3/3 | BULL | BEAR | WAIT FOR BREAK | — | 40.7 |
| EURCAD | SELL | SELL | SELL | SELL | SHORT | 3/3 | BULL | BEAR | WAIT FOR BREAK | — | 45.2 |
| EURCHF | SELL | NEUTRAL | BUY | BUY | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| EURGBP | SELL | SELL | STRONG SELL | STRONG SELL | SHORT | 3/3 | BULL | BEAR | WAIT NEW RETEST | — | 55.0 |
| EURJPY | SELL | SELL | SELL | BUY | SHORT | 3/3 | MIXED | BEAR | WAIT FOR BREAK | — | 50.0 |
| EURNZD | STRONG BUY | STRONG BUY | BUY | SELL | LONG | 3/3 | BULL | BULL | WAIT FOR BREAK | — | 52.4 |
| EURUSD | STRONG SELL | SELL | SELL | SELL | SHORT | 3/3 | BEAR | BEAR | WAIT FOR BREAK | — | 55.0 |
| GBPAUD | BUY | BUY | STRONG BUY | NEUTRAL | LONG | 3/3 | BULL | BULL | WAIT NEW RETEST | — | 55.0 |
| GBPCAD | BUY | BUY | BUY | BUY | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| GBPCHF | STRONG BUY | BUY | BUY | BUY | LONG | 3/3 | BULL | BEAR | WAIT NEW RETEST | — | 41.3 |
| GBPJPY | NEUTRAL | SELL | SELL | BUY | SHORT | 2/3 | BEAR | BEAR | WAIT FOR BREAK | — | 50.4 |
| GBPNZD | BUY | STRONG BUY | BUY | BUY | LONG | 3/3 | BULL | BULL | WAIT FOR BREAK | — | 55.0 |
| GBPUSD | SELL | SELL | SELL | BUY | SHORT | 2/3 | BEAR | BEAR | WAIT FOR BREAK | — | 46.6 |
| NZDCAD | SELL | SELL | SELL | NEUTRAL | SHORT | 3/3 | BULL | BEAR | WAIT FOR BREAK | — | 48.0 |
| NZDCHF | SELL | SELL | NEUTRAL | STRONG BUY | SHORT | 3/3 | BEAR | BEAR | WAIT FOR BREAK | — | 55.0 |
| NZDJPY | STRONG SELL | SELL | SELL | BUY | SHORT | 3/3 | BEAR | BEAR | WAIT FOR BREAK | — | 55.0 |
| NZDUSD | SELL | SELL | SELL | SELL | SHORT | 3/3 | BEAR | BEAR | WAIT FOR BREAK | — | 55.0 |
| USDCAD | BUY | BUY | BUY | BUY | LONG | 3/3 | BULL | BEAR | WAIT FOR BREAK | — | 51.4 |
| USDCHF | BUY | STRONG BUY | BUY | BUY | LONG | 3/3 | BEAR | BULL | WAIT FOR BREAK | — | 46.8 |
| USDJPY | STRONG BUY | BUY | BUY | BUY | LONG | 2/3 | BULL | BEAR | WAIT FOR BREAK | — | 37.1 |

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
