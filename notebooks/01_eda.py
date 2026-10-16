# %% [markdown]
# # Phase 2: Exploratory Data Analysis (EDA)
# 
# This notebook fulfills the Exploratory Data Analysis requirements for the GROUP3 Philippine Real Estate Price Prediction project.
# We will examine data quality, handle anomalies, analyze distributions and relationships, and provide a summary of findings that informs preprocessing.

# %%
# Import necessary libraries
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('ggplot')
sns.set_palette('deep')
os.makedirs('../documentation/screenshots', exist_ok=True)

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
# **Finding 1.1:** The dataset contains 1,500 records and 10 columns. All columns, except `Longitude`, are initially stored as `object` (strings). The `Price (PHP)` column contains commas, and missing values are represented as the string `"na"`.

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

# Check for duplicates & unique identifier counts
duplicate_count = df.duplicated().sum()
print(f"\nNumber of exact duplicate rows: {duplicate_count}")
print(f"Unique Description count: {df['Description'].nunique()}")
print(f"Unique Listing Links: {df['Link'].nunique()}")

# %%
# Visualization: Missing Values per Column
missing_data = missing_counts[missing_counts > 0].sort_values(ascending=False)
missing_df = pd.DataFrame({
    'Feature': missing_data.index,
    'Missing Count': missing_data.values,
    'Percentage (%)': (missing_data.values / len(df)) * 100
})

plt.figure(figsize=(10, 5))
ax = sns.barplot(data=missing_df, x='Missing Count', y='Feature', palette='Reds_r')
plt.title('Missing Values per Column (Raw Dataset, N=1,500)', fontsize=14, fontweight='bold')
plt.xlabel('Count of Missing Records', fontsize=11)
plt.ylabel('Feature Column', fontsize=11)
for p in ax.patches:
    width = p.get_width()
    pct = (width / len(df)) * 100
    ax.annotate(f"{int(width):,} ({pct:.1f}%)", (width + 15, p.get_y() + p.get_height() / 2.),
                va='center', fontsize=10, fontweight='bold')
plt.xlim(0, 1400)
plt.tight_layout()
plt.savefig('../documentation/screenshots/eda_02_missing_values.png', dpi=300)
plt.show()

# %% [markdown]
# **Finding 2.1:**
# * `Price (PHP)` is missing 40 records. Since this is our target variable, we drop these rows during preprocessing, leaving 1,460 clean records.
# * `Land_area (sqm)` is missing 1,171 records (78.1% of the data). This is severe missingness, primarily because high-density condominium units lack individual lot titles.
# * `Bath` (633, 42.2%), `Bedrooms` (120, 8.0%), and `Floor_area (sqm)` (58, 3.9%) have missing values requiring median imputation.
# * **Dataset Size Provenance:** The raw data has 1,500 rows. There are 174 exact duplicate rows. The number of unique descriptions is exactly **1,255** (which is where the academic paper's cited "~1,255 listings" originates), while the final cleaned dataset has **1,460** rows.

# %% [markdown]
# ## 3. Data Type Conversion
# 
# Let's convert our numeric features and target into proper numeric data types.

# %%
# Clean Price: remove commas and convert to float
df['Price (PHP)'] = pd.to_numeric(df['Price (PHP)'].astype(str).str.replace(',', ''), errors='coerce')

# Convert other features to numeric
numeric_cols = ['Bedrooms', 'Bath', 'Floor_area (sqm)', 'Land_area (sqm)', 'Latitude', 'Longitude']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

print("\nUpdated Data Types:")
print(df.dtypes)

# %%
# Summary statistics for numerical columns
df.describe().T

# %% [markdown]
# **Finding 3.1:** 
# * `Price (PHP)` ranges from low starter homes to luxury estates (max 120M PHP). 
# * `Floor_area` and `Land_area` have minimum values near 0 requiring cleaning and median imputation.

# %% [markdown]
# ## 4. Univariate Distributions

# %%
# Visualization 1: Target Variable (Price) Distribution (Skew Analysis)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# Original Price
sns.histplot(df['Price (PHP)'].dropna(), kde=True, ax=ax1, color='#1f77b4')
ax1.set_title('Distribution of Price (PHP) - Severely Right-Skewed', fontsize=12, fontweight='bold')
ax1.set_xlabel('Price (PHP)')

# Log-transformed Price
sns.histplot(np.log1p(df['Price (PHP)'].dropna()), kde=True, ax=ax2, color='#2ca02c')
ax2.set_title('Distribution of Log(Price) - Bell-Shaped Normalization', fontsize=12, fontweight='bold')
ax2.set_xlabel('Log(Price (PHP))')

