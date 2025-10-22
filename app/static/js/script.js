document.getElementById('rent-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = {
        postal_code: formData.get('postal_code'),
        property_size: parseInt(formData.get('property_size')),
        bedrooms: parseInt(formData.get('bedrooms')),
        property_age: parseInt(formData.get('property_age'))
    };

    const resultDiv = document.getElementById('result');

    fetch('/api/predict_rent', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            resultDiv.innerHTML = `<span style="color: red;">Error: ${result.error}</span>`;
        } else {
            resultDiv.innerHTML = `Predicted Rent: <strong>$${result.predicted_rent}</strong>`;
        }
        resultDiv.style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        resultDiv.innerHTML = 'An error occurred. Please try again.';
        resultDiv.style.display = 'block';
    });
});