import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import altair as alt
import pydeck as pdk

from utils import (
    validate_inputs,
    format_price,
    format_confidence_interval,
    calculate_mortgage,
    calculate_closing_costs,
    calculate_investment_metrics
)

# --- Configuration ---
st.set_page_config(
    page_title="Property Retail Calculator | PH Real Estate",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Responsive Modern Fintech CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
    }

    /* Main Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #0d1527 0%, #070b14 100%);
        color: #f1f5f9;
    }

    /* Header Styling */
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
        line-height: 1.2;
    }

    .hero-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.15rem;
        font-weight: 400;
        max-width: 850px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.5;
    }

    /* Badge Pills */
    .badge-container {
        display: flex;
        justify-content: center;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin-bottom: 2rem;
    }

    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-radius: 9999px;
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.2);
        color: #cbd5e1;
    }

    .badge-accent {
        background: rgba(14, 165, 233, 0.15);
        border-color: rgba(56, 189, 248, 0.4);
        color: #38bdf8;
    }

    .badge-emerald {
        background: rgba(16, 185, 129, 0.15);
        border-color: rgba(52, 211, 153, 0.4);
        color: #34d399;
    }

    /* Card Panels */
    .calc-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.2rem;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .calc-card:hover {
        border-color: rgba(99, 102, 241, 0.35);
    }

    .card-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Metric Display Enhancement */
    [data-testid="stMetricValue"] {
        font-size: 2.6rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1 !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Input Controls */
    .stTextInput input, .stNumberInput input, .stSelectbox > div > div > div {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox > div > div > div:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.5);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
        padding: 8px 16px;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(30, 41, 59, 0.9) !important;
        color: #38bdf8 !important;
        border-bottom: 2px solid #38bdf8 !important;
    }

    /* Custom Responsive Tables & Grids */
    .fin-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        font-size: 0.92rem;
    }

    .fin-row:last-child {
        border-bottom: none;
    }

    .fin-label {
        color: #94a3b8;
    }

    .fin-value {
        font-weight: 600;
        color: #f8fafc;
    }

    .fin-highlight {
        color: #34d399;
        font-weight: 700;
    }

    /* Responsive Breakpoints */
    @media (max-width: 992px) {
        .hero-title {
            font-size: 2rem;
        }
        .hero-subtitle {
            font-size: 1rem;
            margin-bottom: 1rem;
        }
        [data-testid="stMetricValue"] {
            font-size: 2rem !important;
        }
    }

    @media (max-width: 640px) {
        .hero-title {
            font-size: 1.6rem;
        }
        .calc-card {
            padding: 14px;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.7rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Load Models & Dataset ---
@st.cache_resource
def load_models():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, '../models/best_model.pkl')
    preprocessor_path = os.path.join(base_dir, '../models/preprocessor.pkl')
    
    model = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)
    return model, preprocessor

@st.cache_data
def load_dataset():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '../data/processed/cleaned_data.csv')
    df = pd.read_csv(data_path)
    locations = sorted(df['Location'].dropna().unique().tolist())
    loc_coords = df.groupby('Location')[['Latitude', 'Longitude']].mean().to_dict('index')
    
    # Precompute location statistics for benchmarking
    loc_stats = df.groupby('Location')['Price (PHP)'].agg(['count', 'min', 'median', 'mean', 'max']).to_dict('index')
    
    return df, locations, loc_coords, loc_stats

try:
    model, preprocessor = load_models()
    df_listings, locations, loc_coords, loc_stats = load_dataset()
except Exception as e:
    st.error(f"⚠️ Error loading required model or dataset: {e}")
    st.stop()

# --- Hero Header ---
st.markdown('<div class="hero-title">Property Retail Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Residential Real Estate Price Estimation Using Structure And Geographic Variables</div>', unsafe_allow_html=True)

st.markdown("""
<div class="badge-container">
    <span class="badge-pill badge-accent">🏢 GROUP3</span>
    <span class="badge-pill badge-emerald">🌲 Random Forest Regressor</span>
    <span class="badge-pill">📊 Lamudi PH Real Estate Dataset</span>
    <span class="badge-pill">🎯 CCMACLRL - COM243ML</span>
</div>
""", unsafe_allow_html=True)

