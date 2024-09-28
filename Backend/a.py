import requests
from datetime import datetime, timedelta

# Replace 'YOUR_API_KEY' with your actual ExchangeRate-API key
API_KEY = '7753d6f27210c76adbea9654'  # Insert your API key here

# Function to get the current exchange rate
def get_current_rate(from_currency, to_currency):
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if data['result'] == 'success':
            return round(data['conversion_rates'].get(to_currency, 0), 3)
        else:
            print(f"Error: Unable to retrieve rates. Response: {data}")
            return None
    except Exception as e:
        print(f"Error fetching current exchange rate: {e}")
        return None

# Function to get historical exchange rates for a specific date
def get_historical_rate(from_currency, to_currency, year, month, day):
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/history/{from_currency}/{year}/{month:02d}/{day:02d}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['result'] == 'success':
            return round(data['conversion_rates'].get(to_currency, 0), 3)
        else:
            print(f"Error: Unable to retrieve historical rate. Response: {data}")
            return None
    except Exception as e:
        print(f"Error fetching historical exchange rate for {year}-{month:02d}-{day:02d}: {e}")
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

# Function to compare current exchange rate with the rate one month ago
def compare_current_and_month_ago_rate(from_currency, to_currency):
    """
    Compares the current exchange rate of a currency pair with the exchange rate from one month ago.
    The function will fetch both current and historical rates, calculate the percentage change,
    and display an alert if the currency fluctuated significantly.

    Args:
    - from_currency (str): The base currency code (e.g., 'USD').
    - to_currency (str): The target currency code (e.g., 'EUR').

    Returns:
    - None
    """
    while True:
        # Get today's date and the date one month ago
        today = datetime.today().strftime('%Y-%m-%d')
        one_month_ago_date = datetime.today() - timedelta(days=30)
        year, month, day = one_month_ago_date.year, one_month_ago_date.month, one_month_ago_date.day
        one_month_ago = one_month_ago_date.strftime('%Y-%m-%d')

        # Fetch current exchange rate
        print(f"Fetching current exchange rate for {from_currency} to {to_currency}...")
        current_rate = get_current_rate(from_currency, to_currency)
        
        # Fetch historical exchange rate from one month ago
        print(f"Fetching exchange rate from one month ago ({one_month_ago}) for {from_currency} to {to_currency}...")
        url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/history/{from_currency}/{year}/{month:02d}/{day:02d}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            historical_data = response.json()
            
            # Check if historical data is valid and extract the rate
            if historical_data['result'] == 'success':
                old_rate = round(historical_data['conversion_rates'].get(to_currency, 0), 3)
            else:
                print(f"Error: Unable to retrieve historical rate. Response: {historical_data}")
                old_rate = None
        except Exception as e:
            print(f"Error fetching historical exchange rate for {one_month_ago}: {e}")
            old_rate = None

        # Display comparison results if both current and historical rates are available
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
            print("Failed to retrieve one or both exchange rates. Please check your inputs.")

        # Ask if the user wants to use this function again
        repeat = input("Would you like to compare the exchange rate for another currency pair? (yes/no): ").lower()
        if repeat != 'yes':
            break

