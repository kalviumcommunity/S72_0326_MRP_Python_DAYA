"""
Milestone 9: Time Series Analysis
Analyze trends over time and identify seasonal patterns
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_time_series(data, date_col, value_col, title=None, save_path=None):
    """Plot time series data."""
    plt.figure(figsize=(14, 6))
    plt.plot(data[date_col], data[value_col], linewidth=2)
    plt.xlabel('Date')
    plt.ylabel(value_col)
    plt.title(title or f'{value_col} Over Time')
    plt.grid(alpha=0.3)
    plt.xticks(rotation=45)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def analyze_trend(data, date_col, value_col):
    """Analyze time series trend."""
    print(f"\n{'='*60}")
    print(f"TIME SERIES ANALYSIS: {value_col}")
    print(f"{'='*60}")
    
    # Ensure date column is datetime
    data[date_col] = pd.to_datetime(data[date_col])
    data = data.sort_values(date_col)
    
    # Basic statistics
    print(f"\n📊 Time Range:")
    print(f"  Start: {data[date_col].min()}")
    print(f"  End: {data[date_col].max()}")
    print(f"  Duration: {(data[date_col].max() - data[date_col].min()).days} days")
    
    # Trend analysis
    print(f"\n📈 Trend Statistics:")
    print(f"  Mean: {data[value_col].mean():.2f}")
    print(f"  Median: {data[value_col].median():.2f}")
    print(f"  Std Dev: {data[value_col].std():.2f}")
    
    # Growth rate
    first_value = data[value_col].iloc[0]
    last_value = data[value_col].iloc[-1]
    growth_rate = ((last_value - first_value) / first_value) * 100
    print(f"\n📊 Overall Growth: {growth_rate:.2f}%")
    
    return {
        'start_date': data[date_col].min(),
        'end_date': data[date_col].max(),
        'mean': data[value_col].mean(),
        'growth_rate': growth_rate
    }

def detect_seasonality(data, date_col, value_col):
    """Detect seasonal patterns."""
    print(f"\n🔍 Seasonality Detection:")
    
    data[date_col] = pd.to_datetime(data[date_col])
    data['month'] = data[date_col].dt.month
    data['day_of_week'] = data[date_col].dt.dayofweek
    
    # Monthly patterns
    monthly_avg = data.groupby('month')[value_col].mean()
    print(f"\n📅 Monthly Averages:")
    for month, avg in monthly_avg.items():
        print(f"  Month {month}: {avg:.2f}")
    
    # Weekly patterns
    weekly_avg = data.groupby('day_of_week')[value_col].mean()
    print(f"\n📆 Day of Week Averages:")
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    for day_num, avg in weekly_avg.items():
        print(f"  {days[day_num]}: {avg:.2f}")
    
    return {
        'monthly_avg': monthly_avg.to_dict(),
        'weekly_avg': weekly_avg.to_dict()
    }

def calculate_moving_average(data, value_col, window=7):
    """Calculate moving average."""
    data[f'{value_col}_MA{window}'] = data[value_col].rolling(
        window=window
    ).mean()
    print(f"\n✅ Added {window}-day moving average")
    return data
