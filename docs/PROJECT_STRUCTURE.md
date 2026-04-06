# Project Structure Documentation

## Directory Layout

```
healthcare-forecasting/
├── data/
│   ├── raw/              # Original datasets (gitignored)
│   ├── processed/        # Cleaned datasets
│   └── features/         # Engineered features
├── notebooks/            # Jupyter notebooks for analysis
├── src/
│   ├── data_processing/  # ETL scripts
│   ├── analysis/         # EDA modules
│   ├── forecasting/      # Prediction models
│   └── visualization/    # Plotting utilities
├── outputs/              # Generated charts and reports
├── docs/                 # Documentation
└── scripts/              # Helper scripts
```

## Module Descriptions

### data_processing
- `ingest_data.py` - Load raw datasets
- `clean_data.py` - Handle missing values, duplicates
- `feature_engineering.py` - Create derived features

### analysis
- EDA scripts for univariate, bivariate, time-series analysis

### forecasting
- Moving average models
- Trend-based forecasting
- Alert generation

### visualization
- Dashboard creation
- Chart utilities

## Setup Instructions

1. Install dependencies: `pip install -r requirements.txt`
2. Run data ingestion: `python src/data_processing/ingest_data.py`
3. Start Jupyter: `jupyter notebook`
