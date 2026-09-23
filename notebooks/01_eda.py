# %% [markdown]
# # Phase 2: Exploratory Data Analysis (EDA)
# 
# This notebook fulfills the Exploratory Data Analysis requirements for the GROUP3 Philippine Real Estate Price Prediction project.
# We will examine data quality, handle anomalies, analyze distributions and relationships, and provide a summary of findings that informs preprocessing.

# %%
# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('ggplot')
sns.set_palette('deep')

# %% [markdown]
# ## 1. Data Loading and Initial Inspection

# %%
# Load the dataset
# Using relative path from notebooks/ to data/original/
data_path = '../data/original/PH_houses_v2.csv'
df_raw = pd.read_csv(data_path)

# Display dataset dimensions and basic info
print(f"Dataset Dimensions: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns\n")

print("Data Types:")
print(df_raw.dtypes)

# %%
# Display the first few rows
df_raw.head()

# %% [markdown]
# **Finding 1.1:** The dataset contains 1,500 records and 10 columns. All columns, except `Longitude`, are currently stored as `object` (strings). The `Price (PHP)` column contains commas, and missing values are represented as the string `"na"`.

# %% [markdown]
# ## 2. Data Quality & Missing Values
# 
# First, we need to convert the `"na"` strings into actual `NaN` values to properly assess missingness.

# %%
# Replace 'na' string with actual numpy NaN
df = df_raw.replace('na', np.nan)

# Check for missing values
missing_counts = df.isnull().sum()
print("Missing Value Counts:")
print(missing_counts[missing_counts > 0])

# Check for duplicates
duplicate_count = df.duplicated().sum()
print(f"\nNumber of duplicate rows: {duplicate_count}")

# %% [markdown]
# **Finding 2.1:**
# * `Price (PHP)` is missing 40 records. Since this is our target variable, we will need to drop these rows during preprocessing.
# * `Land_area (sqm)` is missing 1,171 records (78% of the data). This is severe missingness, likely because many properties are condos which don't have individual land areas.
# * `Bath` (633), `Bedrooms` (120), and `Floor_area (sqm)` (58) also have missing values that will require imputation (e.g., using medians).
# * There are no exact duplicate rows.

# %% [markdown]
# ## 3. Data Type Conversion
# 
# Let's convert our numeric features and target into proper numeric data types.

# %%
# Clean Price: remove commas and convert to float
if df['Price (PHP)'].dtype == object:
    df['Price (PHP)'] = df['Price (PHP)'].str.replace(',', '').astype(float)

# Convert other features to numeric
numeric_cols = ['Bedrooms', 'Bath', 'Floor_area (sqm)', 'Land_area (sqm)', 'Latitude']
for col in numeric_cols:
    if df[col].dtype == object:
        df[col] = pd.to_numeric(df[col], errors='coerce')

print("\nUpdated Data Types:")
print(df.dtypes)

# %%
# Summary statistics for numerical columns
df.describe().T

# %% [markdown]
# **Finding 3.1:** 
# * `Price (PHP)` ranges from incredibly low to extremely high values (max is 120M PHP). 
# * `Floor_area` and `Land_area` have minimum values of 0 or near 0, which might be errors or placeholders, requiring treatment.

# %% [markdown]
# ## 4. Univariate Distributions

# %%
# Visualization 1: Target Variable (Price) Distribution
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# Original Price
sns.histplot(df['Price (PHP)'].dropna(), kde=True, ax=ax1)
ax1.set_title('Distribution of Price (PHP)')
ax1.set_xlabel('Price (PHP)')

# Log-transformed Price
sns.histplot(np.log1p(df['Price (PHP)'].dropna()), kde=True, ax=ax2, color='green')
ax2.set_title('Distribution of Log(Price)')
ax2.set_xlabel('Log(Price (PHP))')

plt.tight_layout()
plt.show()

# %% [markdown]
# **Finding 4.1 (Visualization 1):** The original `Price` distribution is severely right-skewed. The log-transformation of `Price` results in a much more normal distribution. For modeling, predicting `Log(Price)` will likely yield better results for linear models and reduce the impact of extreme values.

# %%
# Visualization 2: Structural Features Distributions
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

sns.countplot(data=df, x='Bedrooms', ax=axes[0,0], color='skyblue')
axes[0,0].set_title('Number of Bedrooms')
axes[0,0].tick_params(axis='x', rotation=45)

sns.countplot(data=df, x='Bath', ax=axes[0,1], color='salmon')
axes[0,1].set_title('Number of Bathrooms')
axes[0,1].tick_params(axis='x', rotation=45)

