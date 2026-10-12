# Deployment Guide — Property Retail Calculator

This repository is fully configured for deployment:
1. **Frontend:** Optimized for **Netlify** (Global CDN, fast loading, responsive on mobile and desktop).
2. **Backend ML API:** Configured for **Render**, **Railway**, or **Koyeb** via FastAPI (`app/api.py`).
3. **Interactive Streamlit App:** Configured for **Streamlit Community Cloud** (`app/main.py`).

---

## 🚀 Option 1: Deploying the Frontend to Netlify

Netlify hosts the static frontend files located in the `frontend/` directory. The repository includes `netlify.toml` which automatically points Netlify to `publish = "frontend"`.

### Method A: Deploy via GitHub (Continuous Deployment - Recommended)
1. Commit and push your changes to GitHub:
   ```bash
   git add .
   git commit -m "feat: setup Netlify deployment"
   git push origin main
   ```
2. Go to [Netlify Dashboard](https://app.netlify.com/).
3. Click **"Add new site"** &rarr; **"Import an existing project"**.
4. Select **GitHub** and pick the repository `flexyledger/GROUP3_ph-real-estate-price-prediction`.
5. Netlify will automatically detect `netlify.toml`:
   - **Publish directory:** `frontend`
   - **Build command:** *(leave empty)*
6. Click **"Deploy site"**.
7. Your site will be live at `https://<your-site-name>.netlify.app`!

### Method B: Deploy via Netlify Drop (Manual Drag-and-Drop)
1. Go to [Netlify Drop](https://app.netlify.com/drop).
2. Drag and drop the `frontend` folder directly from your file manager into the Netlify Drop area.
3. Your site is deployed instantly!

---

## ⚡ Option 2: Deploying the Machine Learning Backend (Optional)

The frontend works out-of-the-box using the built-in client estimation engine and `frontend/data/locations.json`. However, if you want live cloud inference using the serialized Random Forest model (`best_model.pkl`), deploy the backend API.

### Deploying to Render (Free Tier)
1. Log in to [Render](https://render.com/).
2. Click **"New +"** &rarr; **"Web Service"**.
3. Connect your GitHub repository `flexyledger/GROUP3_ph-real-estate-price-prediction`.
4. Configure:
   - **Environment:** `Python`
   - **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt uvicorn fastapi`
   - **Start Command:** `uvicorn app.api:app --host 0.0.0.0 --port $PORT`
5. Click **"Create Web Service"**.
6. Once deployed, copy your Render URL (e.g., `https://group3-ph-api.onrender.com`).
7. Open your Netlify site, click **"⚙️ Backend API Settings"**, paste the URL, and click **"Connect"**!

---

## 🎈 Option 3: Deploying Streamlit to Streamlit Community Cloud

If you also want the native Streamlit application live:
1. Visit [share.streamlit.io](https://share.streamlit.io).
2. Connect your GitHub account and choose `flexyledger/GROUP3_ph-real-estate-price-prediction`.
3. Set **Main file path** to `app/main.py`.
4. Click **"Deploy"**.

---

## 📁 Deployment File Summary
| File | Destination | Purpose |
| :--- | :--- | :--- |
| `netlify.toml` | Netlify | Tells Netlify to serve the `frontend/` directory and configures headers. |
| `frontend/` | Netlify | Complete static HTML/CSS/JS frontend with live Leaflet map and calculators. |
| `app/api.py` | Render / Railway | FastAPI backend serving `best_model.pkl` with CORS enabled. |
| `render.yaml` | Render | 1-Click configuration file for Render web services. |
| `Procfile` | Railway / Koyeb | Process specification for cloud container deployment. |
