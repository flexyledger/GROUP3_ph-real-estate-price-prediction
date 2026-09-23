# GROUP3_ph-real-estate-price-prediction

**Course & Section:** CCMACLRL - COM243ML   
**Course Instructor:** Professor Ken Oliver Caparros  
**Group Name:** GROUP3  
**Project Title:** Philippine Real Estate Property Valuation & Price Prediction Using Machine Learning  
<!-- **Deployed App URL:** [https://group3-ph-real-estate.streamlit.app](https://group3-ph-real-estate.streamlit.app) -->

---

## 📌 1. Project Overview & Objectives

This project develops an end-to-end Machine Learning pipeline and interactive web application to estimate property prices across the Philippines. Grounded in real estate data scraped from [Lamudi.com.ph](https://www.lamudi.com.ph) (`PH_houses_v2.csv`), the system provides data-driven valuation estimates to aid home buyers, property investors, and real estate analysts in making informed decisions.

### Key Objectives:
* **Exploratory Data Analysis (EDA):** Analyze spatial distributions, structural features (bedrooms, bathrooms, area), and price variance across Philippine regions.
* **Evidence-Based Model Comparison:** Train and evaluate **three distinct traditional machine learning algorithms** under strict fair experimental conditions (80/20 train-test split, 5-fold cross-validation).
* **Interactive Deployment:** Integrate the top-performing model into a functional Streamlit application that accepts user feature inputs and returns validated property price estimations.

---

## 🗂️ 2. Repository Directory Structure

The repository strictly follows the required course submission format (`GROUPNAME_PROJECTTITLE/`):

```text
GROUP3_ph-real-estate-price-prediction/
├── app/                        # Streamlit web application
│   ├── main.py                 # Application entry point & UI layout
│   └── utils.py                # Input validation & formatting helpers
├── data/                       # Dataset package
│   ├── original/               # Raw PH_houses_v2.csv & provenance note
│   └── processed/              # Cleaned dataset & feature engineered files
├── notebooks/                  # Interactive Jupyter Notebooks
│   ├── 01_eda.ipynb            # Exploratory Data Analysis & visualizations
│   ├── 02_preprocessing.ipynb  # Data cleaning, encoding, and scaling
│   └── 03_model_training.ipynb # 3-model comparison, CV & test set evaluation
├── src/                        # Reusable modular code
│   ├── preprocessing.py        # Data pipeline transformer
│   └── modeling.py             # Model training and evaluation logic
├── models/                     # Serialized model & pipeline outputs
│   ├── best_model.pkl          # Saved trained Random Forest Regressor model
│   └── preprocessor.pkl       # Saved feature transformation pipeline
├── documentation/              # Technical documentation & visuals
│   ├── user_guide.pdf          # Application user guide
│   └── screenshots/            # EDA plots and app UI screenshots
├── paper/                      # Final academic research paper
│   ├── GROUP3_Research_Paper.pdf
│   └── GROUP3_Research_Paper.docx
├── README.md                   # Technical setup and run instructions
└── requirements.txt            # Software dependencies
```

---

## 📊 3. Dataset Package & Provenance

* **Source:** Kaggle — *Philippine Real Estate* dataset by Arlo Blanco (scraped via BeautifulSoup from Lamudi Philippines).
* **License:** CC0: Public Domain
* **Unit of Analysis:** Individual residential property listings in the Philippines.
* **Records:** ~1,255 unique listings across various provinces and cities.

### Features & Data Dictionary

| Feature Variable | Data Type | Description | Units / Format |
| :--- | :--- | :--- | :--- |
| `Location` | Categorical | Barangay / City / Province location | Name string |
| `Bedrooms` | Numerical | Number of bedrooms | Count |
| `Bath` | Numerical | Number of bathrooms | Count |
| `Floor_area (sqm)`| Numerical | Total interior floor area | Square meters ($\text{m}^2$) |
| `Land_area (sqm)` | Numerical | Total land or lot area | Square meters ($\text{m}^2$) |
| `Latitude` | Numerical | Geographical latitude coordinate | Decimal degrees |
| `Longitude` | Numerical | Geographical longitude coordinate | Decimal degrees |
| `Price (PHP)` | Numerical (**Target**) | Listing price in Philippine Peso | PHP ($\text{₱}$) |

---

## ⚙️ 4. Machine Learning Methodology

### Permitted Algorithms Compared
In accordance with course guidelines prohibiting deep learning and AutoML, **three distinct traditional algorithms** were evaluated:

1. **Linear Regression (Baseline Parametric Model):** Establishes the linear benchmark for structural features against price.
2. **Decision Tree Regressor (Non-Linear Single Tree):** Captures non-linear relationships and feature interactions (e.g., location vs. floor area).
3. **Random Forest Regressor (Ensemble Method - Selected Model):** Reduces variance through bagging, handling geospatial coordinates and skewed real estate values effectively.

### Experimental Design & Fair Conditions
* **Data Split:** 80% Training Set / 20% Untouched Test Set (`random_state=42`).
* **Validation Strategy:** 5-Fold Cross-Validation evaluated strictly on the training set.
* **Primary Metric:** **Root Mean Squared Error (RMSE)** (penalizes large pricing errors on high-value properties).
* **Supporting Metrics:** Mean Absolute Error (MAE), Coefficient of Determination ($R^2$).

---

## 💻 5. Installation & Setup Instructions

Follow these step-by-step instructions to set up and run the repository locally.

### Prerequisites
* Python 3.10 or higher
* `git` CLI tool

### Step 1: Clone the Repository
```bash
git clone https://github.com/YourOrganization/GROUP3_ph-real-estate-price-prediction.git
cd GROUP3_ph-real-estate-price-prediction
```

### Step 2: Create and Activate a Virtual Environment
* **On macOS/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
* **On Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🚀 6. Running the Streamlit Application

To start the interactive web application locally:

```bash
streamlit run app/main.py
```

Upon execution, your default web browser will open to `http://localhost:8501`.

---

## 📱 7. Application Guide & User Input Validation

The Streamlit interface enables interactive property valuation through the following components:

1. **Property Feature Selection:** Users input location, floor area ($\text{m}^2$), land area ($\text{m}^2$), number of bedrooms, and bathrooms.
2. **Input Validation:**
   * Range bounds check (e.g., non-negative floor area, valid Philippine coordinate boundaries).
   * Missing value indicators handled safely without app crashing.
3. **Valuation Output:** Displays the predicted price in Philippine Pesos ($\text{₱}$) along with confidence ranges based on residual analysis.

---

## ⚠️ 8. Model Limitations & Troubleshooting

### Known Model Limitations
* **Geographic Coverage:** High density in Metro Manila and major urban hubs (e.g., Pasig, Makati, Davao, Cebu); performance may degrade in rural areas with sparse listings.
* **Outlier Sensitivity:** Extreme luxury estates exceeding $\text{₱}100\text{M}$ are clipped during preprocessing to preserve main-market model calibration.

### Common Troubleshooting Steps
* **`ModuleNotFoundError`:** Ensure your virtual environment is active (`source venv/bin/activate`) before running Streamlit.
* **File Path Errors:** Run commands from the root directory (`GROUP3_ph-real-estate-price-prediction/`) to ensure relative paths resolve correctly.

---

## 👥 9. Authorship & Project Declaration

This project was developed for the Machine Learning course under the instruction of **Professor Ken Oliver Caparros**. All student members of **GROUP3** jointly declare authorship and technical contribution in accordance with university academic integrity policies.

* **Course Instructor:** Professor Ken Oliver Caparros
* **Group Name:** GROUP3
* **Repository Ownership:** Jointly maintained by the National University of the Philippines and GROUP3 members.

### Team Members

| Profile Picture | Name |
| :---: | :--- |
| <img src="https://github.com/ghost.png" width="50" height="50" style="border-radius:50%"> | **Ezekiel Christian Alcantara** |
| <img src="https://github.com/ghost.png" width="50" height="50" style="border-radius:50%"> | **Genesis Navarro** |
| <img src="https://github.com/ghost.png" width="50" height="50" style="border-radius:50%"> | **Christian Jacob Suntay** |
| <img src="https://github.com/ghost.png" width="50" height="50" style="border-radius:50%"> | **Jay Arre Talosig** |

> **Note:** To display your actual GitHub profile pictures, edit the `README.md` and replace `ghost` in `https://github.com/ghost.png` with your actual GitHub usernames (e.g., `https://github.com/yourusername.png`).