sns.histplot(df['Floor_area (sqm)'].dropna(), bins=50, kde=True, ax=axes[1,0], color='purple')
axes[1,0].set_title('Floor Area (sqm) Distribution')

sns.histplot(df['Land_area (sqm)'].dropna(), bins=50, kde=True, ax=axes[1,1], color='orange')
axes[1,1].set_title('Land Area (sqm) Distribution')

plt.tight_layout()
plt.show()

# %% [markdown]
# **Finding 4.2 (Visualization 2):** 
# * Most properties have 1-3 bedrooms and 1-2 bathrooms.
# * `Floor_area` is heavily skewed with a long tail of very large properties.
# * `Land_area` is also skewed but has very few data points (due to the 78% missing rate).

# %% [markdown]
# ## 5. Bivariate & Outlier Analysis

# %%
# Visualization 3: Floor Area vs. Price
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Floor_area (sqm)', y='Price (PHP)', alpha=0.5)
plt.title('Floor Area vs Price')
plt.xlabel('Floor Area (sqm)')
plt.ylabel('Price (PHP)')
# Add a regression line
sns.regplot(data=df, x='Floor_area (sqm)', y='Price (PHP)', scatter=False, color='red')
plt.show()

# %% [markdown]
# **Finding 5.1 (Visualization 3):** There is a clear positive correlation between `Floor_area` and `Price`, which is expected. However, the variance in price increases significantly as floor area increases (heteroscedasticity). There are also some extreme outliers (e.g., floor area > 3000 sqm or prices > 100M). We may need to clip luxury outliers (>100M) to preserve main-market model calibration.

# %%
# Visualization 4: Correlation Matrix
plt.figure(figsize=(8, 6))
correlation_matrix = df[['Price (PHP)', 'Bedrooms', 'Bath', 'Floor_area (sqm)', 'Land_area (sqm)']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f')
plt.title('Correlation Matrix of Numerical Features')
plt.show()

# %% [markdown]
# **Finding 5.2 (Visualization 4):** 
# * `Bath` and `Floor_area` have the strongest positive correlations with `Price` (~0.62 and ~0.43 respectively). 
# * `Bedrooms` and `Bath` are highly correlated with each other (0.75), which makes sense. 
# * These relationships confirm that structural features are strong predictors for our models.

# %% [markdown]
# ## 6. Geospatial & Location Analysis

# %%
# Check unique locations
print(f"Number of unique locations: {df['Location'].nunique()}")
print("\nTop 10 Locations by Count:")
print(df['Location'].value_counts().head(10))

# %%
# Visualization 5: Geographic Distribution of Prices
plt.figure(figsize=(10, 8))
# We use log price for coloring to reduce the effect of extreme luxury properties
scatter = plt.scatter(df['Longitude'], df['Latitude'], 
            c=np.log1p(df['Price (PHP)']), 
            cmap='viridis', alpha=0.6, s=20)
plt.colorbar(scatter, label='Log(Price)')
plt.title('Geographic Distribution of Property Prices')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

# %% [markdown]
# **Finding 6.1 (Visualization 5):** The dataset is heavily clustered in specific areas (likely Metro Manila and major urban hubs). The geospatial coordinates show distinct clusters of high-priced properties (yellow/green points). Location is clearly a critical feature. Since there are 113 unique locations, Target Encoding the `Location` string will likely be more effective than One-Hot Encoding to keep dimensionality manageable.

# %% [markdown]
# ## 7. EDA Findings & Preprocessing Strategy
# 
# Based on the exploratory analysis, the following preprocessing steps are required for our Machine Learning pipeline:
# 
# 1. **Target Variable:** Drop the 40 rows with missing `Price (PHP)`. We will log-transform `Price (PHP)` during training to handle the extreme right skew and improve regression performance.
# 2. **Missing Values:**
#    * `Land_area` is missing in 78% of rows. We can impute it with 0 (assuming condo/no land) or a median, or drop the column. We will impute with the median or 0 to keep the feature for houses.
#    * Impute `Bedrooms`, `Bath`, and `Floor_area` using the median.
# 3. **Outliers:** Clip extreme luxury prices (e.g., cap at ₱100M) and treat anomalous floor/land areas (e.g., negative or 0 values should be set to NaN and imputed).
# 4. **Feature Engineering:** 
#    * Apply Target Encoding to the `Location` feature to capture location value without creating 113 new dummy columns.
#    * Scale all numerical features (including coordinates) using `StandardScaler` to ensure algorithms like Random Forest and Linear Regression treat them uniformly.
