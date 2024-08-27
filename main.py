import streamlit as st
import pickle
import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler

# loading the saved model
loaded_model = pickle.load(open('./Model/RF_model.pkl', 'rb'))

with open('./Model/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Load categories from the JSON file
with open('categories.json', 'r') as f:
    categories = json.load(f)

# Initialize label encoders for profession, city, and state
profession_encoder = LabelEncoder()
city_encoder = LabelEncoder()
state_encoder = LabelEncoder()

# Fit the encoders with the loaded categories
profession_encoder.fit(categories['profession'])
city_encoder.fit(categories['city'])
state_encoder.fit(categories['state'])

# Function to make predictions
def make_prediction(input_data):

    # Convert input data to DataFrame
    input_df = pd.DataFrame([input_data])

    # Scale the numerical features using the previously fitted scaler
    scaled_input = scaler.transform(input_df[['income', 'age', 'experience', 'current_house_yrs']])

    # Convert the scaled values back to a DataFrame
    scaled_input_df = pd.DataFrame(scaled_input, columns=['income', 'age', 'experience', 'current_house_yrs'])

    # Update the input dataframe with scaled numerical data
    input_df.update(scaled_input_df)

    # Make prediction with the model
    prediction = loaded_model.predict(input_df)

    return prediction[0]

# Streamlit app
def main():
    st.title("Loan Eligibility Prediction")

    # Collect user input
    income = st.number_input("Annual Income ($)", min_value=0, step=1000)
    age = st.number_input("Age", min_value=0, max_value=100)
    experience = st.number_input("Experience (years)", min_value=0, max_value=100)
    marital_status = st.selectbox("Marital Status", ["Married", "Single"])
    car_ownership = st.selectbox("Car Ownership", ["Yes", "No"])
    profession = st.selectbox("Profession:", categories['profession'])
    city = st.selectbox("City:", categories['city'])
    state = st.selectbox("State:", categories['state'])
    current_house_yrs = st.number_input("Current House Years", min_value=0, max_value=100)
    house_ownership = st.selectbox("House Ownership", ["No rent, No own", "Owned", "Rented"])

    # Encode categorical features using LabelEncoder
    profession_encoded = profession_encoder.transform([profession])[0]
    city_encoded = city_encoder.transform([city])[0]
    state_encoded = state_encoder.transform([state])[0]

    # Map categorical input to their encoded values
    marital_status_encoded = 1 if marital_status == "Married" else 0
    car_ownership_encoded = 1 if car_ownership == "Yes" else 0

    # One-hot encode the house ownership
    house_ownership_encoded = {
        "house_ownership_norent_noown": 1 if house_ownership == "No rent, No own" else 0,
        "house_ownership_owned": 1 if house_ownership == "Owned" else 0,
        "house_ownership_rented": 1 if house_ownership == "Rented" else 0,
    }

    # Create input data dictionary
    input_data = {
        'income': income,
        'age': age,
        'experience': experience,
        'married/single': marital_status_encoded,
        'car_ownership': car_ownership_encoded,
        'profession': profession_encoded,
        'city': city_encoded,
        'state': state_encoded,
        'current_house_yrs': current_house_yrs,
        **house_ownership_encoded
    }

    # Predict when the button is clicked
    if st.button("Predict Loan Eligibility"):
        prediction = make_prediction(input_data)
        if prediction == 0:
            st.success("The person is eligible for the loan.")
        else:
            st.error("The person is not eligible for the loan.")

if __name__ == "__main__":
    main()