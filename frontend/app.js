// Ensure the DOM is fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function () {

    // Helper function to display a loader while fetching data
    function showLoader(show) {
        const loader = document.getElementById('preloader'); // Assuming you have a loader with this ID
        if (show) {
            loader.style.display = 'flex'; // Show the loader
        } else {
            loader.style.display = 'none'; // Hide the loader
        }
    }

    // Helper function to scroll smoothly to an element
    function scrollToElement(element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Handle form submissions for comparing rates
    document.getElementById('compare-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission behavior

        // Get form data for comparison
        const fromCurrency = document.getElementById('from_currency').value;
        const toCurrency = document.getElementById('to_currency').value;
        const resultDiv = document.getElementById('compare-result');

        // Simple validation
        if (!fromCurrency || !toCurrency) {
            resultDiv.innerHTML = `<strong>Error:</strong> Please select both currencies.`;
            resultDiv.style.color = 'red';
            scrollToElement(resultDiv); // Scroll to result
            return;
        }

        // Show loader
        showLoader(true);

        // Send a POST request to the Flask backend
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
            // Hide loader
            showLoader(false);

            if (data.error) {
                resultDiv.innerHTML = `<strong>Error:</strong> ${data.error}`;
                resultDiv.style.color = 'red';
            } else {
                resultDiv.innerHTML = `<strong>Comparison Result:</strong><br>
                    Current Rate: ${data.current_rate}<br>
                    Old Rate: ${data.old_rate}<br>
                    Rate Change: ${data.rate_change} (${data.percentage_change}%)`;
                resultDiv.style.color = '#333';
            }

            // Smooth scroll to result
            scrollToElement(resultDiv);
            // Animate result box background color for effect
            resultDiv.style.transition = 'background-color 0.3s ease';
            resultDiv.style.backgroundColor = '#e0f5e9'; // Light green to indicate success
            setTimeout(() => resultDiv.style.backgroundColor = '#f9f9f9', 300); // Revert after 300ms
        })
        .catch(error => {
            console.error('Error:', error);
            resultDiv.innerHTML = `<strong>Error:</strong> Something went wrong.`;
            resultDiv.style.color = 'red';
            scrollToElement(resultDiv);
            showLoader(false); // Hide loader in case of error
        });
    });

    // Handle form submissions for monitoring currencies
    document.getElementById('monitor-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission behavior

        // Get form data for monitoring
        const fromCurrency = document.getElementById('monitor_from_currency').value;
        const toCurrency = document.getElementById('monitor_to_currency').value;
        const monitorValue = document.getElementById('monitor_value').value;
        const resultDiv = document.getElementById('monitor-result');

        // Simple validation
        if (!fromCurrency || !toCurrency || !monitorValue) {
            resultDiv.innerHTML = `<strong>Error:</strong> Please fill in all fields.`;
            resultDiv.style.color = 'red';
            scrollToElement(resultDiv); // Scroll to result
            return;
        }

        // Show loader
        showLoader(true);

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
            // Hide loader
            showLoader(false);

            if (data.error) {
                resultDiv.innerHTML = `<strong>Error:</strong> ${data.error}`;
                resultDiv.style.color = 'red';
            } else {
                resultDiv.innerHTML = `<strong>Monitoring Result:</strong> ${data.message}`;
                resultDiv.style.color = '#333';
            }

            // Smooth scroll to result
            scrollToElement(resultDiv);
            // Animate result box background color for effect
            resultDiv.style.transition = 'background-color 0.3s ease';
            resultDiv.style.backgroundColor = '#e0f5e9'; // Light green to indicate success
            setTimeout(() => resultDiv.style.backgroundColor = '#f9f9f9', 300); // Revert after 300ms
        })
        .catch(error => {
            console.error('Error:', error);
            resultDiv.innerHTML = `<strong>Error:</strong> Something went wrong.`;
            resultDiv.style.color = 'red';
            scrollToElement(resultDiv);
            showLoader(false); // Hide loader in case of error
        });
    });

});
