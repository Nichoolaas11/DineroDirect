// Ensure the DOM is fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function () {

    // Handle form submissions for comparing rates
    document.getElementById('compare-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission behavior

        // Get form data for comparison
        const fromCurrency = document.getElementById('from_currency').value;
        const toCurrency = document.getElementById('to_currency').value;

        // Send a POST request to the Flask backend to get the current rate and other data
        fetch('http://127.0.0.1:5000/compare', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ from_currency: fromCurrency, to_currency: toCurrency })
        })
        .then(response => response.json()) // Parse the JSON response
        .then(data => {
            const resultDiv = document.getElementById('compare-result'); // Reference to the result div
            if (data.error) {
                resultDiv.innerHTML = `<strong>Error:</strong> ${data.error}`; // Display error message
            } else {
                // Display the comparison result with rate change and percentage change
                resultDiv.innerHTML = `<strong>Comparison Result:</strong><br>
                    Current Rate: ${data.current_rate}<br>
                    Old Rate: ${data.old_rate}<br>
                    Rate Change: ${data.rate_change} (${data.percentage_change}%)`;
            }
        })
        .catch(error => console.error('Error:', error)); // Handle any errors that occur
    });

    // Handle form submissions for monitoring currencies
    document.getElementById('monitor-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission behavior

        // Get form data for monitoring
        const fromCurrency = document.getElementById('monitor_from_currency').value;
        const toCurrency = document.getElementById('monitor_to_currency').value;
        const monitorValue = document.getElementById('monitor_value').value;

        // Send a POST request to the Flask backend to monitor the currency pair
        fetch('http://127.0.0.1:5000/monitor', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ from_currency: fromCurrency, to_currency: toCurrency, monitor_value: monitorValue })
        })
        .then(response => response.json()) // Parse the JSON response
        .then(data => {
            const resultDiv = document.getElementById('monitor-result'); // Reference to the result div
            if (data.error) {
                resultDiv.innerHTML = `<strong>Error:</strong> ${data.error}`; // Display error message
            } else {
                resultDiv.innerHTML = `<strong>Monitoring Result:</strong> ${data.message}`; // Display the monitoring result message
            }
        })
        .catch(error => console.error('Error:', error)); // Handle any errors that occur
    });
});
