"""
Milestone 12: Trend-Based Forecasting
Use trend extrapolation to estimate future resource demand
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def fit_linear_trend(data, value_col):
    """Fit linear trend to time series data."""
    print(f"\n{'='*60}")
    print(f"LINEAR TREND ANALYSIS - {value_col}")
    print(f"{'='*60}")
    
    # Create time index
    x = np.arange(len(data))
    y = data[value_col].values
    
    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    print(f"\n📈 Trend Line Equation:")
    print(f"  y = {slope:.4f}x + {intercept:.4f}")
    print(f"\n📊 Statistics:")
    print(f"  Slope: {slope:.4f} (daily change)")
    print(f"  R-squared: {r_value**2:.4f}")
    print(f"  P-value: {p_value:.4e}")
    
    if slope > 0:
        print(f"\n📈 Trend: INCREASING ({slope:.4f} per day)")
    elif slope < 0:
        print(f"\n📉 Trend: DECREASING ({slope:.4f} per day)")
    else:
        print(f"\n➡️  Trend: STABLE")
    
    return slope, intercept, r_value**2

def forecast_trend(data, value_col, periods=7):
    """Forecast using linear trend extrapolation."""
    print(f"\n🔮 Forecasting next {periods} periods...")
    
    # Fit trend
    x = np.arange(len(data))
    y = data[value_col].values
    slope, intercept, _, _, _ = stats.linregress(x, y)
    
    # Forecast
    future_x = np.arange(len(data), len(data) + periods)
    forecast = slope * future_x + intercept
    
    print(f"\n📊 Forecast Results:")
    for i, val in enumerate(forecast, 1):
        print(f"  Day +{i}: {val:.2f}")
    
    return forecast

def calculate_confidence_interval(data, value_col, forecast, confidence=0.95):
    """Calculate confidence intervals for forecast."""
    # Standard error
    residuals = data[value_col] - data[value_col].mean()
    std_error = np.std(residuals)
    
    # Z-score for confidence level
    from scipy.stats import norm
    z_score = norm.ppf((1 + confidence) / 2)
    
    # Confidence interval
    margin = z_score * std_error
    lower = forecast - margin
    upper = forecast + margin
    
    print(f"\n📊 {confidence*100}% Confidence Interval:")
    for i, (f, l, u) in enumerate(zip(forecast, lower, upper), 1):
        print(f"  Day +{i}: {f:.2f} [{l:.2f}, {u:.2f}]")
    
    return lower, upper

def plot_trend_forecast(data, date_col, value_col, forecast, save_path=None):
    """Plot trend and forecast."""
    plt.figure(figsize=(14, 6))
    
    # Actual data
    plt.plot(data[date_col], data[value_col], 
             label='Actual', linewidth=2, marker='o')
    
    # Trend line
    x = np.arange(len(data))
    slope, intercept, _ = fit_linear_trend(data, value_col)
    trend_line = slope * x + intercept
    plt.plot(data[date_col], trend_line, 
             label='Trend Line', linestyle='--', color='red', linewidth=2)
    
    plt.xlabel('Date')
    plt.ylabel(value_col)
    plt.title(f'{value_col} - Trend Analysis & Forecast')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.xticks(rotation=45)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def forecast_resource_demand(data, value_col, forecast_days=14):
    """Complete trend-based forecasting pipeline."""
    print(f"\n{'='*60}")
    print("TREND-BASED RESOURCE DEMAND FORECAST")
    print(f"{'='*60}")
    
    # Fit trend
    slope, intercept, r_squared = fit_linear_trend(data, value_col)
    
    # Forecast
    forecast = forecast_trend(data, value_col, periods=forecast_days)
    
    # Confidence intervals
    lower, upper = calculate_confidence_interval(
        data, value_col, forecast
    )
    
    return {
        'forecast': forecast,
        'lower_bound': lower,
        'upper_bound': upper,
        'slope': slope,
        'r_squared': r_squared
    }
