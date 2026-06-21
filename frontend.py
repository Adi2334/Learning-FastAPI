import streamlit as st
import requests
from schema.models import Patient

API_URL = "http://localhost:8001/patient/predict"

st.title("Insurance Premium Prediction")
st.markdown("Enter patient details to predict insurance premium category")


# Input fields
name = st.text_input("Name")
email = st.text_input("Email")
gender = st.selectbox("Gender", ["Male", "Female", "Other"])    
age = st.number_input("Age", min_value=1, max_value=120, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=3.0, value=1.75)
smoker = st.selectbox("Are you a smoker?", [True, False])
income_lpa = st.number_input("Income (LPA)", min_value=0.0, max_value=1000.0, value=10.0)
occupation = st.selectbox("Occupation", ['retired','freelancer','student','government_job','business_owner','unemployed','private_job'])    

if st.button("Predict"):
    patient_data = {
        "name": name,
        "email": email,
        "gender": gender,
        "age": age,
        "weight": weight,
        "height": height,
        "smoker": smoker,
        "income_lpa": income_lpa,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=patient_data)
        response.raise_for_status()
        prediction = response.json()
        st.success(f"Predicted Insurance Premium Category: {prediction}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error occurred while making the API request: {e}")