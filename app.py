import streamlit as st
import numpy as np
import pickle
import os
from PIL import Image

# Load trained model with error handling
MODEL_PATH = "model.pkl"

if os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, "rb") as file:
            model = pickle.load(file)
    except Exception as e:
        st.error(f"⚠ Error loading model: {e}")
        st.stop()
else:
    st.error("⚠ Model file not found! Please ensure 'model.pkl' is in the same directory.")
    st.stop()

# Set up session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Pages Navigation
page = st.sidebar.radio("Navigation", ["Login", "Wine Quality Predictor", "About Website"])

def login_page():
    st.image("wbg.jpeg", use_container_width=True)
    st.markdown("""<h1 style='text-align: center;'>🍷 Welcome to Wine Quality Predictor</h1>""", unsafe_allow_html=True)
    st.subheader("Login / Sign Up")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:  # Simple authentication check
            st.session_state.authenticated = True
            st.success("Login successful! Navigate to 'Wine Quality Predictor' from the sidebar.")
        else:
            st.error("Please enter valid credentials.")

def wine_quality_page():
    if not st.session_state.authenticated:
        st.warning("Please login first from the Login page.")
        return
    
    st.title("🍷 Wine Quality Predictor")
    st.subheader("Enter the Wine Characteristics")
    
    # Define input fields
    default_values = {"fixed_acidity": 5.2, "volatile_acidity": 0.7, "citric_acid": 0.0, "residual_sugar": 1.9,
                      "chlorides": 0.076, "free_sulfur_dioxide": 11.0, "total_sulfur_dioxide": 34.0, "density": 0.9978,
                      "pH": 3.51, "sulphates": 0.56, "alcohol": 9.4}
    
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Input fields
    fixed_acidity = st.number_input("Fixed Acidity", min_value=0.0, value=st.session_state.fixed_acidity)
    volatile_acidity = st.number_input("Volatile Acidity", min_value=0.0, value=st.session_state.volatile_acidity)
    citric_acid = st.number_input("Citric Acid", min_value=0.0, value=st.session_state.citric_acid)
    residual_sugar = st.number_input("Residual Sugar", min_value=0.0, value=st.session_state.residual_sugar)
    chlorides = st.number_input("Chlorides", min_value=0.0, value=st.session_state.chlorides)
    free_sulfur_dioxide = st.number_input("Free Sulfur Dioxide", min_value=0.0, value=st.session_state.free_sulfur_dioxide)
    total_sulfur_dioxide = st.number_input("Total Sulfur Dioxide", min_value=0.0, value=st.session_state.total_sulfur_dioxide)
    density = st.number_input("Density", min_value=0.0, value=st.session_state.density, format="%.5f")
    pH = st.number_input("pH", min_value=0.0, value=st.session_state.pH)
    sulphates = st.number_input("Sulphates", min_value=0.0, value=st.session_state.sulphates)
    alcohol = st.number_input("Alcohol", min_value=0.0, value=st.session_state.alcohol)
    
    col1, col2 = st.columns(2)
    
    if col1.button("Predict Quality"):
        features = np.array([fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,
                             free_sulfur_dioxide, total_sulfur_dioxide, density, pH, sulphates, alcohol]).reshape(1, -1)
        
        quality_score = model.predict(features)[0]
        
        if quality_score >= 6:
            st.success(f"🍷 Quality: {quality_score} - Good Quality Wine!")
        else:
            st.error(f"🥂 Quality: {quality_score} - Poor Quality Wine.")
    
    if col2.button("Reset Fields"):
        for key in default_values.keys():
            st.session_state[key] = default_values[key]
        st.experimental_rerun()

def about_page():
    st.title("About This Website")
    st.write("""
    This website allows users to predict the quality of wine based on various chemical properties.
    Using a trained Machine Learning model, users can input data and get instant predictions.
    
    **Features:**
    - Secure Login System
    - Interactive User Interface
    - AI-Based Predictions
    - Reset Field Functionality
    - Fully Responsive Design
    """)
    st.image("wbg.jpeg", use_container_width=True)
    
# Page Routing
if page == "Login":
    login_page()
elif page == "Wine Quality Predictor":
    wine_quality_page()
elif page == "About Website":
    about_page()
