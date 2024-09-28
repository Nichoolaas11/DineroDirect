import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline
import re
import os

# Function to extract text from a PDF
def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""  # Handle None for empty pages
    return text

# Function to use AI to parse transactions
def parse_transactions_with_ai(text):
    # Load pre-trained NLP pipeline for information extraction
    nlp = pipeline("ner", model="dslim/bert-base-NER", tokenizer="dslim/bert-base-NER")

    # Extract entities from text
    entities = nlp(text)
    
    transactions = []
    transaction = {}

    for entity in entities:
        if entity['entity'] == 'DATE':
            transaction['date'] = entity['word']
        elif entity['entity'] == 'MONEY':
            amount = re.sub(r'[^\d\.\-]', '', entity['word'])
            transaction['amount'] = float(amount)
        elif entity['entity'] == 'MISC' and len(transaction) == 2:
            transaction['description'] = entity['word']
            transactions.append(transaction)
            transaction = {}

    return transactions

# Function to categorize a transaction based on the description
def categorize_transaction(description):
    categories = {
        "food": ["RESTAURANT", "GROCERY", "FOOD"],
        "gas": ["GAS", "PETROL"],
        "entertainment": ["MOVIE", "CINEMA", "MUSIC"],
        "travel": ["FLIGHT", "TICKET", "HOTEL", "AIRLINE"],
        "healthcare": ["HOSPITAL", "CLINIC", "PHARMACY", "MEDICAL"],
        "shopping": ["STORE", "SHOPPING", "MALL", "RETAIL"],
        "utilities": ["ELECTRIC", "WATER", "GAS BILL", "UTILITY"],
        "subscriptions": ["SUBSCRIPTION", "MONTHLY"],
        "services": ["SERVICE", "FEE", "MAINTENANCE"],
        "education": ["SCHOOL", "COLLEGE", "BOOK", "COURSE"],
        "gifts": ["GIFT", "DONATION"],
    }
    
    description_upper = description.upper()
    for category, keywords in categories.items():
        if any(keyword in description_upper for keyword in keywords):
            return category
    return "misc"  # Default category

# Function to categorize all transactions
def categorize_transactions(transactions):
    for transaction in transactions:
        transaction["category"] = categorize_transaction(transaction["description"])
    return transactions

# Function to summarize spending by category
def summarize_categories(transactions):
    df = pd.DataFrame(transactions)
    summary = df.groupby('category')['amount'].sum()
    total = summary.sum()
    percentages = (summary / total) * 100
    return percentages

# Function to plot spending summary
def plot_summary(summary):
    summary.plot(kind='pie', autopct='%1.1f%%', startangle=140)
    plt.title('Spending by Category')
    plt.ylabel('')
    plt.show()

# Main function to orchestrate the workflow
def main():
    print("Starting the transaction analysis...")
    
    # Prompt user for the file path
    file_path = input("Enter the full path to the bank statement PDF: ")

    # Validate the path
    if not os.path.exists(file_path):
        print("The specified file path does not exist. Please try again.")
        return
    
    # Extract text from the PDF
    text = extract_text_from_pdf(file_path)
    print("Text extracted from the PDF.")

    # Parse and categorize transactions using AI
    transactions = parse_transactions_with_ai(text)
    print(f"Parsed {len(transactions)} transactions.")
    
    categorized_transactions = categorize_transactions(transactions)
    
    # Summarize spending and display the results
    summary = summarize_categories(categorized_transactions)
    print("\nSummary of spending by category:")
    print(summary)
    
    # Plot the summary
    plot_summary(summary)

# Entry point of the script
if __name__ == "__main__":
    main()
