"""
DAYA Healthcare Resource Forecasting - Streamlit Dashboard
Real-time interactive dashboard for hospital bed demand forecasting
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="DAYA - Healthcare Forecasting",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
        }
        .metric-value {
            font-size: 32px;
            font-weight: bold;
            margin: 10px 0;
        }
        .metric-label {
            font-size: 14px;
            opacity: 0.9;
        }
        h1 {
            color: #2E86AB;
            text-align: center;
        }
        .section-header {
            color: #2E86AB;
            border-bottom: 3px solid #F18F01;
            padding-bottom: 10px;
            margin-top: 30px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load processed data and summary"""
    daily_beds = pd.read_csv('data/processed/daily_bed_occupancy.csv')
    daily_beds['date'] = pd.to_datetime(daily_beds['date'])
    
    with open('data/processed/analysis_summary.json', 'r') as f:
        summary = json.load(f)
    
    return daily_beds, summary

# Load data
daily_beds, summary = load_data()

# ============================================================================
# HEADER
# ============================================================================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("# 🏥 DAYA Dashboard")
    st.markdown("### Healthcare Resource Forecasting System")
    st.markdown("*Real-time analytics for hospital bed demand prediction*")

st.divider()

# ============================================================================
# KEY METRICS
# ============================================================================
st.markdown('<div class="section-header">📊 Key Metrics</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        label="Total Patients",
        value=f"{summary['data_summary']['total_patients']:,}",
        delta="Analyzed"
    )

with col2:
    st.metric(
        label="Total Encounters",
        value=f"{summary['data_summary']['total_encounters']:,}",
        delta="Records"
    )

with col3:
    st.metric(
        label="Average Beds/Day",
        value=f"{summary['bed_occupancy']['avg_daily_beds']:.0f}",
        delta="Current"
    )

with col4:
    st.metric(
        label="Peak Demand",
        value=f"{summary['bed_occupancy']['max_daily_beds']}",
        delta="beds"
    )

with col5:
    st.metric(
        label="ICU Ratio",
        value=f"{summary['icu_metrics']['icu_ratio']*100:.1f}%",
        delta="of encounters"
    )

with col6:
    trend_emoji = "📈" if summary['trend_analysis']['slope'] > 0 else "📉"
    st.metric(
        label="Trend Direction",
        value=summary['trend_analysis']['trend_direction'],
        delta=f"{summary['trend_analysis']['slope']:.4f} beds/day"
    )

st.divider()

# ============================================================================
# INTERACTIVE CHARTS
# ============================================================================
st.markdown('<div class="section-header">📈 Trend Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    # Create interactive bed occupancy chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_beds['date'],
        y=daily_beds['bed_count'],
        mode='lines+markers',
        name='Daily Bed Count',
        line=dict(color='#2E86AB', width=2),
        marker=dict(size=4)
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_beds['date'],
        y=daily_beds['MA_7'],
        mode='lines',
        name='7-Day Moving Average',
        line=dict(color='#F18F01', width=2, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_beds['date'],
        y=daily_beds['MA_14'],
        mode='lines',
        name='14-Day Moving Average',
        line=dict(color='#C73E1D', width=2, dash='dash')
    ))
    
    # Add threshold lines
    warning_threshold = summary['alerts']['warning_threshold']
    critical_threshold = summary['alerts']['critical_threshold']
    
    fig.add_hline(
        y=warning_threshold,
        line_dash="dash",
        line_color="orange",
        annotation_text="Warning Threshold",
        annotation_position="right"
    )
    
    fig.add_hline(
        y=critical_threshold,
        line_dash="dash",
        line_color="red",
        annotation_text="Critical Threshold",
        annotation_position="right"
    )
    
    fig.update_layout(
        title="Bed Occupancy Trend with Moving Averages",
        xaxis_title="Date",
        yaxis_title="Bed Count",
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**Current Status**")
    current_beds = summary['alerts']['current_beds']
    status_color = "🔴" if current_beds > warning_threshold else "🟢"
    
    st.write(f"{status_color} **{current_beds}** beds")
    st.write("")
    
    st.markdown("**Thresholds**")
    st.write(f"⚠️ Warning: {warning_threshold:.0f} beds")
    st.write(f"🔴 Critical: {critical_threshold:.0f} beds")
    
    occupancy_pct = (current_beds / 840) * 100
    st.write("")
    st.write(f"**Occupancy:** {occupancy_pct:.1f}%")

st.divider()

# ============================================================================
# DISTRIBUTION & PATTERNS
# ============================================================================
st.markdown('<div class="section-header">📊 Distribution & Patterns</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig_dist = go.Figure(data=[
        go.Histogram(
            x=daily_beds['bed_count'],
            nbinsx=30,
            name='Bed Count',
            marker=dict(color='#2E86AB', opacity=0.7)
        )
    ])
    fig_dist.update_layout(
        title="Bed Count Distribution",
        xaxis_title="Bed Count",
        yaxis_title="Frequency",
        height=400,
        template='plotly_white'
    )
    st.plotly_chart(fig_dist, use_container_width=True)

