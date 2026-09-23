import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from utils import validate_inputs, format_price, format_confidence_interval

# --- Configuration ---
st.set_page_config(
    page_title="PH Real Estate Predictor",
    page_icon="🏠",
    layout="wide"
)

# --- Load Models & Data ---
@st.cache_resource
def load_models():
    # Define paths relative to the app/ directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, '../models/best_model.pkl')
    preprocessor_path = os.path.join(base_dir, '../models/preprocessor.pkl')
    
    model = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)
    return model, preprocessor

@st.cache_data
def load_locations():
    # Load locations from cleaned dataset to populate dropdown
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '../data/processed/cleaned_data.csv')
    df = pd.read_csv(data_path)
    locations = sorted(df['Location'].unique().tolist())
    
    # Also calculate average coordinates per location for default map placement
    loc_coords = df.groupby('Location')[['Latitude', 'Longitude']].mean().to_dict('index')
    return locations, loc_coords

try:
    model, preprocessor = load_models()
    locations, loc_coords = load_locations()
except Exception as e:
    st.error(f"Error loading required files. Please ensure models and data exist. Details: {e}")
    st.stop()

# --- UI Header ---
st.title("🏠 Philippine Real Estate Price Predictor")
st.markdown("""
This application estimates the market value of residential properties in the Philippines. 
It uses a **Random Forest Regressor** model trained on ~1,500 real estate listings.
""")

# --- Sidebar Inputs ---
st.sidebar.header("Property Features")

selected_location = st.sidebar.selectbox("Select Location (Barangay, City/Province)", locations)

# Set default coordinates based on selected location
default_lat = float(loc_coords[selected_location]['Latitude'])
default_lon = float(loc_coords[selected_location]['Longitude'])

col1, col2 = st.sidebar.columns(2)
with col1:
    bedrooms = st.number_input("Bedrooms", min_value=1, max_value=20, value=3, step=1)
    floor_area = st.number_input("Floor Area (sqm)", min_value=5, max_value=5000, value=120)
with col2:
    bathrooms = st.number_input("Bathrooms", min_value=1, max_value=20, value=2, step=1)
    land_area = st.number_input("Land Area (sqm)", min_value=0, max_value=10000, value=150, help="Enter 0 for condo units.")

st.sidebar.markdown("---")
st.sidebar.subheader("Geographic Coordinates")
latitude = st.sidebar.number_input("Latitude", value=default_lat, format="%.6f")
longitude = st.sidebar.number_input("Longitude", value=default_lon, format="%.6f")

# --- Main Content ---
col_main1, col_main2 = st.columns([2, 1])

with col_main1:
    st.subheader("Property Valuation")
    
    if st.button("Predict Price", type="primary"):
        # Validate inputs
        is_valid, error_msg = validate_inputs(bedrooms, bathrooms, floor_area, land_area, latitude, longitude)
        
        if not is_valid:
            st.error(f"⚠️ Input Error: {error_msg}")
        else:
            with st.spinner("Calculating valuation..."):
                # Prepare input dataframe
                input_data = pd.DataFrame({
                    'Location': [selected_location],
                    'Bedrooms': [bedrooms],
                    'Bath': [bathrooms],
                    'Floor_area (sqm)': [floor_area],
                    'Land_area (sqm)': [land_area],
                    'Latitude': [latitude],
                    'Longitude': [longitude]
                })
                
                try:
                    # 1. Transform features via preprocessor
                    X_processed = preprocessor.transform(input_data)
                    
                    # 2. Predict log price
                    log_price_pred = model.predict(X_processed)[0]
                    
                    # 3. Inverse transform (expm1) to get PHP
                    predicted_price = np.expm1(log_price_pred)
                    
                    # 4. Display results
                    st.success("Valuation Successful!")
                    
                    st.metric(label="Estimated Market Value", value=format_price(predicted_price))
                    
                    st.info(f"**Confidence Range (approx. ±15%):** {format_confidence_interval(predicted_price)}")
                    
                except Exception as e:
                    st.error(f"An error occurred during prediction: {e}")

with col_main2:
    st.subheader("Model Information")
    st.markdown("""
    * **Algorithm:** Random Forest Regressor
    * **Features Used:** 7 (Location, Beds, Baths, Floor Area, Land Area, Lat, Lon)
    * **Target:** Log1p(Price)
    * **Preprocessing:** Median Imputation, Target Encoding, Standard Scaling
    """)
    st.caption("Note: Extreme luxury properties (>₱100M) were capped during training to preserve accuracy for the main market segment.")

st.markdown("---")
st.caption("Developed by GROUP3 for the Machine Learning Final Project. Instructor: Professor Ken Oliver Caparros.")
