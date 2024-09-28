from alpha_vantage.foreignexchange import ForeignExchange
from datetime import datetime, timedelta
import requests

# Define your Alpha Vantage API key
API_KEY = 'HCC9Q7ACE7YQQYIX'

print("Hello world")

# Function to get the current exchange rate
def get_current_rate(from_currency, to_currency):
    fx = ForeignExchange(key=API_KEY)
    try:
        # Get real-time exchange rate data
        data, _ = fx.get_currency_exchange_rate(from_currency, to_currency)
        return float(data['5. Exchange Rate'])  # Extract and return the exchange rate
    except Exception as e:
        return None

# Function to get the historical exchange rate for a specific date
def get_historical_rate(from_currency, to_currency, date):
    fx = ForeignExchange(key=API_KEY)
    url = f'https://www.alphavantage.co/query'
    params = {
        'function': 'FX_DAILY',
        'from_symbol': from_currency,
        'to_symbol': to_currency,
        'apikey': API_KEY
    }
    try:
        # Fetch the daily historical data
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Access the "Time Series FX (Daily)" field in the returned JSON
        time_series = data.get('Time Series FX (Daily)', {})
        if date in time_series:
            return float(time_series[date]['4. close'])  # Extract the closing rate for the date
        else:
            return None
    except Exception as e:
        return None

def main():
    while True:
        # Validate and get the base currency code
        while True:
            from_currency = input("Enter the base currency code (e.g., USD): ").upper()
            if get_current_rate(from_currency, 'USD') is not None:
                break
            else:
                print("Invalid base currency code. Please try again.\n")

        # Validate and get the target currency code
        while True:
            to_currency = input("Enter the target currency code (e.g., EUR): ").upper()
            if from_currency == to_currency:
                print("Same currency input. Please enter a different target currency.\n")
            elif get_current_rate(from_currency, to_currency) is not None:
                break
            else:
                print("Invalid target currency code. Please try again.\n")

        # Get today's date and the date one month ago in the required format
        today = datetime.today().strftime('%Y-%m-%d')
        one_month_ago = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')

        # Fetch current and historical exchange rates
        print(f"Fetching current exchange rate for {from_currency} to {to_currency}...")
        current_rate = get_current_rate(from_currency, to_currency)

        print(f"Fetching exchange rate from one month ago ({one_month_ago}) for {from_currency} to {to_currency}...")
        old_rate = get_historical_rate(from_currency, to_currency, one_month_ago)

        # Display the results
        if current_rate and old_rate:
            print(f"\nCurrent {from_currency} to {to_currency} exchange rate: {current_rate}")
            print(f"{from_currency} to {to_currency} exchange rate one month ago: {old_rate}")
            change = ((current_rate - old_rate) / old_rate) * 100
            print(f"Change over the past month: {change:.2f}%")
            break
        else:
            print("Failed to retrieve one or both exchange rates. Please check your API key or try again later.")

if __name__ == "__main__":
    main()
