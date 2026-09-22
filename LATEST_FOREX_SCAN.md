# Latest Forex Scan

**Τελευταία ενημέρωση:** 23/09/2026 00:59 (Europe/Athens)

**Pairs:** 28  |  **Aligned:** 9  |  **A+ READY:** 0

**HTF Reversal mode:** ON  |  **Candidates:** 1  |  **READY:** 0

> Το Quality Score είναι βαθμός συμφωνίας φίλτρων, **όχι πιθανότητα κέρδους**.

> Ratings / EMA50 / ADX: TradingView Screener. Structure / BRC: Yahoo Finance H1 candles (H4/D1 derived). Μπορεί να υπάρχουν μικρές διαφορές candle boundaries από TradingView.

> **A+ READY** απαιτεί: D1/H4/H1 alignment + EMA50 3/3 + D1/H4 structure + ADX + **confirmation στο τελευταίο κλεισμένο H1**, χωρίς υπερβολική απόσταση από τη zone + **RR ≥ 1.2**.

## Top candidates

| # | Pair | Dir | Setup | Bias | EMA50 | D1 Struct | H4 Struct | ADX H4 | ADX H1 | B→R→C | H1 Zone | Entry | SL | TP | RR | Quality |
|---:|---|---|---|---|---:|---|---|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | **USDCAD** | LONG | **WATCH** | ALIGNED | 3/3 | BULL | BULL | 50.7 | 41.3 | **WAIT NEW RETEST** | 1.40144 | — | — | — | **—** | **62.8/100** |
| 2 | **GBPUSD** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 36.9 | 28.4 | **WAIT NEW RETEST** | 1.33365 | — | — | — | **—** | **62.7/100** |
| 3 | **EURUSD** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 33.7 | 29.7 | **WAIT NEW RETEST** | 1.14587 | — | — | — | **—** | **61.4/100** |
| 4 | **EURCAD** | LONG | **WATCH** | ALIGNED | 3/3 | BULL | BULL | 12.7 | 14.2 | **WAIT NEW RETEST** | 1.60990 | — | — | — | **—** | **48.5/100** |
| 5 | **CADJPY** | SHORT | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 12.8 | 17.8 | **WAIT FOR BREAK** | 111.043 | — | — | — | **—** | **48.4/100** |
| 6 | **GBPAUD** | SHORT | **WATCH** | ALIGNED | 3/3 | BULL | BEAR | 13.1 | 17.5 | **WAIT NEW RETEST** | 1.87538 | — | — | — | **—** | **42.2/100** |
| 7 | **EURAUD** | SHORT | **WATCH** | ALIGNED | 3/3 | BULL | MIXED | 14.9 | 19.4 | **BREAK** | 1.60864 | — | — | — | **—** | **40.1/100** |
| 8 | **AUDCAD** | LONG | **WATCH** | ALIGNED | 3/3 | BEAR | BEAR | 15.8 | 21.3 | **WAIT NEW RETEST** | 0.99977 | — | — | — | **—** | **32.1/100** |
| 9 | **GBPJPY** | SHORT | **WATCH** | ALIGNED | 2/3 | BULL | MIXED | 18.1 | 25.5 | **WAIT FOR BREAK** | 207.867 | — | — | — | **—** | **23.7/100** |

### Rating detail

| Pair | D1 | H4 | H1 | Direction |
|---|---|---|---|---|
| USDCAD | BUY | BUY | BUY | LONG |
| GBPUSD | SELL | SELL | SELL | SHORT |
| EURUSD | SELL | SELL | SELL | SHORT |
| EURCAD | BUY | BUY | BUY | LONG |
| CADJPY | SELL | SELL | SELL | SHORT |
| GBPAUD | STRONG SELL | SELL | SELL | SHORT |
| EURAUD | STRONG SELL | STRONG SELL | SELL | SHORT |
| AUDCAD | BUY | BUY | BUY | LONG |
| GBPJPY | SELL | SELL | SELL | SHORT |

## HTF Reversal — ξεχωριστό mode

> Δεν αναμειγνύεται με το A+ Trend. Ψάχνει D1 support/resistance → H4 sweep/rejection/displacement → H1 break/retest/confirmation. Πριν από το break, ένα setup γίνεται **ARMED** μόνο όταν το H1 break απέχει έως **1.5× H1 ATR**. Το shortlist κρατά μόνο ενεργά contexts με **score ≥ 75**. Το **READY** απαιτεί φυσικό D1 target με **RR ≥ 3.0**.

| # | Pair | Dir | State | D1 Zone | H4 Struct | Sweep | Reject | Displ. | H1 BRC | H1 Zone | Entry | SL | TP | RR | Score | Σημείωση |
|---:|---|---|---|---:|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | **GBPNZD** | SHORT | **ARMED** | 2.35363 | BEAR | ✅ | ✅ | ✅ | WAIT FOR BREAK | 2.32582 | — | — | — | — | **82.8/100** | HTF αντίδραση — H1 break κοντά (0.5 ATR) |

_Εκτός shortlist: WATCH 15 | INVALID 11. Δεν θεωρούνται ενεργά candidates._

### Καταστάσεις HTF Reversal

