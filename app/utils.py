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
    Generates an empirical valuation interval based on the test-set Mean 
    Absolute Percentage Error (MAPE = 14.31%, rounded to ±15%).
    Over 80% of held-out properties evaluate within ±11.9% absolute error.
    """
    lower = price_php * (1 - rmse_margin)
    upper = price_php * (1 + rmse_margin)
    return f"₱ {lower:,.2f} - ₱ {upper:,.2f}"

def calculate_mortgage(price_php, down_payment_pct=20.0, annual_interest_pct=7.0, loan_years=20):
    """
    Calculates retail mortgage financing metrics based on Philippine bank standards.
    Returns a dictionary of financing breakdown metrics.
    """
    down_payment = price_php * (down_payment_pct / 100.0)
    principal = max(0.0, price_php - down_payment)
    
    monthly_rate = (annual_interest_pct / 100.0) / 12.0
    num_payments = int(loan_years * 12)
    
    if monthly_rate > 0 and num_payments > 0:
        monthly_payment = principal * (monthly_rate * ((1 + monthly_rate) ** num_payments)) / (((1 + monthly_rate) ** num_payments) - 1)
    elif num_payments > 0:
        monthly_payment = principal / num_payments
    else:
        monthly_payment = 0.0
        
    total_payment = monthly_payment * num_payments
    total_interest = max(0.0, total_payment - principal)
    min_monthly_income = monthly_payment / 0.30 if monthly_payment > 0 else 0.0  # 30% gross rule
    
    return {
        'down_payment': down_payment,
        'principal': principal,
        'monthly_payment': monthly_payment,
        'total_payment': total_payment,
        'total_interest': total_interest,
        'min_monthly_income': min_monthly_income,
        'num_payments': num_payments
    }

def calculate_closing_costs(price_php):
    """
    Estimates Philippine standard property transfer and acquisition closing costs:
    - Documentary Stamp Tax (DST): 1.5%
    - Local Transfer Tax: 0.75%
    - Registration Fee: 0.25%
    - Notarial & Legal Documentation: 1.0%
    """
    dst = price_php * 0.015
    transfer_tax = price_php * 0.0075
    reg_fee = price_php * 0.0025
    notarial = price_php * 0.010
    total_closing = dst + transfer_tax + reg_fee + notarial
    
    return {
        'dst': dst,
        'transfer_tax': transfer_tax,
        'registration_fee': reg_fee,
        'notarial_fee': notarial,
        'total_closing_costs': total_closing
    }

def calculate_investment_metrics(price_php, floor_area, land_area=0, gross_yield_pct=6.5):
    """
    Estimates retail property investment and rental return metrics.
    """
    price_per_sqm_floor = price_php / floor_area if floor_area > 0 else 0.0
    price_per_sqm_land = (price_php / land_area) if land_area and land_area > 0 else 0.0
    
    annual_gross_rent = price_php * (gross_yield_pct / 100.0)
    monthly_gross_rent = annual_gross_rent / 12.0
    payback_years = (price_php / annual_gross_rent) if annual_gross_rent > 0 else 0.0
    
    return {
        'price_per_sqm_floor': price_per_sqm_floor,
        'price_per_sqm_land': price_per_sqm_land,
        'monthly_gross_rent': monthly_gross_rent,
        'annual_gross_rent': annual_gross_rent,
        'gross_yield_pct': gross_yield_pct,
        'payback_years': payback_years
    }