# --- Presets for Fast User Selection ---
PRESETS = {
    "Custom Setup": None,
    "Standard 2BR Urban Condo": {"beds": 2, "baths": 1, "floor": 55, "land": 0},
    "Spacious 3BR Executive Condo": {"beds": 3, "baths": 2, "floor": 110, "land": 0},
    "Suburban Family Townhouse": {"beds": 3, "baths": 2, "floor": 120, "land": 100},
    "Single Detached House & Lot": {"beds": 4, "baths": 3, "floor": 220, "land": 250},
    "Luxury Subdivision Estate": {"beds": 5, "baths": 5, "floor": 450, "land": 600}
}

# --- Responsive Split View (PC Horizontal & Vertical / Mobile Adaptive) ---
col_inputs, col_valuation = st.columns([1.15, 1], gap="medium")

with col_inputs:
    st.markdown("""
    <div class="calc-card">
        <div class="card-title">📍 Structural & Geographic Variables</div>
    """, unsafe_allow_html=True)

    preset_name = st.selectbox(
        "⚡ Quick Property Profile Preset",
        list(PRESETS.keys()),
        index=0,
        help="Select a typical property type to auto-fill structural values, or customize freely."
    )
    preset_data = PRESETS[preset_name]

    default_loc_idx = locations.index("San Antonio, Pasig") if "San Antonio, Pasig" in locations else 0
    selected_location = st.selectbox(
        "Location (Barangay, City / Municipality)",
        locations,
        index=default_loc_idx,
        help="Geographic anchor used for Target Encoding in the ML pipeline."
    )

    default_lat = float(loc_coords[selected_location]['Latitude'])
    default_lon = float(loc_coords[selected_location]['Longitude'])

    # Coordinates row
    c_lat, c_lon = st.columns(2)
    with c_lat:
        latitude = st.number_input("Latitude (°N)", value=default_lat, format="%.6f", help="Philippine latitude boundaries (4.5 to 21.5).")
    with c_lon:
        longitude = st.number_input("Longitude (°E)", value=default_lon, format="%.6f", help="Philippine longitude boundaries (116.0 to 127.0).")

    # Structural inputs
    init_beds = preset_data["beds"] if preset_data else 3
    init_baths = preset_data["baths"] if preset_data else 2
    init_floor = preset_data["floor"] if preset_data else 120
    init_land = preset_data["land"] if preset_data else 150

    s_col1, s_col2 = st.columns(2)
    with s_col1:
        bedrooms = st.number_input("Bedrooms", min_value=1, max_value=20, value=int(init_beds), step=1)
        floor_area = st.number_input("Floor Area (m²)", min_value=5, max_value=5000, value=int(init_floor), step=5)

    with s_col2:
        bathrooms = st.number_input("Bathrooms", min_value=1, max_value=20, value=int(init_baths), step=1)
        land_area = st.number_input("Land Area (m²)", min_value=0, max_value=10000, value=int(init_land), step=10, help="Enter 0 for high-rise condominium units.")

    st.markdown("</div>", unsafe_allow_html=True)

# Validation & Live Prediction
is_valid, error_msg = validate_inputs(bedrooms, bathrooms, floor_area, land_area, latitude, longitude)
predicted_price = 0.0

