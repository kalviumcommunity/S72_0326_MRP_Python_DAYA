"""
Milestone 14: Visualization Dashboard
Build visualizations showing trends, forecasts, and alerts
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

class HealthcareDashboard:
    """Dashboard for healthcare resource forecasting."""
    
    def __init__(self, output_dir='outputs'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def plot_bed_occupancy_trend(self, data, date_col, value_col):
        """Plot bed occupancy over time."""
        fig, ax = plt.subplots(figsize=(14, 6))
        
        ax.plot(data[date_col], data[value_col], 
                linewidth=2, color='#2E86AB', label='Daily Occupancy')
        
        # Add moving average
        if 'MA_7' in data.columns:
            ax.plot(data[date_col], data['MA_7'], 
                   linestyle='--', color='#A23B72', 
                   label='7-day MA', linewidth=2)
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Bed Occupancy', fontsize=12)
        ax.set_title('Hospital Bed Occupancy Trend', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        save_path = self.output_dir / 'bed_occupancy_trend.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {save_path}")
    
    def plot_forecast_comparison(self, actual, forecast, title='Forecast'):
        """Plot actual vs forecast."""
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Actual data
        ax.plot(range(len(actual)), actual, 
                linewidth=2, marker='o', label='Actual', color='#2E86AB')
        
        # Forecast
        forecast_x = range(len(actual), len(actual) + len(forecast))
        ax.plot(forecast_x, forecast, 
                linewidth=2, marker='s', label='Forecast', 
                color='#F18F01', linestyle='--')
        
        # Vertical line separating actual and forecast
        ax.axvline(x=len(actual)-0.5, color='red', 
                  linestyle=':', linewidth=2, label='Forecast Start')
        
        ax.set_xlabel('Time Period', fontsize=12)
        ax.set_ylabel('Value', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        plt.tight_layout()
        
        save_path = self.output_dir / 'forecast_comparison.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {save_path}")
    
    def plot_resource_heatmap(self, data, title='Resource Usage Heatmap'):
        """Create heatmap of resource usage."""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        sns.heatmap(data, annot=True, fmt='.1f', cmap='YlOrRd',
                   cbar_kws={'label': 'Usage Level'}, ax=ax)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        save_path = self.output_dir / 'resource_heatmap.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {save_path}")
    
    def plot_alert_summary(self, alert_counts):
        """Visualize alert distribution."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = list(alert_counts.keys())
        counts = list(alert_counts.values())
        colors = ['#C1121F', '#FCA311', '#06A77D']
        
        bars = ax.bar(categories, counts, color=colors, edgecolor='black')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.set_ylabel('Count', fontsize=12)
        ax.set_title('Alert Summary', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        save_path = self.output_dir / 'alert_summary.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {save_path}")
    
    def create_summary_dashboard(self, metrics):
        """Create comprehensive summary dashboard."""
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # Title
        fig.suptitle('Healthcare Resource Forecasting Dashboard', 
                    fontsize=16, fontweight='bold')
        
        # Metric cards
        ax1 = fig.add_subplot(gs[0, 0])
        self._create_metric_card(ax1, 'Bed Occupancy', 
                                metrics.get('bed_occupancy', 0), '%')
        
        ax2 = fig.add_subplot(gs[0, 1])
        self._create_metric_card(ax2, 'ICU Usage', 
                                metrics.get('icu_usage', 0), '%')
        
        save_path = self.output_dir / 'summary_dashboard.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {save_path}")
    
    def _create_metric_card(self, ax, title, value, unit):
        """Create a metric card."""
        ax.text(0.5, 0.6, f'{value:.1f}{unit}', 
               ha='center', va='center', fontsize=36, fontweight='bold')
        ax.text(0.5, 0.3, title, 
               ha='center', va='center', fontsize=14)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Color based on value
        if value > 80:
            color = '#C1121F'
        elif value > 60:
            color = '#FCA311'
        else:
            color = '#06A77D'
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, 
                                   fill=True, alpha=0.1, color=color))
