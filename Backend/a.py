import requests
from datetime import datetime, timedelta

# Replace 'YOUR_API_KEY' with your actual ExchangeRate-API key
API_KEY = '7753d6f27210c76adbea9654'  # Insert your API key here

# Function to get the current exchange rate
def get_current_rate(from_currency, to_currencies):
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        # Check if the request was successful
        if data['result'] == 'success':
            return {currency: round(data['conversion_rates'].get(currency, 0), 3) for currency in to_currencies}
        else:
            print(f"Error: Unable to retrieve rates. Response: {data}")
            return None
    except Exception as e:
        print(f"Error fetching current exchange rate: {e}")
        return None

# Function to get historical rates for a specified month and year
def get_historical_rates(from_currency, to_currencies, year, month):
    days_in_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day if month < 12 else 31
    rates = {currency: [] for currency in to_currencies}
    dates = []

    # Fetch historical data for each day in the specified month and year
    for day in range(1, days_in_month + 1):
        date = f'{year}/{month:02d}/{day:02d}'
        url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/history/{from_currency}/{year}/{month:02d}/{day:02d}'
        try:
            response = requests.get(url)
            if response.status_code == 404:
                print(f"Historical data not available for {date}. Skipping this date.")
                continue  # Skip to the next date if 404 error occurs

            response.raise_for_status()  # Raise an exception for other HTTP errors
            data = response.json()
            if data['result'] == 'success':
                for currency in to_currencies:
                    rate = data['conversion_rates'].get(currency, None)
                    rates[currency].append(round(rate, 3) if rate is not None else None)
                dates.append(f'{year}-{month:02d}-{day:02d}')
            else:
                print(f"Error: Unable to retrieve rates for {date}. Response: {data}")
        except Exception as e:
            print(f"Error fetching historical exchange rate for {date}: {e}")

    return dates, rates

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

# Function to display historical data in the terminal
def display_historical_data(dates, historical_rates, from_currency):
    if not dates:
        print("No historical data available for the specified period.")
        return

    print("\nHistorical Exchange Rates:\n")
    print("Date       ", end="")
    for currency in historical_rates.keys():
        print(f"{from_currency} to {currency:<10}", end="")
    print()
    print("=" * (12 + 15 * len(historical_rates)))

    for i in range(len(dates)):
        print(f"{dates[i]}  ", end="")
        for currency in historical_rates.keys():
            rate = historical_rates[currency][i]
            print(f"{rate:<15}" if rate is not None else f"{'N/A':<15}", end="")
        print()

def main():
    # Get and validate the base currency code
    while True:
        from_currency = input("Enter the base currency code (e.g., USD): ").upper()
        if is_valid_currency(from_currency):
            break
        else:
            print(f"'{from_currency}' is not a valid currency code. Please try again.")

    # Get and validate the target currencies
    to_currencies = []
    print("Enter the target currency codes (e.g., EUR, GBP, JPY). Type 'done' when finished.")
    while True:
        to_currency = input("Enter a target currency code: ").upper()
        if to_currency == 'DONE':
            if to_currencies:
                break
            else:
                print("Please enter at least one target currency.")
        elif to_currency == from_currency:
            print("The target currency cannot be the same as the base currency. Please enter a different target currency.")
        elif is_valid_currency(to_currency):
            to_currencies.append(to_currency)
            print(f"Added {to_currency}. Enter another currency or type 'done' to finish.")
        else:
            print(f"'{to_currency}' is not a valid currency code. Please try again.")

    # Fetch current exchange rates
    print(f"Fetching current exchange rates for {from_currency} to {', '.join(to_currencies)}...")
    current_rates = get_current_rate(from_currency, to_currencies)

    if current_rates:
        print("\nCurrent Exchange Rates:")
        for currency, rate in current_rates.items():
            print(f"{from_currency} to {currency}: {rate:.3f}")

    # Ask user if they want to see historical data and get month and year
    while True:
        show_history = input("Do you want to see historical exchange rates for a specific month and year? (yes/no): ").lower()
        if show_history == 'yes':
            while True:
                try:
                    year = int(input("Enter the year (e.g., 2023): "))
                    month = int(input("Enter the month (e.g., 9 for September): "))
                    if 1 <= month <= 12:
                        break
                    else:
                        print("Invalid month. Please enter a value between 1 and 12.")
                except ValueError:
                    print("Invalid input. Please enter numerical values for year and month.")

            # Fetch and display historical exchange rates for the specified month and year
            print(f"\nFetching historical exchange rates for {from_currency} to {', '.join(to_currencies)} for {year}-{month:02d}...")
            dates, historical_rates = get_historical_rates(from_currency, to_currencies, year, month)
            display_historical_data(dates, historical_rates, from_currency)
            break
        elif show_history == 'no':
            print("Historical data will not be fetched.")
            break
        else:
            print("Invalid input. Please type 'yes' or 'no'.")

if __name__ == "__main__":
    main()