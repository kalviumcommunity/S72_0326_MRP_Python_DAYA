"""
Generate all visualizations and dashboards
Run this to create graphs, charts, and visual analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

print("="*70)
print("GENERATING VISUALIZATIONS & DASHBOARDS")
print("="*70)

# Create output directory
output_dir = Path('outputs')
output_dir.mkdir(exist_ok=True)

# Load processed data
print("\n[1/10] Loading data...")
daily_beds = pd.read_csv('data/processed/daily_bed_occupancy.csv')
daily_beds['date'] = pd.to_datetime(daily_beds['date'])

with open('data/processed/analysis_summary.json', 'r') as f:
    summary = json.load(f)

print(f"✓ Loaded {len(daily_beds)} days of data")

# ============================================================================
# 1. BED OCCUPANCY TREND
# ============================================================================
print("\n[2/10] Creating bed occupancy trend chart...")
fig, ax = plt.subplots(figsize=(16, 6))

ax.plot(daily_beds['date'], daily_beds['bed_count'], 
        linewidth=2, color='#2E86AB', label='Daily Bed Count', marker='o', markersize=4)
ax.plot(daily_beds['date'], daily_beds['MA_7'], 
        linewidth=2, color='#F18F01', label='7-Day Moving Average', linestyle='--')
ax.plot(daily_beds['date'], daily_beds['MA_14'], 
        linewidth=2, color='#C73E1D', label='14-Day Moving Average', linestyle='--')

ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Bed Count', fontsize=12, fontweight='bold')
ax.set_title('Hospital Bed Occupancy Trend with Moving Averages', 
             fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=11)
ax.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()

save_path = output_dir / '01_bed_occupancy_trend.png'
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {save_path}")

# ============================================================================
# 2. DISTRIBUTION HISTOGRAM
# ============================================================================
print("\n[3/10] Creating bed count distribution...")
fig, ax = plt.subplots(figsize=(12, 6))

ax.hist(daily_beds['bed_count'], bins=20, edgecolor='black', 
        color='#06A77D', alpha=0.7)
ax.axvline(daily_beds['bed_count'].mean(), color='red', 
           linestyle='--', linewidth=2, label=f'Mean: {daily_beds["bed_count"].mean():.0f}')
ax.axvline(daily_beds['bed_count'].median(), color='orange', 
           linestyle='--', linewidth=2, label=f'Median: {daily_beds["bed_count"].median():.0f}')

ax.set_xlabel('Bed Count', fontsize=12, fontweight='bold')
ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
ax.set_title('Distribution of Daily Bed Occupancy', 
             fontsize=14, fontweight='bold', pad=20)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()

save_path = output_dir / '02_bed_distribution.png'
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {save_path}")

# ============================================================================
# 3. BOX PLOT
# ============================================================================
print("\n[4/10] Creating box plot...")
fig, ax = plt.subplots(figsize=(10, 6))

box = ax.boxplot([daily_beds['bed_count']], 
                  labels=['Bed Count'],
                  patch_artist=True,
                  widths=0.5)

for patch in box['boxes']:
    patch.set_facecolor('#2E86AB')
    patch.set_alpha(0.7)

ax.set_ylabel('Bed Count', fontsize=12, fontweight='bold')
ax.set_title('Bed Occupancy Box Plot (Outlier Detection)', 
             fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()

save_path = output_dir / '03_bed_boxplot.png'
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {save_path}")

# ============================================================================
# 4. MONTHLY PATTERN
# ============================================================================
print("\n[5/10] Creating monthly pattern chart...")
monthly_avg = daily_beds.groupby('month')['bed_count'].agg(['mean', 'std'])
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

fig, ax = plt.subplots(figsize=(14, 6))

x = range(len(monthly_avg))
ax.bar(x, monthly_avg['mean'], yerr=monthly_avg['std'], 
       color='#F18F01', alpha=0.7, edgecolor='black', capsize=5)
ax.set_xticks(x)
ax.set_xticklabels([months[i-1] for i in monthly_avg.index])
ax.set_xlabel('Month', fontsize=12, fontweight='bold')
ax.set_ylabel('Average Bed Count', fontsize=12, fontweight='bold')
ax.set_title('Monthly Average Bed Occupancy (with Std Dev)', 
             fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()

save_path = output_dir / '04_monthly_pattern.png'
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {save_path}")

# ============================================================================
# 5. WEEKLY PATTERN
# ============================================================================
print("\n[6/10] Creating weekly pattern chart...")
weekly_avg = daily_beds.groupby('day_of_week')['bed_count'].mean()
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

fig, ax = plt.subplots(figsize=(12, 6))

colors = ['#2E86AB' if i < 5 else '#C73E1D' for i in range(7)]
ax.bar(range(7), weekly_avg, color=colors, alpha=0.7, edgecolor='black')
ax.set_xticks(range(7))
ax.set_xticklabels(days, rotation=45, ha='right')
ax.set_xlabel('Day of Week', fontsize=12, fontweight='bold')
ax.set_ylabel('Average Bed Count', fontsize=12, fontweight='bold')
ax.set_title('Weekly Pattern: Average Bed Occupancy by Day', 
             fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3)

# Add legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#2E86AB', alpha=0.7, label='Weekday'),
                   Patch(facecolor='#C73E1D', alpha=0.7, label='Weekend')]
ax.legend(handles=legend_elements, loc='best')

plt.tight_layout()

save_path = output_dir / '05_weekly_pattern.png'
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {save_path}")

# ============================================================================
# 6. FORECAST COMPARISON
# ============================================================================
print("\n[7/10] Creating forecast comparison...")
fig, ax = plt.subplots(figsize=(16, 6))

# Historical data
ax.plot(daily_beds['date'], daily_beds['bed_count'], 
        linewidth=2, marker='o', label='Actual', color='#2E86AB', markersize=4)

# Forecast dates
last_date = daily_beds['date'].max()
forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=7)

# MA forecast
ma_forecast = [summary['forecasts']['ma_7day']] * 7
ax.plot(forecast_dates, ma_forecast, 
        linewidth=2, marker='s', label='MA Forecast', 
        color='#F18F01', linestyle='--', markersize=6)

# Trend forecast
trend_forecast = summary['forecasts']['trend_7day']
ax.plot(forecast_dates, trend_forecast, 
        linewidth=2, marker='^', label='Trend Forecast', 
        color='#C73E1D', linestyle='--', markersize=6)

# Vertical line
ax.axvline(x=last_date, color='gray', linestyle=':', linewidth=2, label='Forecast Start')

ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Bed Count', fontsize=12, fontweight='bold')
ax.set_title('7-Day Bed Occupancy Forecast (MA vs Trend)', 
             fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=11)
ax.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()

save_path = output_dir / '06_forecast_comparison.png'
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {save_path}")

# ============================================================================
# 7. ALERT ZONES
# ============================================================================
print("\n[8/10] Creating alert zones visualization...")
fig, ax = plt.subplots(figsize=(16, 6))

warning = summary['alerts']['warning_threshold']
critical = summary['alerts']['critical_threshold']

ax.plot(daily_beds['date'], daily_beds['bed_count'], 
        linewidth=2, color='#2E86AB', label='Daily Bed Count', marker='o', markersize=4)

# Alert zones
ax.axhspan(0, warning, alpha=0.1, color='green', label='Normal Zone')
ax.axhspan(warning, critical, alpha=0.1, color='orange', label='Warning Zone')
ax.axhspan(critical, daily_beds['bed_count'].max() + 50, alpha=0.1, color='red', label='Critical Zone')

ax.axhline(y=warning, color='orange', linestyle='--', linewidth=2, label=f'Warning: {warning:.0f}')
ax.axhline(y=critical, color='red', linestyle='--', linewidth=2, label=f'Critical: {critical:.0f}')

ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Bed Count', fontsize=12, fontweight='bold')
ax.set_title('Bed Occupancy with Alert Thresholds', 
             fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=10)
ax.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()

save_path = output_dir / '07_alert_zones.png'
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {save_path}")

# ============================================================================
# 8. SUMMARY DASHBOARD
# ============================================================================
print("\n[9/10] Creating summary dashboard...")
fig = plt.figure(figsize=(18, 10))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Title
fig.suptitle('Healthcare Resource Forecasting Dashboard', 
             fontsize=18, fontweight='bold', y=0.98)

# Metric cards
def create_metric_card(ax, title, value, unit, color):
    ax.text(0.5, 0.6, f'{value}{unit}', 
           ha='center', va='center', fontsize=42, fontweight='bold', color=color)
    ax.text(0.5, 0.25, title, 
           ha='center', va='center', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, fill=True, alpha=0.1, color=color))

# Card 1: Average beds
ax1 = fig.add_subplot(gs[0, 0])
create_metric_card(ax1, 'Average Daily Beds', 
                  int(summary['bed_occupancy']['avg_daily_beds']), '', '#2E86AB')

# Card 2: Peak beds
ax2 = fig.add_subplot(gs[0, 1])
create_metric_card(ax2, 'Peak Demand', 
                  summary['bed_occupancy']['max_daily_beds'], ' beds', '#F18F01')

# Card 3: ICU ratio
ax3 = fig.add_subplot(gs[0, 2])
create_metric_card(ax3, 'ICU/Emergency Ratio', 
                  f"{summary['icu_metrics']['icu_ratio']*100:.1f}", '%', '#C73E1D')

# Chart 1: Trend
ax4 = fig.add_subplot(gs[1, :])
ax4.plot(daily_beds['date'], daily_beds['bed_count'], linewidth=2, color='#2E86AB')
ax4.plot(daily_beds['date'], daily_beds['MA_7'], linewidth=2, color='#F18F01', linestyle='--')
ax4.set_title('Bed Occupancy Trend', fontweight='bold')
ax4.set_xlabel('Date')
ax4.set_ylabel('Bed Count')
ax4.grid(alpha=0.3)
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)

# Chart 2: Distribution
ax5 = fig.add_subplot(gs[2, 0])
ax5.hist(daily_beds['bed_count'], bins=15, color='#06A77D', alpha=0.7, edgecolor='black')
ax5.set_title('Distribution', fontweight='bold')
ax5.set_xlabel('Bed Count')
ax5.set_ylabel('Frequency')
ax5.grid(axis='y', alpha=0.3)

# Chart 3: Monthly
ax6 = fig.add_subplot(gs[2, 1])
monthly_avg = daily_beds.groupby('month')['bed_count'].mean()
ax6.bar(range(len(monthly_avg)), monthly_avg, color='#F18F01', alpha=0.7, edgecolor='black')
ax6.set_title('Monthly Average', fontweight='bold')
ax6.set_xlabel('Month')
ax6.set_ylabel('Avg Beds')
ax6.grid(axis='y', alpha=0.3)

# Chart 4: Weekly
ax7 = fig.add_subplot(gs[2, 2])
weekly_avg = daily_beds.groupby('day_of_week')['bed_count'].mean()
colors = ['#2E86AB' if i < 5 else '#C73E1D' for i in range(7)]
ax7.bar(range(7), weekly_avg, color=colors, alpha=0.7, edgecolor='black')
ax7.set_title('Weekly Pattern', fontweight='bold')
ax7.set_xlabel('Day')
ax7.set_ylabel('Avg Beds')
ax7.set_xticks(range(7))
ax7.set_xticklabels(['M', 'T', 'W', 'T', 'F', 'S', 'S'])
ax7.grid(axis='y', alpha=0.3)

plt.tight_layout()

save_path = output_dir / '08_summary_dashboard.png'
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {save_path}")

# ============================================================================
# 9. STATISTICS TABLE
# ============================================================================
print("\n[10/10] Creating statistics summary...")
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('tight')
ax.axis('off')

stats_data = [
    ['Metric', 'Value'],
    ['', ''],
    ['DATA SUMMARY', ''],
    ['Total Patients', f"{summary['data_summary']['total_patients']:,}"],
    ['Total Encounters', f"{summary['data_summary']['total_encounters']:,}"],
    ['Clean Encounters', f"{summary['data_summary']['clean_encounters']:,}"],
    ['Date Range', f"{summary['data_summary']['date_range_start'][:10]} to {summary['data_summary']['date_range_end'][:10]}"],
    ['', ''],
    ['BED OCCUPANCY', ''],
    ['Average Daily Beds', f"{summary['bed_occupancy']['avg_daily_beds']:.2f}"],
    ['Median Daily Beds', f"{summary['bed_occupancy']['median_daily_beds']:.2f}"],
    ['Max Daily Beds', f"{summary['bed_occupancy']['max_daily_beds']}"],
    ['Min Daily Beds', f"{summary['bed_occupancy']['min_daily_beds']}"],
    ['Standard Deviation', f"{summary['bed_occupancy']['std_dev']:.2f}"],
    ['', ''],
    ['ICU METRICS', ''],
    ['ICU/Emergency Ratio', f"{summary['icu_metrics']['icu_ratio']*100:.2f}%"],
    ['', ''],
    ['TREND ANALYSIS', ''],
    ['Trend Direction', summary['trend_analysis']['trend_direction']],
    ['Slope (beds/day)', f"{summary['trend_analysis']['slope']:.4f}"],
    ['R-squared', f"{summary['trend_analysis']['r_squared']:.4f}"],
    ['', ''],
    ['FORECASTS', ''],
    ['7-Day MA Forecast', f"{summary['forecasts']['ma_7day']:.2f} beds/day"],
    ['', ''],
    ['ALERT THRESHOLDS', ''],
    ['Warning Threshold', f"{summary['alerts']['warning_threshold']:.0f} beds"],
    ['Critical Threshold', f"{summary['alerts']['critical_threshold']:.0f} beds"],
    ['Current Status', f"{summary['alerts']['current_beds']} beds"],
]

table = ax.table(cellText=stats_data, cellLoc='left', loc='center',
                colWidths=[0.5, 0.5])
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2)

# Style header
for i in range(2):
    table[(0, i)].set_facecolor('#2E86AB')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Style section headers
for row in [2, 8, 15, 17, 22, 24]:
    table[(row, 0)].set_facecolor('#F18F01')
    table[(row, 0)].set_text_props(weight='bold', color='white')
    table[(row, 1)].set_facecolor('#F18F01')

plt.title('Healthcare Resource Forecasting - Statistics Summary', 
          fontsize=16, fontweight='bold', pad=20)

save_path = output_dir / '09_statistics_table.png'
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {save_path}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("✓ ALL VISUALIZATIONS GENERATED!")
print("="*70)

print(f"\n📊 Generated 9 visualizations:")
print(f"  1. Bed occupancy trend with moving averages")
print(f"  2. Bed count distribution histogram")
print(f"  3. Box plot for outlier detection")
print(f"  4. Monthly pattern analysis")
print(f"  5. Weekly pattern analysis")
print(f"  6. 7-day forecast comparison")
print(f"  7. Alert zones visualization")
print(f"  8. Comprehensive summary dashboard")
print(f"  9. Statistics summary table")

print(f"\n📁 All files saved to: {output_dir.absolute()}")
print(f"\n💡 Open the 'outputs' folder to view all visualizations!")
print("="*70)
