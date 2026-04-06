"""
Complete Data Analysis - Standalone Script
Runs all analysis steps and saves results
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import json

print("="*70)
print("HEALTHCARE RESOURCE FORECASTING - COMPLETE ANALYSIS")
print("="*70)

# Create output directories
Path('data/processed').mkdir(parents=True, exist_ok=True)
Path('outputs').mkdir(parents=True, exist_ok=True)

# ============================================================================
# 1. DATA INGESTION
# ============================================================================
print("\n[1/8] DATA INGESTION")
print("-" * 70)

# Load CA Hospital datasets
ca_dir = Path('Datasets/Ca')
patients = pd.read_csv(ca_dir / 'patients.csv')
encounters = pd.read_csv(ca_dir / 'encounters.csv')
procedures = pd.read_csv(ca_dir / 'procedures.csv')
providers = pd.read_csv(ca_dir / 'providers.csv')

print(f"✓ Patients: {len(patients):,} rows, {patients.shape[1]} columns")
print(f"✓ Encounters: {len(encounters):,} rows, {encounters.shape[1]} columns")
print(f"✓ Procedures: {len(procedures):,} rows, {procedures.shape[1]} columns")
print(f"✓ Providers: {len(providers):,} rows, {providers.shape[1]} columns")

# ============================================================================
# 2. DATA UNDERSTANDING
# ============================================================================
print("\n[2/8] DATA UNDERSTANDING")
print("-" * 70)

print("\n📊 Patients Dataset:")
print(f"  Columns: {list(patients.columns[:5])}...")
print(f"  Missing values: {patients.isnull().sum().sum()}")
print(f"  Unique patients: {patients[patients.columns[0]].nunique()}")

print("\n📊 Encounters Dataset:")
print(f"  Columns: {list(encounters.columns[:5])}...")
print(f"  Missing values: {encounters.isnull().sum().sum()}")
print(f"  Unique encounters: {len(encounters)}")

# ============================================================================
# 3. DATA CLEANING
# ============================================================================
print("\n[3/8] DATA CLEANING")
print("-" * 70)

# Clean encounters
encounters_clean = encounters.copy()
encounters_clean['visit_date'] = pd.to_datetime(encounters_clean['visit_date'], errors='coerce')
encounters_clean['discharge_date'] = pd.to_datetime(encounters_clean['discharge_date'], errors='coerce')

# Remove rows with invalid dates
before = len(encounters_clean)
encounters_clean = encounters_clean.dropna(subset=['visit_date'])
after = len(encounters_clean)
print(f"✓ Removed {before - after} rows with invalid dates")
print(f"✓ Clean encounters: {len(encounters_clean):,} rows")

# Date range
print(f"✓ Date range: {encounters_clean['visit_date'].min()} to {encounters_clean['visit_date'].max()}")

# ============================================================================
# 4. FEATURE ENGINEERING
# ============================================================================
print("\n[4/8] FEATURE ENGINEERING")
print("-" * 70)

# Calculate daily bed occupancy
daily_beds = encounters_clean.groupby(
    encounters_clean['visit_date'].dt.date
).size().reset_index()
daily_beds.columns = ['date', 'bed_count']
daily_beds['date'] = pd.to_datetime(daily_beds['date'])
daily_beds = daily_beds.sort_values('date')

print(f"✓ Daily bed occupancy calculated: {len(daily_beds)} days")
print(f"  Average: {daily_beds['bed_count'].mean():.2f} beds/day")
print(f"  Max: {daily_beds['bed_count'].max()} beds")
print(f"  Min: {daily_beds['bed_count'].min()} beds")

# Moving averages
daily_beds['MA_7'] = daily_beds['bed_count'].rolling(window=7, min_periods=1).mean()
daily_beds['MA_14'] = daily_beds['bed_count'].rolling(window=14, min_periods=1).mean()
print(f"✓ Added 7-day and 14-day moving averages")

# Time features
daily_beds['month'] = daily_beds['date'].dt.month
daily_beds['day_of_week'] = daily_beds['date'].dt.dayofweek
daily_beds['is_weekend'] = daily_beds['day_of_week'].isin([5, 6]).astype(int)
print(f"✓ Added time-based features")

# ICU ratio (using visit_type or admission_type)
if 'visit_type' in encounters_clean.columns:
    total = len(encounters_clean)
    icu_count = len(encounters_clean[
        encounters_clean['visit_type'].str.contains(
            'intensive|icu|emergency|critical', case=False, na=False
        )
    ])
    icu_ratio = icu_count / total
    print(f"✓ ICU/Emergency ratio: {icu_ratio:.2%} ({icu_count:,}/{total:,})")
elif 'admission_type' in encounters_clean.columns:
    total = len(encounters_clean)
    icu_count = len(encounters_clean[
        encounters_clean['admission_type'].str.contains(
            'intensive|icu|emergency|critical', case=False, na=False
        )
    ])
    icu_ratio = icu_count / total
    print(f"✓ ICU/Emergency ratio: {icu_ratio:.2%} ({icu_count:,}/{total:,})")
else:
    icu_ratio = 0
    print(f"✓ ICU ratio: Not available in dataset")

# ============================================================================
# 5. UNIVARIATE ANALYSIS
# ============================================================================
print("\n[5/8] UNIVARIATE ANALYSIS")
print("-" * 70)

print("\n📊 Bed Count Distribution:")
print(f"  Mean: {daily_beds['bed_count'].mean():.2f}")
print(f"  Median: {daily_beds['bed_count'].median():.2f}")
print(f"  Std Dev: {daily_beds['bed_count'].std():.2f}")
print(f"  Skewness: {daily_beds['bed_count'].skew():.2f}")
print(f"  Min: {daily_beds['bed_count'].min()}")
print(f"  Max: {daily_beds['bed_count'].max()}")
print(f"  Q1 (25%): {daily_beds['bed_count'].quantile(0.25):.2f}")
print(f"  Q3 (75%): {daily_beds['bed_count'].quantile(0.75):.2f}")

# ============================================================================
# 6. TIME SERIES ANALYSIS
# ============================================================================
print("\n[6/8] TIME SERIES ANALYSIS")
print("-" * 70)

# Monthly patterns
monthly_avg = daily_beds.groupby('month')['bed_count'].mean()
print("\n📅 Monthly Average Bed Occupancy:")
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
for month_num, avg in monthly_avg.items():
    month_name = months[month_num-1] if month_num <= 12 else f"Month {month_num}"
    print(f"  {month_name}: {avg:.2f} beds")

# Weekly patterns
weekly_avg = daily_beds.groupby('day_of_week')['bed_count'].mean()
print("\n📆 Day of Week Average:")
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
for day_num, avg in weekly_avg.items():
    print(f"  {days[day_num]}: {avg:.2f} beds")

# Trend analysis
from scipy import stats
x = np.arange(len(daily_beds))
y = daily_beds['bed_count'].values
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

print(f"\n📈 Trend Analysis:")
print(f"  Slope: {slope:.4f} beds/day")
print(f"  R-squared: {r_value**2:.4f}")
print(f"  P-value: {p_value:.4e}")
if slope > 0.01:
    print(f"  Trend: INCREASING")
elif slope < -0.01:
    print(f"  Trend: DECREASING")
else:
    print(f"  Trend: STABLE")

# ============================================================================
# 7. FORECASTING
# ============================================================================
print("\n[7/8] FORECASTING")
print("-" * 70)

# Moving average forecast (7-day)
last_7_days = daily_beds['bed_count'].tail(7).mean()
forecast_ma_7 = [last_7_days] * 7

print(f"\n📊 7-Day Moving Average Forecast:")
print(f"  Forecast: {last_7_days:.2f} beds/day (constant)")

# Trend-based forecast
last_x = len(daily_beds) - 1
forecast_trend = []
for i in range(1, 8):
    forecast_val = slope * (last_x + i) + intercept
    forecast_trend.append(forecast_val)

print(f"\n📈 7-Day Trend-Based Forecast:")
for i, val in enumerate(forecast_trend, 1):
    print(f"  Day +{i}: {val:.2f} beds")

# ============================================================================
# 8. ALERT SYSTEM
# ============================================================================
print("\n[8/8] ALERT SYSTEM")
print("-" * 70)

# Define thresholds (based on percentiles)
threshold_warning = daily_beds['bed_count'].quantile(0.75)
threshold_critical = daily_beds['bed_count'].quantile(0.90)

print(f"\n⚠️  Alert Thresholds:")
print(f"  Warning: {threshold_warning:.0f} beds (75th percentile)")
print(f"  Critical: {threshold_critical:.0f} beds (90th percentile)")

# Check current status
current_beds = daily_beds['bed_count'].iloc[-1]
print(f"\n📊 Current Status: {current_beds} beds")
if current_beds >= threshold_critical:
    print(f"  🔴 CRITICAL - Immediate action required!")
elif current_beds >= threshold_warning:
    print(f"  🟡 WARNING - Monitor closely")
else:
    print(f"  🟢 NORMAL - Within acceptable range")

# ============================================================================
# SAVE RESULTS
# ============================================================================
print("\n" + "="*70)
print("SAVING RESULTS")
print("="*70)

# Save processed data
daily_beds.to_csv('data/processed/daily_bed_occupancy.csv', index=False)
print(f"✓ Saved: data/processed/daily_bed_occupancy.csv")

# Save summary
summary = {
    'analysis_date': datetime.now().isoformat(),
    'data_summary': {
        'total_patients': int(len(patients)),
        'total_encounters': int(len(encounters)),
        'clean_encounters': int(len(encounters_clean)),
        'date_range_start': str(encounters_clean['visit_date'].min()),
        'date_range_end': str(encounters_clean['visit_date'].max()),
        'days_analyzed': int(len(daily_beds))
    },
    'bed_occupancy': {
        'avg_daily_beds': float(daily_beds['bed_count'].mean()),
        'median_daily_beds': float(daily_beds['bed_count'].median()),
        'max_daily_beds': int(daily_beds['bed_count'].max()),
        'min_daily_beds': int(daily_beds['bed_count'].min()),
        'std_dev': float(daily_beds['bed_count'].std())
    },
    'icu_metrics': {
        'icu_ratio': float(icu_ratio)
    },
    'trend_analysis': {
        'slope': float(slope),
        'r_squared': float(r_value**2),
        'trend_direction': 'INCREASING' if slope > 0.01 else 'DECREASING' if slope < -0.01 else 'STABLE'
    },
    'forecasts': {
        'ma_7day': float(last_7_days),
        'trend_7day': [float(x) for x in forecast_trend]
    },
    'alerts': {
        'warning_threshold': float(threshold_warning),
        'critical_threshold': float(threshold_critical),
        'current_beds': int(current_beds)
    }
}

with open('data/processed/analysis_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)
print(f"✓ Saved: data/processed/analysis_summary.json")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*70)
print("✓ ANALYSIS COMPLETE!")
print("="*70)

print(f"\n📊 Key Findings:")
print(f"  • Analyzed {len(patients):,} patients across {len(encounters_clean):,} encounters")
print(f"  • Date range: {(encounters_clean['visit_date'].max() - encounters_clean['visit_date'].min()).days} days")
print(f"  • Average daily bed demand: {daily_beds['bed_count'].mean():.0f} beds")
print(f"  • Peak demand: {daily_beds['bed_count'].max()} beds")
print(f"  • ICU/Emergency ratio: {icu_ratio:.1%}")
print(f"  • Trend: {summary['trend_analysis']['trend_direction']} ({slope:.4f} beds/day)")
print(f"  • 7-day MA forecast: {last_7_days:.0f} beds/day")

print(f"\n📁 Output Files:")
print(f"  • data/processed/daily_bed_occupancy.csv")
print(f"  • data/processed/analysis_summary.json")

print("\n" + "="*70)
