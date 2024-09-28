import requests
from collections.abc import MutableMapping


# Replace 'YOUR_API_KEY' with your actual Fixer.io API key
API_KEY = 'de6138de3e1957aca54ee97795e85e96'

# Endpoint to get all supported symbols (currencies)
url = f"http://data.fixer.io/api/symbols?access_key={API_KEY}"

try:
    # Make a GET request to the Fixer.io API
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for any HTTP errors

    # Parse the JSON response
    data = response.json()

    # Check if the request was successful
    if data.get("success"):
        symbols = data.get("symbols")
        print("Supported Currencies:")
        for currency, description in symbols.items():
            print(f"{currency}: {description}")
    else:
        print("Error:", data.get("error", "Unknown error occurred"))

except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")
except requests.exceptions.JSONDecodeError:
    print("JSON Decode Error: Unable to parse the response as JSON.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
