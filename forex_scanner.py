"""
Forex Scanner - πρώτη έκδοση
============================

Στόχος:
1. Ανάγνωση Forex δεδομένων από το tvscreener.
2. Έλεγχος D1 + H4 + H1 στην ίδια κατεύθυνση.
3. Μετά θα προστεθεί Break -> Retest -> Confirmation.
4. Τα καλύτερα setups θα εμφανίζονται στην κορυφή.

Αυτό είναι το πρώτο πραγματικό αρχείο του scanner.
"""

from tvscreener import ForexScreener


def fetch_forex_market():
    """Κατεβάζει ένα πρώτο snapshot της αγοράς Forex."""
    screener = ForexScreener()
    return screener.get()


def main():
    print("=" * 60)
    print("FOREX SCANNER - D1 + H4 + H1")
    print("Πρώτο στάδιο: σύνδεση με τα δεδομένα TradingView Screener")
    print("=" * 60)

    data = fetch_forex_market()

    print(f"Βρέθηκαν {len(data)} Forex εγγραφές.")
    print("\nΠρώτες γραμμές:")
    print(data.head(20).to_string())

    print("\nΕΠΟΜΕΝΟ ΒΗΜΑ:")
    print("- D1 direction")
    print("- H4 confirmation")
    print("- H1 setup")
    print("- Break -> Retest -> Confirmation")
    print("- Ranking των καλύτερων setups")


if __name__ == "__main__":
    main()
