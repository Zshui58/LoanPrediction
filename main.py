import streamlit as st
import pickle
import numpy as np
import json
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# loading the saved model
# loaded_model = pickle.load(open('./Model/RF_model.pkl', 'rb'))

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

# Define the categorical options globally
marriedsingle = ['Married', 'Single']
house = ['No rent,No own', 'Own', 'Rent']
car = ['No car', 'Yes, have car']

# Function to determine loan eligibility
def determine_eligibility(annual_income, age, experience, profession, city, state, current_job_yrs, current_house_yrs, maritalStatus, houseOwnership, carOwnership):
    # Label encode the categorical features
    profession_encoded = profession_encoder.transform([profession])[0]
    city_encoded = city_encoder.transform([city])[0]
    state_encoded = state_encoder.transform([state])[0]

    # Combine the input data into a single array
    input_data = [annual_income, age, experience, profession_encoded, city_encoded, state_encoded, current_job_yrs, current_house_yrs]

    # Encode categorical features
    married_single_encoded = [1, 0] if maritalStatus == 'Married' else [0, 1]
    car_ownership_encoded = [1, 0] if carOwnership == 'Yes, have car' else [0, 1]
    house_ownership_encoded = [1, 0, 0] if houseOwnership == 'No rent, No own' else [0, 1, 0] if houseOwnership == 'Own' else [0, 0, 1]

    # Combine all features
    input_data_combined = input_data + married_single_encoded + car_ownership_encoded + house_ownership_encoded

    # Ensure the input data has the correct shape
    input_data_as_numpy_array = np.asarray(input_data_combined).reshape(1, -1)

    # Make a prediction
    prediction = loaded_model.predict(input_data_as_numpy_array)
    print(prediction)

    if prediction[0] == 0:
        return 'The person gets the loan'
    else:
        return 'The person fails to get the loan'


# Streamlit application
def main():

    st.title("Loan Eligibility Checker")

    # Collecting user input
    st.header("Please enter your details:")
    annual_income = st.number_input("Annual Income ($)", min_value=0, step=1000)
    age = st.number_input("Age:", min_value=17, max_value=80)
    experience = st.number_input("Experience in work:")
    profession = st.selectbox("Profession:", categories['profession'])
    city = st.selectbox("City:", categories['city'])
    state = st.selectbox("State:", categories['state'])
    current_job_yrs = st.number_input("Current Job Years:")
    current_house_yrs = st.number_input("Current House Years:")
    maritalStatus = st.selectbox("Select Marital Status:", marriedsingle, index=0)
    houseOwnership = st.selectbox("Select House Ownership:", house, index=0)
    carOwnership = st.selectbox("Select Car Ownership:", car, index=0)

    # Code for Prediction
    eligibility_status = ''

    # Determine eligibility when the button is clicked
    if st.button("Check Eligibility"):
        eligibility_status = determine_eligibility(annual_income, age, experience, profession, city, state, current_job_yrs, current_house_yrs, maritalStatus, houseOwnership, carOwnership)
        st.subheader("Loan Eligibility Status:")
        st.write(eligibility_status)


if __name__ == "__main__":
    main()

