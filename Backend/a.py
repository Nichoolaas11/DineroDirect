from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Enable CORS on the entire Flask app

API_KEY = '7753d6f27210c76adbea9654' 

# Function to get the current exchange rate
def get_current_rate(from_currency, to_currency):
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['result'] == 'success':
            return round(data['conversion_rates'].get(to_currency, 0), 3)
        else:
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
            return None
    except Exception as e:
        print(f"Error fetching historical exchange rate for {year}-{month:02d}-{day:02d}: {e}")
        return None

# Route to handle comparison of current and historical rates
@app.route('/compare', methods=['POST', 'OPTIONS'])
def compare_current_and_month_ago_rate():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight request successful'}), 200

    data = request.json
    from_currency = data.get('from_currency')
    to_currency = data.get('to_currency')

    if not from_currency or not to_currency:
        return jsonify({'error': 'Please provide both from_currency and to_currency'}), 400

    one_month_ago_date = datetime.today() - timedelta(days=30)
    year, month, day = one_month_ago_date.year, one_month_ago_date.month, one_month_ago_date.day

    current_rate = get_current_rate(from_currency, to_currency)
    old_rate = get_historical_rate(from_currency, to_currency, year, month, day)

    if current_rate and old_rate:
        change = current_rate - old_rate  # Calculate the absolute change in the exchange rate
        percentage_change = ((current_rate - old_rate) / old_rate) * 100  # Calculate percentage change
        return jsonify({
            'current_rate': current_rate,
            'old_rate': old_rate,
            'rate_change': round(change, 3),
            'percentage_change': round(percentage_change, 2),
            'message': f"Change over the past month: {percentage_change:.2f}%"
        })
    else:
        return jsonify({'error': 'Failed to retrieve one or both exchange rates'}), 400

# Route to monitor a currency based on conditions set by the user
@app.route('/monitor', methods=['POST', 'OPTIONS'])
def monitor_currencies_with_conditions():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight request successful'}), 200

    data = request.json
    from_currency = data.get('from_currency')
    to_currency = data.get('to_currency')
    monitor_value = data.get('monitor_value', None)  # Optional, default is None

    # Validate input currencies
    if not from_currency or not to_currency:
        return jsonify({'error': 'Please provide both from_currency and to_currency'}), 400

    # Fetch the current rate
    current_rate = get_current_rate(from_currency, to_currency)
    if not current_rate:
        return jsonify({'error': 'Unable to fetch the current rate'}), 400

    # Use the current rate if no custom value is provided
    if not monitor_value:
        monitor_value = current_rate

    # Calculate the percentage change
    percentage_change = abs((current_rate - float(monitor_value)) / float(monitor_value)) * 100

    if percentage_change >= 5:
        direction = "up" if current_rate > float(monitor_value) else "down"
        return jsonify({
            'alert': True,
            'current_rate': current_rate,
            'monitor_value': float(monitor_value),
            'percentage_change': round(percentage_change, 2),
            'message': f"Alert: The currency has experienced a significant {direction} change of {percentage_change:.2f}%. Current rate: {current_rate}"
        })
    else:
        return jsonify({
            'alert': False,
            'current_rate': current_rate,
            'monitor_value': float(monitor_value),
            'percentage_change': round(percentage_change, 2),
            'message': f"The currency is stable. Current change is within 5% of the monitored value."
        })

if __name__ == '__main__':
    app.run(debug=True)
