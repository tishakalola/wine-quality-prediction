import streamlit as st
import json
import requests

# Simulate a session state to track login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    """Simulated login function."""
    st.title("🔐 Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "password123":  # Dummy credentials
            st.session_state.logged_in = True
            st.success("Login successful! Redirecting...")
            st.experimental_rerun()  # Refresh the page after login
        else:
            st.error("Invalid credentials, please try again!")

def predictor_page():
    """Main Wine Quality Predictor Page"""
    st.title("🍷 Wine Quality Predictor")

    # Dummy content box
    with st.container():
        st.subheader("📌 About This Predictor")
        st.write("This predictor uses machine learning to estimate wine quality based on chemical properties. Enter values below.")

    # Input fields
    fixed_acidity = st.number_input("Fixed Acidity")
    volatile_acidity = st.number_input("Volatile Acidity")
    citric_acid = st.number_input("Citric Acid")
    residual_sugar = st.number_input("Residual Sugar")
    chlorides = st.number_input("Chlorides")
    free_sulfur_dioxide = st.number_input("Free Sulfur Dioxide")
    total_sulfur_dioxide = st.number_input("Total Sulfur Dioxide")
    density = st.number_input("Density")
    pH = st.number_input("pH")
    sulphates = st.number_input("Sulphates")
    alcohol = st.number_input("Alcohol")

    if st.button("Predict Quality"):
        input_data = {
            "fixed_acidity": fixed_acidity,
            "volatile_acidity": volatile_acidity,
            "citric_acid": citric_acid,
            "residual_sugar": residual_sugar,
            "chlorides": chlorides,
            "free_sulfur_dioxide": free_sulfur_dioxide,
            "total_sulfur_dioxide": total_sulfur_dioxide,
            "density": density,
            "pH": pH,
            "sulphates": sulphates,
            "alcohol": alcohol
        }

        # Send data to backend for prediction (assuming you have a backend API)
        response = requests.post("http://localhost:5000/predict", json={"features": list(input_data.values())})
        if response.status_code == 200:
            prediction = response.json()["prediction"]
            st.success(f"Predicted Quality: {prediction}")
        else:
            st.error("Error: Unable to fetch prediction!")

# Main Logic - Show login first, then the predictor page
if st.session_state.logged_in:
    predictor_page()
else:
    login()
