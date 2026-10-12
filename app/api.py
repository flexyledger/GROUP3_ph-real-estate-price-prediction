from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
import joblib
import os

app = FastAPI(
    title="PH Real Estate Price Prediction ML API",
    description="Random Forest Regressor backend for Property Retail Calculator (GROUP3)",
    version="1.0.0"
)

# Enable CORS for Netlify frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and preprocessor
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '../models/best_model.pkl')
PREPROCESSOR_PATH = os.path.join(BASE_DIR, '../models/preprocessor.pkl')

try:
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    print("Model and preprocessor loaded successfully.")
except Exception as e:
    print(f"Warning: Failed to load model files: {e}")
    model = None
    preprocessor = None

class PropertyFeatures(BaseModel):
    location: str = Field(..., example="San Antonio, Pasig")
    bedrooms: float = Field(..., ge=1, le=20, example=3)
    bath: float = Field(..., ge=1, le=20, example=2)
    floor_area: float = Field(..., ge=5, le=5000, example=120)
    land_area: float = Field(..., ge=0, le=10000, example=150)
    latitude: float = Field(..., ge=4.5, le=21.5, example=14.588)
    longitude: float = Field(..., ge=116.0, le=127.0, example=121.060)

class PredictionResponse(BaseModel):
    status: str
    predicted_price_php: float
    confidence_lower_php: float
    confidence_upper_php: float
    formatted_price: str
    formatted_range: str

@app.get("/")
def root():
    return {
        "service": "Property Retail Calculator API",
        "team": "GROUP3",
        "course": "CCMACLRL - COM243ML",
        "status": "online",
        "endpoints": ["/predict", "/health"]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy" if model is not None else "degraded",
        "model_loaded": model is not None,
        "algorithm": "Random Forest Regressor"
    }

@app.post("/predict", response_model=PredictionResponse)
def predict_price(payload: PropertyFeatures):
    if model is None or preprocessor is None:
        raise HTTPException(status_code=500, detail="ML model is not loaded on the server.")

    input_df = pd.DataFrame({
        'Location': [payload.location],
        'Bedrooms': [payload.bedrooms],
        'Bath': [payload.bath],
        'Floor_area (sqm)': [payload.floor_area],
        'Land_area (sqm)': [payload.land_area],
        'Latitude': [payload.latitude],
        'Longitude': [payload.longitude]
    })

    try:
        X_trans = preprocessor.transform(input_df)
        log_pred = model.predict(X_trans)[0]
        price = float(np.expm1(log_pred))
        
        lower = price * 0.85
        upper = price * 1.15
        
        return PredictionResponse(
            status="success",
            predicted_price_php=round(price, 2),
            confidence_lower_php=round(lower, 2),
            confidence_upper_php=round(upper, 2),
            formatted_price=f"₱ {price:,.2f}",
            formatted_range=f"₱ {lower:,.2f} - ₱ {upper:,.2f}"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Inference error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
