
import streamlit as st
import pandas as pd
import joblib

# Load Models
model_tourist_number = joblib.load('weights/model_tourist_number.pkl')
model_model_value = joblib.load('weights/model_model_value.pkl')

# Configure the page
st.set_page_config(page_title="Murtad - From Data To Smart Moves", layout="centered")

# Landing Page
def landing_page():
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src='deploy/imges.png' width='300'/>
            <h2 style='margin-top: 30px;'>Here, data speaks the language of the future.<br>
            We reveal the stories behind the numbers behind destinations,<br>
            so your vision is clearer and your steps are smarter.</h2>
            <p style='margin-top: 20px;'>Explore the future of tourism trends and spending in Saudi Arabia<br>
            with AI-powered insights and predictions.</p>
            <br><br>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Get Started"):
        st.session_state.page = 'prediction'

# Prediction Page
def prediction_page():
    st.sidebar.title("About the App")
    st.sidebar.markdown("""
    This app predicts:

    - **Number of Tourists**
    - **Tourism Income (SAR)**

    Based on:
    - Province
    - Tourism Type
    - Indicator
    - Year
    - Month
    """)

    st.title("Welcome to Murtad")
    st.subheader("Customize Your Tourism Forecast")

    # Inputs
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("Select Year", [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026])
        month = st.selectbox("Select Month", list(range(1,13)))
        province = st.selectbox("Select Province", [
            'Al Bahah', 'Al Jawf', 'Al Madinah', 'Al-Qassim', 'Asir', 'Eastern Province',
            'Hail', 'Jazan', 'Makkah', 'Najran', 'Northern Borders', 'Riyadh', 'Tabuk'
        ])
    with col2:
        indicator = st.selectbox("Select Indicator", ['Overnight Visitors', 'Tourism Revenue'])
        tourism_type = st.selectbox("Select Tourism Type", ['domestics_tourism', 'inbound_tourism'])

    if st.button("Predict"):
        input_data = pd.DataFrame({
            'Province': [province],
            'month': [month],
            'tourism type': [tourism_type],
            'Indicator': [indicator]
        })

        if indicator == "Overnight Visitors":
            prediction = model_tourist_number.predict(input_data)[0]
            st.success(f"Predicted Number of Tourists: {int(prediction):,}")
        else:
            prediction = model_model_value.predict(input_data)[0]
            st.success(f"Predicted Tourism Income: {int(prediction):,} SAR")

# Navigation Control
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

if st.session_state.page == 'landing':
    landing_page()
else:
    prediction_page()
