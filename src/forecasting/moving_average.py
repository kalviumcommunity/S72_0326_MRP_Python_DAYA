"""
Milestone 11: Moving Average Forecast
Implement rolling averages (7-day, 14-day) for forecasting
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_moving_averages(data, value_col, windows=[7, 14, 30]):
    """Calculate multiple moving averages."""
    print(f"\n{'='*60}")
    print(f"MOVING AVERAGE FORECAST - {value_col}")
    print(f"{'='*60}")
    
    for window in windows:
        ma_col = f'MA_{window}'
        data[ma_col] = data[value_col].rolling(window=window).mean()
        print(f"✅ Calculated {window}-day moving average")
    
    return data

def forecast_moving_average(data, value_col, window=7, periods=7):
    """Forecast future values using moving average."""
    print(f"\n📈 Forecasting next {periods} periods using {window}-day MA")
    
    # Calculate moving average
    ma = data[value_col].rolling(window=window).mean()
    last_ma = ma.iloc[-1]
    
    # Simple forecast: use last MA value
    forecast = [last_ma] * periods
    
    print(f"\nForecast (constant MA): {last_ma:.2f}")
    print(f"Forecasted values: {forecast}")
    
    return forecast

def evaluate_forecast(actual, predicted):
    """Calculate forecast accuracy metrics."""
    actual = np.array(actual)
    predicted = np.array(predicted)
    
    # Mean Absolute Error
    mae = np.mean(np.abs(actual - predicted))
    
    # Mean Absolute Percentage Error
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    
    # Root Mean Squared Error
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))
    
    print(f"\n📊 Forecast Accuracy:")
    print(f"  MAE: {mae:.2f}")
    print(f"  MAPE: {mape:.2f}%")
    print(f"  RMSE: {rmse:.2f}")
    
    return {
        'mae': mae,
        'mape': mape,
        'rmse': rmse
    }

def plot_forecast(data, date_col, value_col, forecast, save_path=None):
    """Plot actual vs forecast."""
    plt.figure(figsize=(14, 6))
    
    # Plot actual data
    plt.plot(data[date_col], data[value_col], 
             label='Actual', linewidth=2)
    
    # Plot moving averages
    if 'MA_7' in data.columns:
        plt.plot(data[date_col], data['MA_7'], 
                label='7-day MA', linestyle='--', alpha=0.7)
    if 'MA_14' in data.columns:
        plt.plot(data[date_col], data['MA_14'], 
                label='14-day MA', linestyle='--', alpha=0.7)
    
    plt.xlabel('Date')
    plt.ylabel(value_col)
    plt.title(f'{value_col} - Actual vs Moving Averages')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.xticks(rotation=45)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def forecast_bed_demand(encounters_df, forecast_days=7):
    """Forecast bed demand using moving average."""
    print(f"\n{'='*60}")
    print("BED DEMAND FORECAST")
    print(f"{'='*60}")
    
    # Daily bed occupancy
    encounters_df['START'] = pd.to_datetime(encounters_df['START'])
    daily_beds = encounters_df.groupby(
        encounters_df['START'].dt.date
    ).size().reset_index()
    daily_beds.columns = ['date', 'bed_count']
    
    # Calculate moving averages
    daily_beds = calculate_moving_averages(
        daily_beds, 'bed_count', windows=[7, 14]
    )
    
    # Forecast
    forecast = forecast_moving_average(
        daily_beds, 'bed_count', window=7, periods=forecast_days
    )
    
    return daily_beds, forecast
