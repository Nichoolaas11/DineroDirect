import re
import pdfplumber
from collections import defaultdict

def read_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_chase_transactions(file_path):
    text = read_pdf(file_path)

    # Split the text into lines
    lines = text.splitlines()
    payments = []
    purchases = []
    is_payments_section = False
    is_purchases_section = False

    for line in lines:
        line = line.strip()
        
        if line.startswith("PAYMENTS AND OTHER CREDITS"):
            is_payments_section = True
            continue
        elif line.startswith("PURCHASE"):
            is_payments_section = False
            is_purchases_section = True
            continue

        if is_payments_section and line:
            parts = line.split()
            if len(parts) >= 3 and parts[1] == "Payment":
                try:
                    date = parts[0]
                    amount = float(parts[-1])
                    payments.append((date, -amount))  # Store as negative for payments
                except ValueError:
                    continue  # Skip any lines that don't have a valid amount
        elif is_purchases_section and line:
            match = re.match(r'(\d{2}/\d{2})\s+(.*)\s+([0-9]+\.[0-9]{2})', line)
            if match:
                date, description, amount = match.groups()
                amount = float(amount)
                purchases.append((date, description, round(amount)))  # Round purchases

    print(f"Payments found: {payments}")  # Debug print
    print(f"Purchases found: {purchases}")  # Debug print

    # Categorize purchases
    categorized_purchases = categorize_purchases(purchases)
    return payments, categorized_purchases

def categorize_purchases(purchases):
    categories = defaultdict(float)
    for date, description, amount in purchases:
        # Example categorization logic
        if "CHICK-FIL-A" in description:
            categories["Food"] += amount
        elif "WINGS" in description:
            categories["Food"] += amount
        elif "GAS" in description or "EXXON" in description:
            categories["Gas"] += amount
        else:
            categories["Other"] += amount
    return categories

def main():
    file_path = r'C:\Users\nicho\Documents\GitHub\DineroDirect\Backend\statements_pdf\F1FF59F0-0799-4042-A2B5-92C21E8213C6-list.pdf'
    payments, categorized_purchases = extract_chase_transactions(file_path)

    print("\nPayments:")
    for date, amount in payments:
        print(f"{date}: ${abs(amount):.2f}")  # Print payments as positive values

    print("\nCategorized Purchases:")
    for category, total in categorized_purchases.items():
        print(f"{category}: ${total:.2f}")

if __name__ == "__main__":
    main()
