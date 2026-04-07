# Healthcare Resource Forecasting System - DAYA

**Created by Team MRP**

## 🎯 Project Overview
A comprehensive data science project focused on forecasting healthcare resource demand (hospital beds, ICU capacity, oxygen supply) using real-world hospital datasets from 2021-2025. This project demonstrates end-to-end data science workflow with interactive dashboards, predictive analytics, and actionable insights.

## 📊 Problem Statement
Healthcare facilities face critical challenges in resource allocation. This project aims to:
- Predict bed occupancy and demand trends
- Forecast ICU capacity requirements
- Estimate oxygen supply needs
- Generate early warning alerts for resource shortages

## 🗂️ Datasets Used
1. **CA Hospital Dataset (Q1 2025)** - Core hospital operations data
2. **ICU Patient Dataset (2025)** - Critical care records with clinical variables
3. **Hospital Patient Records (2021-2024)** - Multi-year time-series data

## 📈 Key Metrics
- Bed occupancy rate
- ICU utilization ratio
- Oxygen consumption per patient
- Patient inflow/outflow patterns
- Seasonal demand variations

## 🛠️ Tech Stack
- Python 3.x
- Pandas, NumPy
- Matplotlib, Seaborn
- Scikit-learn

## 📁 Project Structure
```
├── data/
│   ├── raw/              # Original datasets
│   ├── processed/        # Cleaned and transformed data
│   └── features/         # Engineered features
├── notebooks/            # Jupyter notebooks for analysis
├── src/                  # Python scripts
│   ├── data_processing/
│   ├── analysis/
│   ├── forecasting/
│   └── visualization/
├── outputs/              # Generated plots and reports
├── docs/                 # Documentation
└── README.md
```

## 🚀 Getting Started
```bash
# Clone the repository
git clone https://github.com/kalviumcommunity/S72_0326_MRP_Python_DAYA.git

# Install dependencies
pip install -r requirements.txt

# Run data ingestion
python src/data_processing/ingest_data.py
```

## 📝 Development Milestones
- [x] M1: Problem Framing
- [ ] M2: Project Setup
- [ ] M3: Data Collection
- [ ] M4: Data Understanding
- [ ] M5: Data Cleaning
- [ ] M6: Feature Engineering
- [ ] M7-10: Exploratory Analysis
- [ ] M11-12: Forecasting Models
- [ ] M13: Alert System
- [ ] M14: Visualization Dashboard
- [ ] M15: Documentation

## 👤 Author
DAYA - Kalvium Community Project

## 📄 License
MIT License