plt.tight_layout()
plt.savefig('../documentation/screenshots/eda_01_price_distribution.png', dpi=300)
plt.show()

# %% [markdown]
# **Finding 4.1 (Visualization 1):** The raw `Price` distribution exhibits severe positive right-skewness. The log-transformation `log1p(Price)` produces a normalized bell curve, which stabilizes variance for regression and prevents extreme luxury values from distorting gradients.

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
# * `Floor_area` is heavily skewed with a long tail of very large luxury properties.
# * `Land_area` has a heavy spike at 0/missing for condo units.

# %% [markdown]
# ## 5. Bivariate & Outlier Analysis

# %%
# Visualization 3: Floor Area vs. Price
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Floor_area (sqm)', y='Price (PHP)', alpha=0.5)
plt.title('Floor Area vs Price', fontsize=13, fontweight='bold')
plt.xlabel('Floor Area (sqm)')
plt.ylabel('Price (PHP)')
sns.regplot(data=df, x='Floor_area (sqm)', y='Price (PHP)', scatter=False, color='red')
plt.show()

# %% [markdown]
# **Finding 5.1 (Visualization 3):** There is a clear positive correlation between `Floor_area` and `Price`. The variance expands with floor size (heteroscedasticity). Capping extreme luxury prices at ₱100M preserves calibration for mainstream residential housing.

# %%
# Visualization 4: Correlation Matrix Heatmap
plt.figure(figsize=(8, 6))
correlation_matrix = df[['Price (PHP)', 'Bedrooms', 'Bath', 'Floor_area (sqm)', 'Land_area (sqm)', 'Latitude', 'Longitude']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f', linewidths=0.5)
plt.title('Correlation Matrix of Structural and Spatial Features', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('../documentation/screenshots/eda_03_correlation_heatmap.png', dpi=300)
plt.show()

# %% [markdown]
# **Finding 5.2 (Visualization 4):** 
# * `Floor_area` and `Bath` show the strongest positive linear correlations with `Price` (r ≈ 0.43 to 0.62). 
# * `Bedrooms` and `Bath` have strong multicollinearity (0.75), which tree-based ensemble models handle without degradation.

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
scatter = plt.scatter(df['Longitude'], df['Latitude'], 
            c=np.log1p(df['Price (PHP)']), 
            cmap='viridis', alpha=0.6, s=30, edgecolors='none')
cbar = plt.colorbar(scatter)
cbar.set_label('Log(Price in PHP)', fontsize=11)
plt.title('Spatial Distribution of Property Listings (Latitude vs Longitude)', fontsize=14, fontweight='bold')
plt.xlabel('Longitude (°E)', fontsize=11)
plt.ylabel('Latitude (°N)', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)

# Annotate key economic clusters
plt.annotate('Metro Manila\n(Major Density)', xy=(121.0, 14.6), xytext=(122.5, 16.0),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
             fontsize=10, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.5))
plt.annotate('Cebu City', xy=(123.9, 10.3), xytext=(125.0, 11.5),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
             fontsize=10, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.5))
plt.annotate('Davao City', xy=(125.6, 7.1), xytext=(126.8, 6.0),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
             fontsize=10, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.5))

plt.tight_layout()
plt.savefig('../documentation/screenshots/eda_04_spatial_scatter.png', dpi=300)
plt.show()

# %% [markdown]
# **Finding 6.1 (Visualization 5):** The dataset displays heavy spatial clustering around Metro Manila (National Capital Region), Cebu City, and Davao City. High-value clusters (yellow points) correlate strongly with urban hubs. Because there are 113 unique categorical location names, Target Encoding with empirical smoothing is required.

# %% [markdown]
# ## 7. EDA Findings & Preprocessing Strategy
# 
# Based on the exploratory analysis, the following preprocessing steps are required for our Machine Learning pipeline:
# 
# 1. **Target Variable:** Drop the 40 rows with missing `Price (PHP)`. Apply `log1p(Price)` transformation during training to normalize the right-skewed distribution.
# 2. **Missing Values:** Impute `Bedrooms`, `Bath`, `Floor_area`, and `Land_area` with medians.
# 3. **Outliers:** Cap extreme luxury prices at ₱100M to maintain calibration for mainstream buyers.
# 4. **Feature Engineering:** 
#    * Target encode the `Location` feature (smoothing factor = 10) to capture neighborhood premiums without adding 113 sparse dummy columns.
#    * Scale numerical features with `StandardScaler`.
#    * Fit all encoders strictly on the training partition to eliminate data leakage.
