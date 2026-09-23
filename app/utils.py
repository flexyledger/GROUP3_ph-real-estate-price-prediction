import pandas as pd
import numpy as np

def validate_inputs(bedrooms, bath, floor_area, land_area, lat, lon):
    """
    Validates user inputs from the Streamlit application.
    Returns (is_valid, error_message).
    """
    if floor_area < 5:
        return False, "Floor area must be at least 5 sqm."
        
    if land_area < 0:
        return False, "Land area cannot be negative."
        
    # Approximate bounding box for the Philippines
    if not (4.5 <= lat <= 21.5):
        return False, "Latitude is outside the Philippines (approx. 4.5 to 21.5)."
        
    if not (116.0 <= lon <= 127.0):
        return False, "Longitude is outside the Philippines (approx. 116.0 to 127.0)."
        
    return True, ""

def format_price(price_php):
    """
    Formats the predicted price into a readable PHP string.
    """
    return f"₱ {price_php:,.2f}"

def format_confidence_interval(price_php, rmse_margin=0.15):
    """
    Generates a rough confidence interval based on a percentage margin
    or an RMSE value. Here we just use +/- 15% as a heuristic for 
    the Streamlit display.
    """
    lower = price_php * (1 - rmse_margin)
    upper = price_php * (1 + rmse_margin)
    return f"₱ {lower:,.2f} - ₱ {upper:,.2f}"
