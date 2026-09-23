# Dataset Provenance: Philippine Real Estate Price Prediction

* **Source Name:** Philippine Real Estate Dataset
* **Original Author:** Arlo Blanco
* **Source Platform:** Kaggle
* **Data Origin:** Scraped from Lamudi.com.ph (Lamudi Philippines) using BeautifulSoup
* **License:** CC0: Public Domain
* **Filename:** `PH_houses_v2.csv`
* **Size:** ~1,500 records

## Description
This dataset contains real estate property listings across the Philippines. The unit of analysis is individual residential properties (houses, condos, townhouses, etc.). Features include geographic coordinates, location details, structural features (bedrooms, bathrooms, floor area, land area), and the listing price in Philippine Peso (PHP).

## Data Dictionary
| Feature | Description | Data Type | Units |
| :--- | :--- | :--- | :--- |
| `Description` | Title/description of the property listing | String | N/A |
| `Location` | Barangay, City, and/or Province | String | N/A |
| `Price (PHP)` | Listing price of the property | String (Formatted with commas) | Philippine Peso (PHP) |
| `Bedrooms` | Number of bedrooms | String / Int | Count |
| `Bath` | Number of bathrooms | String / Int | Count |
| `Floor_area (sqm)`| Interior floor area of the property | String / Float | Square Meters (sqm) |
| `Land_area (sqm)` | Total lot/land area of the property | String / Float | Square Meters (sqm) |
| `Latitude` | Latitude coordinate of the property | Float | Decimal Degrees |
| `Longitude` | Longitude coordinate of the property | Float | Decimal Degrees |
| `Link` | Original Lamudi listing URL | String (URL) | N/A |
