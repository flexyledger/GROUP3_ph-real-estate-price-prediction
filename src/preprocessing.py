import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from category_encoders import TargetEncoder

def load_and_clean_data(filepath='../data/original/PH_houses_v2.csv'):
    """
    Loads raw CSV data, parses types, drops missing targets, and handles strings.
    """
    # Load dataset
    df = pd.read_csv(filepath)
    
    # Drop rows where target is missing
    df = df.replace('na', np.nan)
    df = df.dropna(subset=['Price (PHP)'])
    
    # Parse Price
    df['Price (PHP)'] = df['Price (PHP)'].astype(str).str.replace(',', '').astype(float)
        
    # Convert numeric columns
    numeric_cols = ['Bedrooms', 'Bath', 'Floor_area (sqm)', 'Land_area (sqm)', 'Latitude', 'Longitude']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Cap extreme outliers in Price (e.g. > 100M PHP) to 100M
    df.loc[df['Price (PHP)'] > 100000000, 'Price (PHP)'] = 100000000
    
    return df

def prepare_features(df):
    """
    Selects features and target variable.
    """
    # Use Log1p of price as target to handle skew
    y = np.log1p(df['Price (PHP)'])
    
    # Select features
    features = ['Location', 'Bedrooms', 'Bath', 'Floor_area (sqm)', 'Land_area (sqm)', 'Latitude', 'Longitude']
    X = df[features].copy()
    
    return X, y

def build_preprocessor():
    """
    Builds the scikit-learn ColumnTransformer pipeline for preprocessing.
    """
    numeric_features = ['Bedrooms', 'Bath', 'Floor_area (sqm)', 'Land_area (sqm)', 'Latitude', 'Longitude']
    categorical_features = ['Location']
    
    # Numeric Pipeline: Impute with median, then scale
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    # Categorical Pipeline: Target encoding (requires category_encoders package)
    # Using smoothing to handle rare locations
    categorical_transformer = Pipeline(steps=[
        ('target_encoder', TargetEncoder(smoothing=10))
    ])
    
    # Combine into a ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    return preprocessor