with col2:
    # Box plot
    fig_box = go.Figure(data=[
        go.Box(y=daily_beds['bed_count'], name='Bed Count', marker=dict(color='#2E86AB'))
    ])
    fig_box.update_layout(
        title="Box Plot (Outlier Detection)",
        yaxis_title="Bed Count",
        height=400,
        template='plotly_white'
    )
    st.plotly_chart(fig_box, use_container_width=True)

# ============================================================================
# TIME PATTERNS
# ============================================================================
st.markdown('<div class="section-header">🗓️ Time Patterns</div>', unsafe_allow_html=True)

# Add month and week to dataframe
daily_beds['month'] = daily_beds['date'].dt.month
daily_beds['day_of_week'] = daily_beds['date'].dt.day_name()

col1, col2 = st.columns(2)

with col1:
    monthly_avg = daily_beds.groupby('month')['bed_count'].mean()
    fig_monthly = px.bar(
        x=monthly_avg.index,
        y=monthly_avg.values,
        labels={'x': 'Month', 'y': 'Average Beds'},
        title='Monthly Average Pattern',
        color_discrete_sequence=['#F18F01']
    )
    fig_monthly.update_layout(height=400, template='plotly_white')
    st.plotly_chart(fig_monthly, use_container_width=True)

with col2:
    # Weekly pattern
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_avg = daily_beds.groupby('day_of_week')['bed_count'].mean().reindex(day_order)
    
    fig_weekly = px.bar(
        x=weekly_avg.index,
        y=weekly_avg.values,
        labels={'x': 'Day of Week', 'y': 'Average Beds'},
        title='Weekly Pattern Analysis',
        color_discrete_sequence=['#2E86AB']
    )
    fig_weekly.update_layout(height=400, template='plotly_white', xaxis_tickangle=-45)
    st.plotly_chart(fig_weekly, use_container_width=True)

st.divider()