with col_valuation:
    st.markdown("""
    <div class="calc-card">
        <div class="card-title">🏷️ Retail Price Valuation Result</div>
    """, unsafe_allow_html=True)

    if not is_valid:
        st.error(f"⚠️ **Validation Check Failed:** {error_msg}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Construct DataFrame matching the pipeline specification
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
            X_processed = preprocessor.transform(input_data)
            log_price_pred = model.predict(X_processed)[0]
            predicted_price = float(np.expm1(log_price_pred))

            st.metric(label="Estimated Retail Market Price", value=format_price(predicted_price))

            # Metric highlights
            price_sqm_floor = predicted_price / floor_area if floor_area > 0 else 0
            price_sqm_land = (predicted_price / land_area) if land_area > 0 else 0

            q_col1, q_col2 = st.columns(2)
            with q_col1:
                st.markdown(f"""
                <div class="fin-row">
                    <span class="fin-label">Confidence Range (±15%):</span>
                    <span class="fin-value">{format_confidence_interval(predicted_price)}</span>
                </div>
                <div class="fin-row">
                    <span class="fin-label">Floor Price / m²:</span>
                    <span class="fin-highlight">{format_price(price_sqm_floor)}/m²</span>
                </div>
                """, unsafe_allow_html=True)

            with q_col2:
                land_str = f"{format_price(price_sqm_land)}/m²" if land_area > 0 else "Condo Unit (N/A)"
                st.markdown(f"""
                <div class="fin-row">
                    <span class="fin-label">Land Price / m²:</span>
                    <span class="fin-value">{land_str}</span>
                </div>
                <div class="fin-row">
                    <span class="fin-label">Inference Status:</span>
                    <span class="fin-highlight">● Live Synced</span>
                </div>
                """, unsafe_allow_html=True)

            # Quick summary bar
            st.markdown(f"""
            <div style="margin-top: 15px; padding: 10px 14px; background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 10px; font-size: 0.88rem; color: #bae6fd;">
                <strong>💡 Market Valuation Insight:</strong> This valuation is driven by Random Forest ensemble inference across structural geometry and localized coordinate embeddings for <em>{selected_location}</em>.
            </div>
            """, unsafe_allow_html=True)

        except Exception as ex:
            st.error(f"Inference computation error: {ex}")

    st.markdown("</div>", unsafe_allow_html=True)

# --- Full-Width Interactive Feature Tabs ---
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

tab_calc, tab_model, tab_geo, tab_specs = st.tabs([
    "🧮 Retail & Mortgage Calculator",
    "🌲 Random Forest Insights & Feature Importance",
    "🗺️ Geospatial & Neighborhood Benchmark",
    "📋 Academic Methodology & Specs"
])

# --- TAB 1: RETAIL & MORTGAGE FINANCING CALCULATOR ---
with tab_calc:
    st.markdown("""
    <div class="calc-card">
        <div class="card-title">💰 Philippine Real Estate Retail Financing & Investment Breakdown</div>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.2rem;">
            Configure retail mortgage terms, estimated closing fees (DST, Transfer Tax, Registration), and rental return metrics based on standard Philippine retail acquisition guidelines.
        </p>
    """, unsafe_allow_html=True)

    if predicted_price > 0:
        param_col1, param_col2, param_col3, param_col4 = st.columns(4)
        with param_col1:
            down_pct = st.slider("Down Payment (%)", min_value=10, max_value=50, value=20, step=5)
        with param_col2:
            loan_tenure = st.slider("Loan Tenure (Years)", min_value=5, max_value=30, value=20, step=1)
        with param_col3:
            interest_rate = st.slider("Annual Interest Rate (%)", min_value=4.0, max_value=12.0, value=7.0, step=0.25)
        with param_col4:
            rental_yield_target = st.slider("Est. Gross Rental Yield (%)", min_value=3.0, max_value=12.0, value=6.5, step=0.5)

        # Computations
        mortgage = calculate_mortgage(predicted_price, down_payment_pct=down_pct, annual_interest_pct=interest_rate, loan_years=loan_tenure)
        closing = calculate_closing_costs(predicted_price)
        investment = calculate_investment_metrics(predicted_price, floor_area, land_area, gross_yield_pct=rental_yield_target)

        total_cash_out = mortgage['down_payment'] + closing['total_closing_costs']

        f_col1, f_col2, f_col3 = st.columns(3, gap="medium")

        with f_col1:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.6); padding: 16px; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.15); height: 100%;">
                <div style="font-weight: 700; color: #38bdf8; margin-bottom: 12px; font-size: 1.05rem;">🏦 Mortgage Amortization</div>
                <div class="fin-row">
                    <span class="fin-label">Estimated Monthly Payment:</span>
                    <span class="fin-highlight" style="font-size: 1.15rem;">{format_price(mortgage['monthly_payment'])}</span>
                </div>
                <div class="fin-row">
                    <span class="fin-label">Loan Principal ({(100-down_pct)}%):</span>
                    <span class="fin-value">{format_price(mortgage['principal'])}</span>
                </div>
                <div class="fin-row">
                    <span class="fin-label">Total Loan Interest:</span>
                    <span class="fin-value">{format_price(mortgage['total_interest'])}</span>
                </div>
                <div class="fin-row">
                    <span class="fin-label">Total Loan Repayment:</span>
                    <span class="fin-value">{format_price(mortgage['total_payment'])}</span>
                </div>
                <div class="fin-row">
                    <span class="fin-label">Min. Monthly Income (30% Rule):</span>
                    <span class="fin-value" style="color: #fde047;">{format_price(mortgage['min_monthly_income'])}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with f_col2:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.6); padding: 16px; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.15); height: 100%;">
                <div style="font-weight: 700; color: #c084fc; margin-bottom: 12px; font-size: 1.05rem;">📑 Acquisition & Closing Fees</div>
                <div class="fin-row">
                    <span class="fin-label">Down Payment ({down_pct}%):</span>
                    <span class="fin-value">{format_price(mortgage['down_payment'])}</span>
                </div>
                <div class="fin-row">
                    <span class="fin-label">Doc. Stamp Tax (DST 1.5%):</span>
                    <span class="fin-value">{format_price(closing['dst'])}</span>
                </div>
                <div class="fin-row">
                    <span class="fin-label">Local Transfer Tax (0.75%):</span>
                    <span class="fin-value">{format_price(closing['transfer_tax'])}</span>
                </div>
                <div class="fin-row">
                    <span class="fin-label">LRA Registration (0.25%):</span>
                    <span class="fin-value">{format_price(closing['registration_fee'])}</span>
                </div>
                <div class="fin-row">
                    <span class="fin-label">Notarial & Legal (1.0%):</span>
                    <span class="fin-value">{format_price(closing['notarial_fee'])}</span>
                </div>
                <div class="fin-row" style="border-top: 1px dashed rgba(255,255,255,0.2); padding-top: 8px;">
                    <span class="fin-label" style="font-weight: 700; color: #f8fafc;">Total Initial Cash Out:</span>
                    <span class="fin-highlight">{format_price(total_cash_out)}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with f_col3:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.6); padding: 16px; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.15); height: 100%;">
                <div style="font-weight: 700; color: #34d399; margin-bottom: 12px; font-size: 1.05rem;">📈 Rental & Investment Yield</div>
                <div class="fin-row">
                    <span class="fin-label">Est. Monthly Gross Rent:</span>
                    <span class="fin-highlight" style="font-size: 1.15rem;">{format_price(investment['monthly_gross_rent'])}</span>
                </div>
                <div class="fin-row">
                    <span class="fin-label">Est. Annual Gross Rent:</span>
                    <span class="fin-value">{format_price(investment['annual_gross_rent'])}</span>
                </div>
                <div class="fin-row">
                    <span class="fin-label">Target Gross Rental Yield:</span>
                    <span class="fin-value">{rental_yield_target:.1f}%</span>
                </div>
                <div class="fin-row">
                    <span class="fin-label">Gross Capital Payback:</span>
                    <span class="fin-value">{investment['payback_years']:.1f} Years</span>
                </div>
                <div class="fin-row">
                    <span class="fin-label">Net Monthly Cash Flow est.:</span>
                    <span class="fin-value" style="color: {'#34d399' if (investment['monthly_gross_rent'] - mortgage['monthly_payment']) >= 0 else '#f87171'};">
                        {format_price(investment['monthly_gross_rent'] - mortgage['monthly_payment'])}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Capital Allocation Chart
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.markdown("##### 📊 Capital Allocation Breakdown")
        
        alloc_df = pd.DataFrame({
            "Component": ["Loan Principal", "Down Payment", "Closing Fees (Taxes/LRA)"],
            "Amount_PHP": [mortgage['principal'], mortgage['down_payment'], closing['total_closing_costs']],
            "Percentage": [
                (mortgage['principal'] / (predicted_price + closing['total_closing_costs'])) * 100,
                (mortgage['down_payment'] / (predicted_price + closing['total_closing_costs'])) * 100,
                (closing['total_closing_costs'] / (predicted_price + closing['total_closing_costs'])) * 100
            ]
        })

        alloc_chart = alt.Chart(alloc_df).mark_bar(cornerRadius=6, height=28).encode(
            x=alt.X("Amount_PHP:Q", title="Total Capital (PHP)", axis=alt.Axis(format="~s")),
            y=alt.Y("Component:N", sort=["Loan Principal", "Down Payment", "Closing Fees (Taxes/LRA)"], title=None),
            color=alt.Color("Component:N", scale=alt.Scale(
                domain=["Loan Principal", "Down Payment", "Closing Fees (Taxes/LRA)"],
                range=["#38bdf8", "#34d399", "#c084fc"]
            ), legend=None),
            tooltip=[
                alt.Tooltip("Component:N"),
                alt.Tooltip("Amount_PHP:Q", title="Amount (PHP)", format=",.2f"),
                alt.Tooltip("Percentage:Q", title="Share (%)", format=".1f")
            ]
        ).properties(height=140)

        st.altair_chart(alloc_chart, use_container_width=True)

    else:
        st.info("Please enter valid property parameters above to view retail financing calculations.")

    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: RANDOM FOREST INSIGHTS & FEATURE IMPORTANCE ---
