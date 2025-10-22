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
    return render_template('index.html')


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
    bedrooms = int(data['bedrooms'])
    age = int(data['property_age'])

    # Input validation
    if size <= 0 or bedrooms < 0 or age < 0:
        return jsonify({"error": "Property size, bedrooms, and age must be positive values."}), 400
    
    # Convert to the input format for the model (reproduce One-Hot Encoding)
    input_vector = np.zeros(len(features))
    
    # 1. Set Size, Bedrooms and Age
    input_vector[0] = size
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