# ============================================================================
# FORECAST & ALERTS
# ============================================================================
st.markdown('<div class="section-header">🔮 Forecast & Alerts</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 7-Day MA Forecast")
    forecast_value = summary['forecasts']['ma_7day']
    st.markdown(f"<div class='metric-value'>{forecast_value:.0f}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-label'>beds/day</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### Trend Analysis")
    st.write(f"**Direction:** {summary['trend_analysis']['trend_direction']}")
    st.write(f"**Slope:** {summary['trend_analysis']['slope']:.4f} beds/day")
    st.write(f"**R-squared:** {summary['trend_analysis']['r_squared']:.4f}")

with col3:
    st.markdown("### Alert Status")
    current = summary['alerts']['current_beds']
    warning = summary['alerts']['warning_threshold']
    critical = summary['alerts']['critical_threshold']
    
    if current > critical:
        st.error(f"🔴 CRITICAL: {current} beds > {critical:.0f}")
    elif current > warning:
        st.warning(f"⚠️ WARNING: {current} beds > {warning:.0f}")
    else:
        st.success(f"🟢 NORMAL: {current} beds ≤ {warning:.0f}")

st.divider()

# ============================================================================
# STATISTICS SUMMARY TABLE
# ============================================================================
st.markdown('<div class="section-header">📋 Statistics Summary</div>', unsafe_allow_html=True)

stats_data = {
    'Metric': [
        'Total Patients',
        'Total Encounters',
        'Clean Encounters',
        'Date Range',
        'Average Daily Beds',
        'Median Daily Beds',
        'Max Daily Beds',
        'Min Daily Beds',
        'Standard Deviation',
        'ICU/Emergency Ratio',
        'Trend Direction',
        'Slope (beds/day)',
        'R-squared',
        '7-Day MA Forecast',
        'Warning Threshold',
        'Critical Threshold',
        'Current Status'
    ],
    'Value': [
        f"{summary['data_summary']['total_patients']:,}",
        f"{summary['data_summary']['total_encounters']:,}",
        f"{summary['data_summary']['clean_encounters']:,}",
        f"{summary['data_summary']['date_range_start'][:10]} to {summary['data_summary']['date_range_end'][:10]}",
        f"{summary['bed_occupancy']['avg_daily_beds']:.2f}",
        f"{summary['bed_occupancy']['median_daily_beds']:.2f}",
        f"{summary['bed_occupancy']['max_daily_beds']}",
        f"{summary['bed_occupancy']['min_daily_beds']}",
        f"{summary['bed_occupancy']['std_dev']:.2f}",
        f"{summary['icu_metrics']['icu_ratio']*100:.2f}%",
        summary['trend_analysis']['trend_direction'],
        f"{summary['trend_analysis']['slope']:.4f}",
        f"{summary['trend_analysis']['r_squared']:.4f}",
        f"{summary['forecasts']['ma_7day']:.2f} beds/day",
        f"{summary['alerts']['warning_threshold']:.0f} beds",
        f"{summary['alerts']['critical_threshold']:.0f} beds",
        f"{summary['alerts']['current_beds']} beds"
    ]
}

stats_df = pd.DataFrame(stats_data)
st.dataframe(stats_df, use_container_width=True, hide_index=True)

st.divider()

# ============================================================================
# DATA DOWNLOAD
# ============================================================================
st.markdown('<div class="section-header">📥 Download Data</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    csv = daily_beds.to_csv(index=False)
    st.download_button(
        label="📥 Download Daily Bed Data (CSV)",
        data=csv,
        file_name="daily_bed_occupancy.csv",
        mime="text/csv"
    )

with col2:
    json_data = json.dumps(summary, indent=2)
    st.download_button(
        label="📥 Download Summary (JSON)",
        data=json_data,
        file_name="analysis_summary.json",
        mime="application/json"
    )

st.divider()

# ============================================================================
# FOOTER
# ============================================================================
col1, col2, col3 = st.columns(3)
with col2:
    st.markdown("""
        <div style='text-align: center; color: #999; font-size: 12px; margin-top: 30px;'>
            <p><strong>DAYA</strong> - Healthcare Resource Forecasting System</p>
            <p>Developed by MRP Team | 2025</p>
            <p>60,000 patients • 70,000 encounters • Real-time Analytics</p>
        </div>
    """, unsafe_allow_html=True)

# Add refresh button in sidebar
st.sidebar.divider()
if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Dashboard Info")
st.sidebar.write(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.sidebar.write(f"**Data Points:** {len(daily_beds)}")
st.sidebar.write(f"**Date Range:** {daily_beds['date'].min().date()} to {daily_beds['date'].max().date()}")