- **WATCH:** η τιμή αντέδρασε σε επιβεβαιωμένη D1 zone, αλλά δεν υπάρχει ακόμη αρκετή H4 επιβεβαίωση.
- **ARMED:** H1 retest ή ισχυρό HTF context με το απαιτούμενο H1 break έως 1.5× H1 ATR μακριά· μπαίνει στο shortlist μόνο με score ≥ 75.
- **WAIT RETEST:** έγινε H1 break και περιμένει επιστροφή στη broken zone.
- **READY:** fresh confirmation στο τελευταίο κλεισμένο H1 και RR ≥ 3.0 προς την επόμενη D1 zone.
- **INVALID:** παραβίαση D1 zone, ληγμένο H1 setup, υπερβολική απομάκρυνση ή RR < 3.0.
- Απενεργοποίηση χωρίς αφαίρεση κώδικα: `ENABLE_HTF_REVERSAL=false python forex_scanner.py`.

## Όλα τα 28 pairs

| Pair | D1 | H4 | H1 | Dir | EMA | D1 Struct | H4 Struct | BRC | RR | Quality |
|---|---|---|---|---|---:|---|---|---|---:|---:|
| AUDCAD | BUY | BUY | BUY | LONG | 3/3 | BEAR | BEAR | WAIT NEW RETEST | — | 32.1 |
| AUDCHF | BUY | SELL | NEUTRAL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| AUDJPY | NEUTRAL | BUY | BUY | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| AUDNZD | BUY | NEUTRAL | SELL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| AUDUSD | NEUTRAL | SELL | BUY | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| CADCHF | NEUTRAL | SELL | SELL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| CADJPY | SELL | SELL | SELL | SHORT | 3/3 | BEAR | BEAR | WAIT FOR BREAK | — | 48.4 |
| CHFJPY | SELL | BUY | BUY | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| EURAUD | STRONG SELL | STRONG SELL | SELL | SHORT | 3/3 | BULL | MIXED | BREAK | — | 40.1 |
| EURCAD | BUY | BUY | BUY | LONG | 3/3 | BULL | BULL | WAIT NEW RETEST | — | 48.5 |
| EURCHF | NEUTRAL | SELL | SELL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| EURGBP | NEUTRAL | BUY | BUY | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| EURJPY | SELL | SELL | NEUTRAL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| EURNZD | BUY | SELL | SELL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| EURUSD | SELL | SELL | SELL | SHORT | 3/3 | BEAR | BEAR | WAIT NEW RETEST | — | 61.4 |
| GBPAUD | STRONG SELL | SELL | SELL | SHORT | 3/3 | BULL | BEAR | WAIT NEW RETEST | — | 42.2 |
| GBPCAD | BUY | BUY | NEUTRAL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| GBPCHF | NEUTRAL | SELL | SELL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| GBPJPY | SELL | SELL | SELL | SHORT | 2/3 | BULL | MIXED | WAIT FOR BREAK | — | 23.7 |
| GBPNZD | BUY | SELL | STRONG SELL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| GBPUSD | SELL | SELL | SELL | SHORT | 3/3 | BEAR | BEAR | WAIT NEW RETEST | — | 62.7 |
| NZDCAD | SELL | NEUTRAL | BUY | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| NZDCHF | NEUTRAL | SELL | NEUTRAL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| NZDJPY | SELL | BUY | BUY | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| NZDUSD | SELL | NEUTRAL | BUY | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| USDCAD | BUY | BUY | BUY | LONG | 3/3 | BULL | BULL | WAIT NEW RETEST | — | 62.8 |
| USDCHF | BUY | SELL | SELL | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |
| USDJPY | NEUTRAL | BUY | BUY | — | 0/3 | N/A | N/A | WAIT | — | 0.0 |

## Πώς διαβάζεται

- **Bias STRONG/ALIGNED:** συμφωνία Technical Rating σε D1/H4/H1.
- **EMA50 3/3:** τιμή και κλίση EMA50 συμφωνούν με την κατεύθυνση και στα 3 TF.
- **D1/H4 Struct:** BULL ή BEAR από ολοκληρωμένα swing highs/lows.
- **ADX:** πάνω από ~20 δείχνει ισχυρότερη τάση· δεν είναι μόνο του σήμα εισόδου.
- **BRC WAIT FOR BREAK/BREAK/RETEST/READY:** το break γίνεται μόνο σε **επιβεβαιωμένο H1 swing resistance/support (15 κεριά αριστερά + 15 δεξιά)**, όχι σε μικρό 3-candle high/low. Μετά το break, η broken zone μένει ενεργή για έως **8 επόμενα κλεισμένα H1 κεριά** ώστε να προλάβει retest. **WAIT NEW RETEST** σημαίνει ότι το παλιό setup έχει λήξει ή η τιμή απομακρύνθηκε από τη zone.
- **Entry/SL/TP:** εμφανίζονται μόνο όταν το BRC είναι READY. Entry = τελευταίο κλεισμένο H1, SL = H1 zone ± 0.35×ATR, TP = κοντινότερο ολοκληρωμένο H4 swing target.
- **RR:** ✅ όταν RR ≥ 1.2, ❌ όταν είναι χαμηλότερο. Το A+ READY απαιτεί RR pass.
- **A+ READY:** το αυστηρότερο φίλτρο. Πριν από trade χρειάζεται τελικός οπτικός έλεγχος chart, spread/news και sizing.