with tab_model:
    st.markdown("""
    <div class="calc-card">
        <div class="card-title">🌲 Random Forest Regressor Interpretability</div>
        <p style="color: #94a3b8; font-size: 0.95rem;">
            Our top-performing model is an ensemble <strong>Random Forest Regressor</strong> trained on log-transformed prices. Below is the empirical feature importance distribution derived from the trained trees.
        </p>
    """, unsafe_allow_html=True)

    rf_features = ['Location', 'Floor_area (sqm)', 'Land_area (sqm)', 'Longitude', 'Latitude', 'Bath', 'Bedrooms']
    rf_importances = getattr(model, 'feature_importances_', [0.6206, 0.2478, 0.0774, 0.0252, 0.0139, 0.0100, 0.0052])
    
    # Clean feature names for presentation
    feature_labels = {
        'Location': 'Location (Target Encoded)',
        'Floor_area (sqm)': 'Floor Area (m²)',
        'Land_area (sqm)': 'Land Area (m²)',
        'Longitude': 'Longitude (°E Coordinates)',
        'Latitude': 'Latitude (°N Coordinates)',
        'Bath': 'Bathrooms Count',
        'Bedrooms': 'Bedrooms Count'
    }

    imp_df = pd.DataFrame({
        "Feature": [feature_labels.get(f, f) for f in rf_features],
        "Importance": [float(val) * 100 for val in rf_importances]
    }).sort_values("Importance", ascending=False)

    imp_chart = alt.Chart(imp_df).mark_bar(cornerRadius=6, height=24).encode(
        x=alt.X("Importance:Q", title="Model Gini Feature Importance (%)", scale=alt.Scale(domain=[0, 70])),
        y=alt.Y("Feature:N", sort='-x', title=None),
        color=alt.Color("Importance:Q", scale=alt.Scale(scheme='tealblues'), legend=None),
        tooltip=[
            alt.Tooltip("Feature:N"),
            alt.Tooltip("Importance:Q", title="Importance (%)", format=".2f")
        ]
    ).properties(height=260)

    st.altair_chart(imp_chart, use_container_width=True)

    m_c1, m_c2, m_c3 = st.columns(3)
    with m_c1:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 14px; border-radius: 10px; border: 1px solid rgba(148, 163, 184, 0.1);">
            <div style="font-weight: 700; color: #38bdf8; font-size: 0.95rem;">📍 Geographic Dominance (62.1%)</div>
            <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">
                Location accounts for over 62% of price variance, confirming the real estate adage <em>"Location, Location, Location"</em>. Smoothed Target Encoding captured micro-market premiums effectively.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with m_c2:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 14px; border-radius: 10px; border: 1px solid rgba(148, 163, 184, 0.1);">
            <div style="font-weight: 700; color: #34d399; font-size: 0.95rem;">📐 Structural Area (32.5%)</div>
            <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">
                Floor Area (24.8%) is the single strongest structural predictor, followed by Land Area (7.7%). Combined with location, structural volume accounts for >94% of total predictive power.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with m_c3:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 14px; border-radius: 10px; border: 1px solid rgba(148, 163, 184, 0.1);">
            <div style="font-weight: 700; color: #c084fc; font-size: 0.95rem;">🎯 Strict Non-Overfitting Design</div>
            <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">
                Ensemble bagging with 5-fold cross-validation prevents single-tree leaf memorization, delivering superior generalization compared to simple Decision Trees and OLS Linear Regression.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: GEOSPATIAL & NEIGHBORHOOD BENCHMARK ---
