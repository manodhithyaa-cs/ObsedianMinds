# 🌊 AquaScope – AI-Based Water Contamination Prediction Platform

### 🛰️ Predict. Prevent. Protect.

AquaScope is an AI-powered environmental intelligence platform that **predicts water contamination risks** using open **satellite imagery**, **weather data**, and **industrial activity records**.  
Instead of waiting for contamination to occur, AquaScope proactively identifies **“at-risk water bodies”** and visualizes them on a **dynamic risk heatmap**.

---

## 📖 Table of Contents
- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Our Solution](#-our-solution)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [ML Model Overview](#-ml-model-overview)
- [How to Run Locally](#-how-to-run-locally)
- [Demo Workflow](#-demo-workflow)
- [Patentable Innovation](#-patentable-innovation)
- [Future Scope](#-future-scope)
- [Team](#-team)
- [License](#-license)

---

## 🌍 Overview
Each year, millions of people are affected by polluted water sources. Traditional monitoring relies on **manual water sampling**, which is **time-consuming** and **reactive**.

**AquaScope** uses **AI + open data** to detect early signs of contamination and generate a **Water Contamination Risk Score (WCRS)** for each region.  
It empowers governments, NGOs, and environmental researchers to act **before** pollution spreads.

---

## 🚨 Problem Statement
Water contamination detection today:
- Requires physical sampling & lab tests.
- Offers results after contamination occurs.
- Is localized — not scalable or predictive.

There is **no intelligent platform** that integrates **real-time satellite, weather, and industrial data** to **forecast contamination risk** across large areas.

---

## 💡 Our Solution
**AquaScope** introduces a **Predictive Environmental Risk Scoring Algorithm** that:
1. Collects open **satellite imagery** (Sentinel-2, Landsat) to derive water quality indices.  
2. Merges **weather conditions** (rainfall, temperature, wind).  
3. Incorporates **industrial discharge proximity** and past contamination records.  
4. Predicts contamination probability using a trained **AI model**.  
5. Displays a **live risk heatmap** for authorities and researchers.

---

## ✨ Key Features
✅ **AI-Based Risk Prediction** – Predicts contamination before it occurs.  
✅ **Satellite + Weather Data Fusion** – Multi-modal analysis for accuracy.  
✅ **Environmental Risk Score (0–100)** – Quantified contamination likelihood.  
✅ **Interactive Dashboard** – Real-time risk visualization on a global map.  
✅ **Early Alert System** – Email or in-app alerts when a region hits high-risk threshold.

---

## 🧠 Tech Stack

| Layer | Tools / Libraries |
|-------|-------------------|
| **Frontend** | React.js, Tailwind CSS, Leaflet.js / Mapbox |
| **Backend** | Node.js / Express or Python Flask |
| **ML/AI** | Python (Scikit-learn, TensorFlow, Pandas, NumPy) |
| **Data Sources** | Sentinel Hub API, Google Earth Engine, OpenWeatherMap, NASA POWER |
| **Database** | PostgreSQL + PostGIS |
| **Hosting** | Render / Railway / Vercel |
| **Visualization** | Chart.js, GeoJSON, Mapbox Heatmaps |

---

## 🧩 System Architecture

+-------------------+
| Satellite Data | → NDWI, NDTI, Turbidity
+-------------------+
↓
+-------------------+
| Weather Data | → Rainfall, Temp, Wind
+-------------------+
↓
+-------------------+
| Industrial Records| → Geo-tagged factories
+-------------------+
↓
+---------------------------+
| Data Preprocessing |
| - Cleaning & merging |
| - Feature extraction |
+---------------------------+
↓
+---------------------------+
| ML Model (RF / XGBoost) |
| → Predict Risk Score |
+---------------------------+
↓
+---------------------------+
| Web Dashboard (React) |
| → Heatmap Visualization |
+---------------------------+


---

## 🤖 ML Model Overview

**Inputs:**
- NDWI (Normalized Difference Water Index)  
- NDTI (Normalized Difference Turbidity Index)  
- Rainfall, Temperature, Wind Speed  
- Industrial Density Index (distance to factories)

**Output:**
- `Water Contamination Risk Score (0–100)`

**Algorithms Tried:**
- Random Forest
- XGBoost
- LSTM (for time-series trend prediction)

**Evaluation Metrics:**
- Accuracy, MAE, RMSE, F1-Score

---

## ⚙️ How to Run Locally

```bash
# Clone the repo
git clone https://github.com/manodhithyaa-cs/ObsedianMinds.git
cd ObsedianMinds

# Backend setup
cd backend
pip install -r requirements.txt
python app.py

# Frontend setup
cd frontend
npm install
npm start
