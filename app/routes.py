# Import necessary libraries
import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from flask import request, jsonify, render_template
from flask_cors import CORS # To allow access from the frontend during development
from app import app

# Load the training data from the CSV file
data_path = os.path.join(os.path.dirname(__file__), '..', 'data.csv')
df = pd.read_csv(data_path)

# Define features (X) and labels (y)
features = ['Size', 'Bedrooms', 'Age', 'Postal_Code_56789', 'Postal_Code_23456', 'Postal_Code_34567', 'Postal_Code_45678']
X = df[features]
y = df['Rent']

# Train the model
model = LinearRegression()
model.fit(X, y)

CORS(app) # Allow access from anywhere (should be restricted in a production environment)

@app.route('/')
def index():
    sample_data = df.to_dict('records')
    feature_names = df.columns.tolist()
    return render_template('index.html', sample_data=sample_data, feature_names=feature_names)


# Rent prediction API endpoint
@app.route('/api/predict_rent', methods=['POST'])
def predict_rent():
    # Receive JSON data from the frontend
    data = request.get_json()
    
    # Check for mandatory parameters
    if not all(k in data for k in ('postal_code', 'property_size', 'bedrooms', 'property_age')):
        return jsonify({"error": "Missing parameters"}), 400

    # Input values
    postal_code = str(data['postal_code'])
    size = int(data['property_size'])
    # Convert size from m² to sqft (1 m² = 10.764 sqft)
    size_sqft = round(size * 10.764)
    bedrooms = int(data['bedrooms'])
    age = int(data['property_age'])

    # Input validation
    if size <= 0 or bedrooms < 0 or age < 0:
        return jsonify({"error": "Property size, bedrooms, and age must be positive values."}), 400

    # Range validation (based on training data)
    if not (80 <= size <= 300):
        return jsonify({"error": "Property size (m²) must be between 80 and 300."}), 400
    if not (1 <= bedrooms <= 5):
        return jsonify({"error": "Number of bedrooms must be between 1 and 5."}), 400
    if not (1 <= age <= 20):
        return jsonify({"error": "Property age (years) must be between 1 and 20."}), 400
    
    # Convert to the input format for the model (reproduce One-Hot Encoding)
    input_vector = np.zeros(len(features))
    
    # 1. Set Size, Bedrooms and Age
    input_vector[0] = size_sqft
    input_vector[1] = bedrooms
    input_vector[2] = age
    
    # 2. Set the One-Hot vector corresponding to the Postal Code
    try:
        pc_index = features.index(f'Postal_Code_{postal_code}')
        input_vector[pc_index] = 1
    except ValueError:
        # Handling for unrecognized postal codes (here, it's an error)
        return jsonify({"error": "Invalid postal code"}), 400

    # Execute the prediction
    prediction = model.predict([input_vector])
    predicted_rent = max(100, round(prediction[0]))
    
    # Return the result in JSON format
    return jsonify({
        "predicted_rent": predicted_rent,
        "model_used": "Multiple Linear Regression"
    })
