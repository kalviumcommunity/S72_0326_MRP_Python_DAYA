"""
Complete analysis pipeline - runs all milestones
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Import modules
from src.data_processing.ingest_data import main as load_data
from src.data_processing.clean_data import clean_dataset
from src.data_processing.feature_engineering import engineer_features

print("="*60)
print("HEALTHCARE RESOURCE FORECASTING - COMPLETE ANALYSIS")
print("="*60)

# Load data
print("\n[1/7] Loading datasets...")
data = load_data()

# Extract main datasets
patients = data['ca_hospital']['patients']
encounters = data['ca_hospital']['encounters']
procedures = data['ca_hospital']['procedures']
hospital_records = data['hospital_records']

print(f"\n✓ Loaded {len(patients)} patients")
print(f"✓ Loaded {len(encounters)} encounters")
print(f"✓ Loaded {len(procedures)} procedures")

# Data Understanding
print("\n[2/7] Data Understanding...")
print(f"\nPatients Dataset:")
print(f"  Shape: {patients.shape}")
print(f"  Columns: {list(patients.columns)}")
print(f"  Missing values: {patients.isnull().sum().sum()}")

print(f"\nEncounters Dataset:")
print(f"  Shape: {encounters.shape}")
print(f"  Date range: {encounters['START'].min()} to {encounters['START'].max()}")
print(f"  Missing values: {encounters.isnull().sum().sum()}")

# Data Cleaning
print("\n[3/7] Data Cleaning...")
encounters_clean = encounters.copy()
encounters_clean['START'] = pd.to_datetime(encounters_clean['START'])
encounters_clean['STOP'] = pd.to_datetime(encounters_clean['STOP'])
print(f"✓ Cleaned encounters: {len(encounters_clean)} rows")

# Feature Engineering
print("\n[4/7] Feature Engineering...")

# Calculate daily bed occupancy
daily_beds = encounters_clean.groupby(
    encounters_clean['START'].dt.date
).size().reset_index()
daily_beds.columns = ['date', 'bed_count']
daily_beds['date'] = pd.to_datetime(daily_beds['date'])

# Calculate moving averages
daily_beds['MA_7'] = daily_beds['bed_count'].rolling(window=7).mean()
daily_beds['MA_14'] = daily_beds['bed_count'].rolling(window=14).mean()

print(f"✓ Created daily bed occupancy: {len(daily_beds)} days")
print(f"  Average daily beds: {daily_beds['bed_count'].mean():.2f}")
print(f"  Max daily beds: {daily_beds['bed_count'].max()}")
print(f"  Min daily beds: {daily_beds['bed_count'].min()}")

# ICU ratio
if 'ENCOUNTERCLASS' in encounters_clean.columns:
    total_encounters = len(encounters_clean)
    icu_encounters = len(encounters_clean[
        encounters_clean['ENCOUNTERCLASS'].str.contains(
            'intensive|icu|emergency', case=False, na=False
        )
    ])
    icu_ratio = icu_encounters / total_encounters
    print(f"\n✓ ICU/Emergency ratio: {icu_ratio:.2%}")

# Univariate Analysis
print("\n[5/7] Univariate Analysis...")
print(f"\nBed Count Statistics:")
print(f"  Mean: {daily_beds['bed_count'].mean():.2f}")
print(f"  Median: {daily_beds['bed_count'].median():.2f}")
print(f"  Std Dev: {daily_beds['bed_count'].std():.2f}")
print(f"  Skewness: {daily_beds['bed_count'].skew():.2f}")

# Time Series Analysis
print("\n[6/7] Time Series Analysis...")
daily_beds['month'] = daily_beds['date'].dt.month
monthly_avg = daily_beds.groupby('month')['bed_count'].mean()
print(f"\nMonthly Average Bed Occupancy:")
for month, avg in monthly_avg.items():
    print(f"  Month {month}: {avg:.2f} beds")

# Forecasting
print("\n[7/7] Forecasting...")
# Simple moving average forecast
last_7_days = daily_beds['bed_count'].tail(7).mean()
forecast_7day = [last_7_days] * 7
print(f"\n7-day forecast (MA): {last_7_days:.2f} beds/day")

# Trend forecast
from scipy import stats
x = np.arange(len(daily_beds))
y = daily_beds['bed_count'].values
slope, intercept, r_value, _, _ = stats.linregress(x, y)
print(f"\nTrend Analysis:")
print(f"  Slope: {slope:.4f} beds/day")
print(f"  R-squared: {r_value**2:.4f}")
if slope > 0:
    print(f"  Trend: INCREASING")
else:
    print(f"  Trend: DECREASING")

# Save processed data
print("\n" + "="*60)
print("SAVING RESULTS")
print("="*60)

output_dir = Path('data/processed')
output_dir.mkdir(parents=True, exist_ok=True)

daily_beds.to_csv(output_dir / 'daily_bed_occupancy.csv', index=False)
print(f"✓ Saved: data/processed/daily_bed_occupancy.csv")

# Create summary report
summary = {
    'total_patients': len(patients),
    'total_encounters': len(encounters),
    'date_range_start': str(encounters_clean['START'].min()),
    'date_range_end': str(encounters_clean['START'].max()),
    'avg_daily_beds': float(daily_beds['bed_count'].mean()),
    'max_daily_beds': int(daily_beds['bed_count'].max()),
    'icu_ratio': float(icu_ratio) if 'icu_ratio' in locals() else 0,
    'trend_slope': float(slope),
    'forecast_7day': float(last_7_days)
}

import json
with open(output_dir / 'analysis_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)
print(f"✓ Saved: data/processed/analysis_summary.json")

print("\n" + "="*60)
print("✓ ANALYSIS COMPLETE!")
print("="*60)
print(f"\nKey Findings:")
print(f"  • Analyzed {len(patients):,} patients")
print(f"  • Processed {len(encounters):,} encounters")
print(f"  • Average daily bed demand: {daily_beds['bed_count'].mean():.0f} beds")
print(f"  • Trend: {'INCREASING' if slope > 0 else 'DECREASING'} ({slope:.4f} beds/day)")
print(f"  • 7-day forecast: {last_7_days:.0f} beds/day")
