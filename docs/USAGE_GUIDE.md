# Usage Guide

## Getting Started

### Installation
```bash
# Clone repository
git clone https://github.com/kalviumcommunity/S72_0326_MRP_Python_DAYA.git
cd S72_0326_MRP_Python_DAYA

# Install dependencies
pip install -r requirements.txt
```

### Running the Pipeline

#### 1. Data Ingestion
```bash
python src/data_processing/ingest_data.py
```

#### 2. Data Cleaning
```python
from src.data_processing.clean_data import clean_dataset
from src.data_processing.ingest_data import main as load_data

data = load_data()
clean_encounters = clean_dataset(
    data['ca_hospital']['encounters'],
    name='Encounters',
    date_cols=['START', 'STOP']
)
```

#### 3. Feature Engineering
```python
from src.data_processing.feature_engineering import engineer_features

features = engineer_features(data['ca_hospital'])
```

#### 4. Analysis
```python
from src.analysis.univariate import analyze_numeric_variable
from src.analysis.time_series import analyze_trend

# Univariate analysis
analyze_numeric_variable(encounters, 'TOTAL_CLAIM_COST')

# Time series analysis
analyze_trend(encounters, 'START', 'bed_count')
```

#### 5. Forecasting
```python
from src.forecasting.moving_average import forecast_bed_demand
from src.forecasting.trend_forecast import forecast_resource_demand

# Moving average forecast
daily_beds, forecast = forecast_bed_demand(encounters, forecast_days=7)

# Trend-based forecast
trend_forecast = forecast_resource_demand(daily_beds, 'bed_count')
```

#### 6. Alerts
```python
from src.forecasting.alert_system import ResourceAlertSystem

alert_system = ResourceAlertSystem()
alert_system.check_bed_occupancy(current_occupancy=450, capacity=500)
alert_system.generate_report()
```

#### 7. Visualization
```python
from src.visualization.dashboard import HealthcareDashboard

dashboard = HealthcareDashboard()
dashboard.plot_bed_occupancy_trend(daily_beds, 'date', 'bed_count')
dashboard.plot_forecast_comparison(actual, forecast)
```

## Module Reference

### data_processing
- `ingest_data.py` - Load datasets
- `clean_data.py` - Data cleaning utilities
- `feature_engineering.py` - Feature creation
- `config.py` - Configuration settings

### analysis
- `data_understanding.py` - Dataset exploration
- `univariate.py` - Single variable analysis
- `bivariate.py` - Relationship analysis
- `time_series.py` - Temporal analysis
- `correlation.py` - Correlation matrices

### forecasting
- `moving_average.py` - MA forecasting
- `trend_forecast.py` - Trend extrapolation
- `alert_system.py` - Alert generation

### visualization
- `dashboard.py` - Dashboard creation

## Tips & Best Practices

1. **Always check data quality first**
2. **Use appropriate time windows for MA**
3. **Validate forecasts against holdout data**
4. **Tune alert thresholds based on hospital capacity**
5. **Save visualizations for reporting**
