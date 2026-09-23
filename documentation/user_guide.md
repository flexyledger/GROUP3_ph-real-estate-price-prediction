# Philippine Real Estate Price Predictor — User Guide

## Introduction
Welcome to the Philippine Real Estate Price Predictor! This application provides data-driven estimates of residential property values across the Philippines based on a machine learning model trained on ~1,500 real estate listings.

## Getting Started

### 1. Launching the Application
Make sure you have installed the requirements (`pip install -r requirements.txt`) and run the application from your terminal:
```bash
streamlit run app/main.py
```
Your default web browser will automatically open the application at `http://localhost:8501`.

### 2. How to Use the Predictor

The application interface is divided into two main sections:

#### A. Sidebar: Property Features Input
Here you will define the characteristics of the property you want to value:
* **Location:** Select the Barangay, City, or Province from the dropdown. This is a crucial factor in property valuation.
* **Bedrooms:** Number of bedrooms in the property.
* **Floor Area (sqm):** The interior floor space of the property in square meters.
* **Bathrooms:** Number of bathrooms.
* **Land Area (sqm):** The lot area. For condominium units, please enter `0`.
* **Geographic Coordinates:** The latitude and longitude will automatically update to the average coordinates of the selected location. You can manually adjust these if you know the exact coordinates of the property.

#### B. Main Screen: Valuation & Information
* **Predict Price Button:** Once you have entered all the features, click this button to generate the valuation.
* **Estimated Market Value:** The model's primary prediction, displayed in Philippine Pesos (₱).
* **Confidence Range:** Provides an approximate ±15% range around the estimated value to account for normal market variance and unobserved factors (like property condition, age, or view).
* **Model Information:** Details about the underlying algorithm (Random Forest Regressor) and preprocessing steps used to generate the prediction.

## Troubleshooting & Constraints
* **"Input Error" Messages:** The application has strict validation rules. For example, floor area cannot be negative or too small, and coordinates must fall within the Philippines. Adjust your inputs according to the error message.
* **Luxury Properties:** The model was calibrated on the main market segment. Estimates for ultra-luxury properties (historically >₱100M) may be less accurate as they were capped during training to prevent skewing the general model.
* **Rural Areas:** The model performs best in high-density urban areas like Metro Manila, Cebu, and Davao, where there is substantial listing data.