# Function to monitor a currency based on conditions set by the user
def monitor_currencies_with_conditions(from_currency, to_currency):
    """
    Monitors a currency pair based on the user's choice of using the current exchange rate or a custom value.
    Alerts the user if the currency value changes by more than 5% from the monitored value.
    
    Args:
    - from_currency (str): The base currency code (e.g., 'USD').
    - to_currency (str): The target currency code (e.g., 'EUR').

    Returns:
    - None
    """
    while True:
        # Fetch the current rate for the currency pair
        current_rate = get_current_rate(from_currency, to_currency)
        if current_rate:
            print(f"\nThe current exchange rate for {from_currency} to {to_currency} is {current_rate}")
            
            # Ask the user whether to use the current rate or a custom value
            use_current_rate = input("Would you like to use this current rate for monitoring? (yes/no): ").lower()
            if use_current_rate == 'yes':
                monitor_value = current_rate
            else:
                try:
                    # Allow the user to enter a custom value for monitoring
                    monitor_value = float(input(f"Enter a custom value for {from_currency} to {to_currency} (e.g., 0.85): "))
                except ValueError:
                    print("Invalid value entered. Using the current rate as the monitoring value.")
                    monitor_value = current_rate

            # Calculate the percentage change from the monitored value to the current rate
            percentage_change = abs((current_rate - monitor_value) / monitor_value) * 100

            # Trigger an alert if the change exceeds or equals 5%
            if percentage_change >= 5:
                direction = "up" if current_rate > monitor_value else "down"
                print(f"Alert: The currency has experienced a significant {direction} change of {percentage_change:.2f}%. Current rate: {current_rate}")
            else:
                print(f"The currency is stable. Current change is within 5% of the monitored value.")
        else:
            print(f"Unable to fetch the current rate for {from_currency} to {to_currency}. Please try again later.")

        # Ask the user if they want to use this function again
        repeat = input("Would you like to set monitoring conditions for another currency pair? (yes/no): ").lower()
        if repeat != 'yes':
            print("Exiting currency monitoring.")
            break


# Function to display historical data for a specified period
def get_historical_rates_for_period(from_currency, to_currency):
    while True:
        try:
            year = int(input("Enter the year (e.g., 2023): "))
            month = int(input("Enter the month (e.g., 9 for September): "))
            if 1 <= month <= 12:
                days_in_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day if month < 12 else 31
                print(f"\nHistorical Exchange Rates for {from_currency} to {to_currency} ({year}-{month:02d}):")
                for day in range(1, days_in_month + 1):
                    rate = get_historical_rate(from_currency, to_currency, year, month, day)
                    if rate:
                        print(f"{year}-{month:02d}-{day:02d}: {rate}")
            else:
                print("Invalid month. Please enter a value between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter numerical values for year and month.")

        # Ask if the user wants to use this function again
        repeat = input("Would you like to get historical rates for another period? (yes/no): ").lower()
        if repeat != 'yes':
            break


def main():
    """
    Main function to present the user with a menu for selecting different operations:
    - See the current rate compared with one month ago.
    - Get historical rates for a specified period.
    - Monitor a currency based on conditions.
    - Exit the program.
    """
    while True:
        print("\nMain Menu")
        print("1. See the current rate compared with one month ago")
        print("2. Get historical rates for a specified period")
        print("3. Monitor a currency based on conditions")
        print("4. Exit")
        choice = input("Please enter the number of your choice: ")

        if choice == '1':
            # Compare current rate with one month ago
            from_currency = input("Enter the base currency code (e.g., USD): ").upper()
            to_currency = input("Enter the target currency code (e.g., EUR): ").upper()
            if is_valid_currency(from_currency) and is_valid_currency(to_currency):
                compare_current_and_month_ago_rate(from_currency, to_currency)
            else:
                print("Invalid currency code entered. Please try again.")

        elif choice == '2':
            # Get historical rates for a specified period
            from_currency = input("Enter the base currency code (e.g., USD): ").upper()
            to_currency = input("Enter the target currency code (e.g., EUR): ").upper()
            if is_valid_currency(from_currency) and is_valid_currency(to_currency):
                get_historical_rates_for_period(from_currency, to_currency)
            else:
                print("Invalid currency code entered. Please try again.")

        elif choice == '3':
            # Monitor a currency based on conditions using the updated function
            from_currency = input("Enter the base currency code (e.g., USD): ").upper()
            to_currency = input("Enter the target currency code (e.g., EUR): ").upper()
            if is_valid_currency(from_currency) and is_valid_currency(to_currency):
                monitor_currencies_with_conditions(from_currency, to_currency)
            else:
                print("Invalid currency code entered. Please try again.")

        elif choice == '4':
            # Exit the program
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