with tab_geo:
    st.markdown("""
    <div class="calc-card">
        <div class="card-title">🗺️ Interactive Geospatial Mapping & Neighborhood Benchmark</div>
        <p style="color: #94a3b8; font-size: 0.95rem;">
            Explore the spatial coordinate positioning of the property alongside historical listings in <strong>{0}</strong>.
        </p>
    """.format(selected_location), unsafe_allow_html=True)

    # Filter neighborhood listings
    nbr_df = df_listings[df_listings['Location'] == selected_location].copy()
    if nbr_df.empty or len(nbr_df) < 2:
        # Fallback to broader nearby dataset points if single listing
        nbr_df = df_listings.dropna(subset=['Latitude', 'Longitude']).head(50).copy()

    # Create Pydeck Map
    current_point = pd.DataFrame({
        'lat': [latitude],
        'lon': [longitude],
        'tooltip': [f"Current Property: {format_price(predicted_price)}"]
    })

    # Surrounding listings layer
    surround_layer = pdk.Layer(
        "ScatterplotLayer",
        data=nbr_df.dropna(subset=['Latitude', 'Longitude']),
        get_position=["Longitude", "Latitude"],
        get_color=[56, 189, 248, 160],  # Cyan
        get_radius=200,
        pickable=True,
    )

    # Current focal point layer (bright glowing emerald)
    focal_layer = pdk.Layer(
        "ScatterplotLayer",
        data=current_point,
        get_position=["lon", "lat"],
        get_color=[16, 185, 129, 255],  # Emerald
        get_radius=350,
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=latitude,
        longitude=longitude,
        zoom=12,
        pitch=25,
    )

    st.pydeck_chart(
        pdk.Deck(
            layers=[surround_layer, focal_layer],
            initial_view_state=view_state,
            tooltip={"text": "{tooltip}"},
            map_style="mapbox://styles/mapbox/dark-v11"
        ),
        use_container_width=True
    )

    # Location distribution benchmark
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown(f"##### 📊 Price Benchmark Distribution in `{selected_location}`")

    loc_data = df_listings[df_listings['Location'] == selected_location]['Price (PHP)'].dropna()
    if len(loc_data) > 0:
        b_c1, b_c2, b_c3, b_c4 = st.columns(4)
        with b_c1:
            st.metric("Total Listings in Location", f"{len(loc_data)} listings")
        with b_c2:
            st.metric("Locality Lowest Price", format_price(loc_data.min()))
        with b_c3:
            st.metric("Locality Median Price", format_price(loc_data.median()))
        with b_c4:
            st.metric("Locality Highest Price", format_price(loc_data.max()))

        # Benchmark comparison bar
        comp_df = pd.DataFrame({
            "Metric": ["Neighborhood Minimum", "Neighborhood Median", "Current Valuation", "Neighborhood Maximum"],
            "Price_PHP": [loc_data.min(), loc_data.median(), predicted_price, loc_data.max()],
            "Category": ["Benchmark", "Benchmark", "Current Estimate", "Benchmark"]
        })

        comp_chart = alt.Chart(comp_df).mark_bar(cornerRadius=6, height=26).encode(
            x=alt.X("Price_PHP:Q", title="Price in Philippine Peso (PHP)", axis=alt.Axis(format="~s")),
            y=alt.Y("Metric:N", sort=["Neighborhood Minimum", "Neighborhood Median", "Current Valuation", "Neighborhood Maximum"], title=None),
            color=alt.Color("Category:N", scale=alt.Scale(
                domain=["Benchmark", "Current Estimate"],
                range=["#64748b", "#10b981"]
            ), legend=None),
            tooltip=[
                alt.Tooltip("Metric:N"),
                alt.Tooltip("Price_PHP:Q", title="Price (PHP)", format=",.2f")
            ]
        ).properties(height=180)

        st.altair_chart(comp_chart, use_container_width=True)
    else:
        st.info("Sparse listing density for this specific barangay; general regional coordinates utilized.")

    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 4: ACADEMIC METHODOLOGY & SPECS ---
