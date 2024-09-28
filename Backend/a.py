import requests
from datetime import datetime, timedelta

# Replace 'YOUR_API_KEY' with your actual ExchangeRate-API key
API_KEY = '7753d6f27210c76adbea9654'

# Function to get the current exchange rate
def get_current_rate(from_currency, to_currency):
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        # Check if the request was successful
        if data['result'] == 'success':
            return data['conversion_rates'][to_currency]
        else:
            print(f"Error: Unable to retrieve rates. Response: {data}")
            return None
    except Exception as e:
        print(f"Error fetching current exchange rate: {e}")
        return None

# Function to get the historical exchange rate for a specific date
def get_historical_rate(from_currency, to_currency, year, month, day):
    # Use the correct endpoint for historical data
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/history/{from_currency}/{year}/{month}/{day}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        # Check if the request was successful
        if data['result'] == 'success':
            return data['conversion_rates'][to_currency]
        else:
            print(f"Error: Unable to retrieve historical rates. Response: {data}")
            return None
    except Exception as e:
        print(f"Error fetching historical exchange rate: {e}")
        return None

# Function to validate if a currency code is valid using the ExchangeRate-API
def is_valid_currency(currency_code):
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/codes'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['result'] == 'success':
            valid_codes = [code[0] for code in data['supported_codes']]
            return currency_code in valid_codes
        else:
            print(f"Error: Unable to fetch supported currency codes. Response: {data}")
            return False
    except Exception as e:
        print(f"Error fetching supported currency codes: {e}")
        return False

def main():
    # Get and validate the base currency code
    while True:
        from_currency = input("Enter the base currency code (e.g., USD): ").upper()
        if is_valid_currency(from_currency):
            break
        else:
            print(f"'{from_currency}' is not a valid currency code. Please try again.")

    # Get and validate the target currency code
    while True:
        to_currency = input("Enter the target currency code (e.g., EUR): ").upper()
        if from_currency == to_currency:
            print("The target currency cannot be the same as the base currency. Please enter a different target currency.")
        elif is_valid_currency(to_currency):
            break
        else:
            print(f"'{to_currency}' is not a valid currency code. Please try again.")

    # Get today's date and the date one month ago in the required format
    today = datetime.today().strftime('%Y-%m-%d')
    one_month_ago = datetime.today() - timedelta(days=30)
    one_month_ago_year = one_month_ago.year
    one_month_ago_month = one_month_ago.month
    one_month_ago_day = one_month_ago.day

    # Fetch current and historical exchange rates
    print(f"Fetching current exchange rate for {from_currency} to {to_currency}...")
    current_rate = get_current_rate(from_currency, to_currency)

    print(f"Fetching exchange rate from one month ago ({one_month_ago_year}-{one_month_ago_month:02d}-{one_month_ago_day:02d}) for {from_currency} to {to_currency}...")
    old_rate = get_historical_rate(from_currency, to_currency, one_month_ago_year, one_month_ago_month, one_month_ago_day)

    # Display the results
    if current_rate and old_rate:
        print(f"\nCurrent {from_currency} to {to_currency} exchange rate: {current_rate}")
        print(f"{from_currency} to {to_currency} exchange rate one month ago: {old_rate}")
        change = ((current_rate - old_rate) / old_rate) * 100
        print(f"Change over the past month: {change:.2f}%")

        # Print interpretation of the fluctuation
        if change >= 10:
            print("This month the currency exchange has fluctuated a lot.")
        elif 5 < change < 10:
            print("This month the currency exchange has fluctuated moderately.")
        elif 0 <= change <= 5:
            print("This month the currency exchange has fluctuated a little.")
        elif change < 0:
            print("This month the base currency has gained value compared to the target currency.")
    else:
        print("Failed to retrieve one or both exchange rates. Please check your inputs and API key.")

if __name__ == "__main__":
    main()