with tab_specs:
    st.markdown("""
    <div class="calc-card">
        <div class="card-title">📋 Academic Project & Research Methodology Specifications</div>
        <div style="font-size: 0.95rem; color: #cbd5e1; line-height: 1.7;">
            <p><strong>Course & Section:</strong> CCMACLRL - COM243ML (Machine Learning)</p>
            <p><strong>Course Instructor:</strong> Professor Ken Oliver Caparros</p>
            <p><strong>Group Name:</strong> GROUP3</p>
            <p><strong>Project Title:</strong> Property Retail Calculator - Residential Real Estate Price Estimation Using Structure And Geographic Variables</p>
            <hr style="border-color: rgba(255, 255, 255, 0.1); margin: 15px 0;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-top: 15px;">
                <div style="background: rgba(30, 41, 59, 0.5); padding: 12px; border-radius: 8px;">
                    <span style="color: #38bdf8; font-weight: 600;">Ezekiel Christian Alcantara</span><br>
                    <span style="color: #94a3b8; font-size: 0.85rem;">Pipeline & Feature Engineering</span>
                </div>
                <div style="background: rgba(30, 41, 59, 0.5); padding: 12px; border-radius: 8px;">
                    <span style="color: #38bdf8; font-weight: 600;">Genesis Navarro</span><br>
                    <span style="color: #94a3b8; font-size: 0.85rem;">EDA & Statistical Analysis</span>
                </div>
                <div style="background: rgba(30, 41, 59, 0.5); padding: 12px; border-radius: 8px;">
                    <span style="color: #38bdf8; font-weight: 600;">Christian Jacob Suntay</span><br>
                    <span style="color: #94a3b8; font-size: 0.85rem;">Model Training & 5-Fold CV</span>
                </div>
                <div style="background: rgba(30, 41, 59, 0.5); padding: 12px; border-radius: 8px;">
                    <span style="color: #38bdf8; font-weight: 600;">Jay Arre Talosig</span><br>
                    <span style="color: #94a3b8; font-size: 0.85rem;">Deployment & UI Architecture</span>
                </div>
            </div>
            <hr style="border-color: rgba(255, 255, 255, 0.1); margin: 15px 0;">
            <p style="font-size: 0.88rem; color: #94a3b8;">
                <strong>Experimental Protocol:</strong> In accordance with course guidelines prohibiting deep learning and AutoML, three traditional models (Linear Regression, Decision Tree Regressor, and Random Forest Regressor) were compared under strictly identical train/test splits (80/20) and 5-Fold cross-validation. Preprocessing transformers were fit strictly on the training partition to eliminate data leakage.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; margin-top: 2rem; padding-bottom: 2rem;">
    Property Retail Calculator • GROUP3 Final Project • National University • Instructor: Prof. Ken Oliver Caparros
</div>
""", unsafe_allow_html=True)
