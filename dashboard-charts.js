/**
 * Dashboard Chart Renderer - Plotly.js
 * Loads data and renders interactive charts in dashboard.html
 */

// Global data storage
let dailyBedsData = null;
let summaryData = null;

/**
 * Load CSV data
 */
async function loadCSVData(filePath) {
    try {
        const response = await fetch(filePath);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${filePath} not found`);
        }
        const csvText = await response.text();
        return parseCSV(csvText);
    } catch (error) {
        console.error('Error loading CSV:', error);
        showError(`Failed to load ${filePath}. Make sure it exists and run on localhost:8000 (not file://)`);
        return null;
    }
}

/**
 * Parse CSV text to array of objects
 */
function parseCSV(csvText) {
    const lines = csvText.trim().split('\n');
    const headers = lines[0].split(',');
    const data = [];

    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        const obj = {};
        headers.forEach((header, index) => {
            const key = header.trim();
            const value = values[index].trim();
            // Convert to number if possible
            obj[key] = isNaN(value) ? value : parseFloat(value);
        });
        data.push(obj);
    }
    return data;
}

/**
 * Load JSON summary data
 */
async function loadJSONData(filePath) {
    try {
        const response = await fetch(filePath);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${filePath} not found`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error loading JSON:', error);
        showError(`Failed to load ${filePath}. Make sure it exists and run on localhost:8000 (not file://)`);
        return null;
    }
}

/**
 * Initialize all charts and update stats
 */
async function initializeDashboard() {
    console.log('🚀 Initializing dashboard...');
    console.log('📍 Current URL:', window.location.href);
    
    // Load data
    dailyBedsData = await loadCSVData('data/processed/daily_bed_occupancy.csv');
    summaryData = await loadJSONData('data/processed/analysis_summary.json');

    if (!dailyBedsData || !summaryData) {
        console.error('Failed to load one or more data files');
        showError('Failed to load data files. Make sure to run the server and files exist.');
        return;
    }

    // Update stats cards with real data
    updateStatsCards();

    // Render all charts
    renderBedOccupancyTrend();
    renderDistributionHistogram();
    renderBoxPlot();
    renderMonthlyPattern();
    renderWeeklyPattern();
    renderForecastComparison();
    renderAlertZones();
    renderStatisticsTable();

    console.log('✅ Dashboard initialized successfully');
}

/**
 * Update stats cards with real data
 */
function updateStatsCards() {
    // Total Patients
    const totalPatients = document.querySelector('[data-stat="patients"]');
    if (totalPatients) {
        totalPatients.querySelector('.stat-value').textContent = 
            summaryData.data_summary.total_patients.toLocaleString();
    }

    // Average Daily Beds
    const avgBeds = document.querySelector('[data-stat="avg-beds"]');
    if (avgBeds) {
        avgBeds.querySelector('.stat-value').textContent = 
            Math.round(summaryData.bed_occupancy.avg_daily_beds);
    }

    // ICU Ratio
    const icuRatio = document.querySelector('[data-stat="icu-ratio"]');
    if (icuRatio) {
        icuRatio.querySelector('.stat-value').textContent = 
            (summaryData.icu_metrics.icu_ratio * 100).toFixed(1) + '%';
    }

    // 7-Day Forecast
    const forecast = document.querySelector('[data-stat="forecast"]');
    if (forecast) {
        forecast.querySelector('.stat-value').textContent = 
            Math.round(summaryData.forecasts.ma_7day);
    }

    // Current Beds
    const currentBeds = summaryData.alerts.current_beds;
    const warningThreshold = summaryData.alerts.warning_threshold;
    const criticalThreshold = summaryData.alerts.critical_threshold;

    // Update alert status
    const alertStatus = document.querySelector('.alert-status');
    if (alertStatus) {
        if (currentBeds > criticalThreshold) {
            alertStatus.innerHTML = '<span class="status-badge status-critical"><i data-lucide="alert-octagon"></i> CRITICAL</span>';
        } else if (currentBeds > warningThreshold) {
            alertStatus.innerHTML = '<span class="status-badge status-warning"><i data-lucide="alert-triangle"></i> WARNING</span>';
        } else {
            alertStatus.innerHTML = '<span class="status-badge status-normal"><i data-lucide="check-circle"></i> Normal</span>';
        }
        lucide.createIcons();
    }
}

/**
 * Render Bed Occupancy Trend Chart
 */
function renderBedOccupancyTrend() {
    const container = document.getElementById('chart-bed-occupancy');
    if (!container) return;

    const dates = dailyBedsData.map(d => d.date);
    const bedCount = dailyBedsData.map(d => d.bed_count);
    const ma7 = dailyBedsData.map(d => d.MA_7);
    const ma14 = dailyBedsData.map(d => d.MA_14);

    const warningThreshold = summaryData.alerts.warning_threshold;
    const criticalThreshold = summaryData.alerts.critical_threshold;

    const trace1 = {
        x: dates,
        y: bedCount,
        mode: 'lines+markers',
        name: 'Daily Bed Count',
        line: { color: '#2E86AB', width: 2 },
        marker: { size: 4 }
    };

    const trace2 = {
        x: dates,
        y: ma7,
        mode: 'lines',
        name: '7-Day MA',
        line: { color: '#F18F01', width: 2, dash: 'dash' }
    };

    const trace3 = {
        x: dates,
        y: ma14,
        mode: 'lines',
        name: '14-Day MA',
        line: { color: '#C73E1D', width: 2, dash: 'dash' }
    };

    const layout = {
        title: 'Bed Occupancy Trend with Moving Averages',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Bed Count' },
        hovermode: 'x unified',
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { family: 'Outfit, sans-serif', color: '#ccc' },
        margin: { t: 40, r: 20, b: 40, l: 60 },
        shapes: [
            {
                type: 'line',
                x0: dates[0], x1: dates[dates.length - 1],
                y0: warningThreshold, y1: warningThreshold,
                line: { color: 'orange', width: 2, dash: 'dash' }
            },
            {
                type: 'line',
                x0: dates[0], x1: dates[dates.length - 1],
                y0: criticalThreshold, y1: criticalThreshold,
                line: { color: '#ef4444', width: 2, dash: 'dash' }
            }
        ],
        annotations: [
            {
                x: dates[dates.length - 1],
                y: warningThreshold,
                text: 'Warning',
                showarrow: false,
                xanchor: 'right',
                font: { color: 'orange', size: 10 }
            },
            {
                x: dates[dates.length - 1],
                y: criticalThreshold,
                text: 'Critical',
                showarrow: false,
                xanchor: 'right',
                font: { color: '#ef4444', size: 10 }
            }
        ]
    };

    const config = { responsive: true, displayModeBar: true };

    Plotly.newPlot(container, [trace1, trace2, trace3], layout, config);
}

/**
 * Render Distribution Histogram
 */
function renderDistributionHistogram() {
    const container = document.getElementById('chart-distribution');
    if (!container) return;

    const bedCount = dailyBedsData.map(d => d.bed_count);

    const trace = {
        x: bedCount,
        type: 'histogram',
        nbinsx: 20,
        name: 'Bed Count',
        marker: { color: '#2E86AB', opacity: 0.7 }
    };

    const layout = {
        title: 'Bed Count Distribution',
        xaxis: { title: 'Bed Count' },
        yaxis: { title: 'Frequency' },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { family: 'Outfit, sans-serif', color: '#ccc' },
        margin: { t: 40, r: 20, b: 40, l: 60 }
    };

    const config = { responsive: true, displayModeBar: true };

    Plotly.newPlot(container, [trace], layout, config);
}

/**
 * Render Box Plot
 */
function renderBoxPlot() {
    const container = document.getElementById('chart-boxplot');
    if (!container) return;

    const bedCount = dailyBedsData.map(d => d.bed_count);

    const trace = {
        y: bedCount,
        name: 'Bed Count',
        type: 'box',
        marker: { color: '#2E86AB' }
    };

    const layout = {
        title: 'Box Plot (Outlier Detection)',
        yaxis: { title: 'Bed Count' },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { family: 'Outfit, sans-serif', color: '#ccc' },
        margin: { t: 40, r: 20, b: 40, l: 60 }
    };

    const config = { responsive: true, displayModeBar: true };

    Plotly.newPlot(container, [trace], layout, config);
}

/**
 * Render Monthly Pattern
 */
function renderMonthlyPattern() {
    const container = document.getElementById('chart-monthly');
    if (!container) return;

    // Add month to data
    const dataWithMonth = dailyBedsData.map(d => ({
        ...d,
        date: new Date(d.date),
        month: new Date(d.date).getMonth() + 1
    }));

    // Calculate monthly averages
    const monthlyAvg = {};
    dataWithMonth.forEach(d => {
        if (!monthlyAvg[d.month]) monthlyAvg[d.month] = [];
        monthlyAvg[d.month].push(d.bed_count);
    });

    const months = Object.keys(monthlyAvg).map(m => parseInt(m)).sort((a, b) => a - b);
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const avgValues = months.map(m => 
        monthlyAvg[m].reduce((a, b) => a + b) / monthlyAvg[m].length
    );

    const trace = {
        x: months.map(m => monthNames[m - 1]),
        y: avgValues,
        type: 'bar',
        marker: { color: '#F18F01' }
    };

    const layout = {
        title: 'Monthly Average Pattern',
        xaxis: { title: 'Month' },
        yaxis: { title: 'Average Beds' },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { family: 'Outfit, sans-serif', color: '#ccc' },
        margin: { t: 40, r: 20, b: 40, l: 60 }
    };

    const config = { responsive: true, displayModeBar: true };

    Plotly.newPlot(container, [trace], layout, config);
}

/**
 * Render Weekly Pattern
 */
function renderWeeklyPattern() {
    const container = document.getElementById('chart-weekly');
    if (!container) return;

    // Add day of week to data
    const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const dataWithDay = dailyBedsData.map(d => ({
        ...d,
        date: new Date(d.date),
        dayOfWeek: new Date(d.date).getDay()
    }));

    // Calculate weekly averages
    const weeklyAvg = {};
    dataWithDay.forEach(d => {
        if (!weeklyAvg[d.dayOfWeek]) weeklyAvg[d.dayOfWeek] = [];
        weeklyAvg[d.dayOfWeek].push(d.bed_count);
    });

    const days = [0, 1, 2, 3, 4, 5, 6];
    const avgValues = days.map(d => {
        if (!weeklyAvg[d] || weeklyAvg[d].length === 0) return 0;
        return weeklyAvg[d].reduce((a, b) => a + b) / weeklyAvg[d].length;
    });

    const trace = {
        x: days.map(d => dayNames[d]),
        y: avgValues,
        type: 'bar',
        marker: { color: '#2E86AB' }
    };

    const layout = {
        title: 'Weekly Pattern Analysis',
        xaxis: { title: 'Day of Week' },
        yaxis: { title: 'Average Beds' },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { family: 'Outfit, sans-serif', color: '#ccc' },
        margin: { t: 40, r: 20, b: 40, l: 60 }
    };

    const config = { responsive: true, displayModeBar: true };

    Plotly.newPlot(container, [trace], layout, config);
}

/**
 * Render Forecast Comparison
 */
function renderForecastComparison() {
    const container = document.getElementById('chart-forecast');
    if (!container) return;

    const dates = dailyBedsData.map(d => d.date);
    const actual = dailyBedsData.map(d => d.bed_count);
    const ma7 = dailyBedsData.map(d => d.MA_7);

    const trace1 = {
        x: dates,
        y: actual,
        mode: 'lines',
        name: 'Actual',
        line: { color: '#2E86AB', width: 2 }
    };

    const trace2 = {
        x: dates,
        y: ma7,
        mode: 'lines',
        name: '7-Day MA Forecast',
        line: { color: '#F18F01', width: 2, dash: 'dash' }
    };

    const layout = {
        title: '7-Day Forecast Comparison (MA vs Actual)',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Bed Count' },
        hovermode: 'x unified',
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { family: 'Outfit, sans-serif', color: '#ccc' },
        margin: { t: 40, r: 20, b: 40, l: 60 }
    };

    const config = { responsive: true, displayModeBar: true };

    Plotly.newPlot(container, [trace1, trace2], layout, config);
}

/**
 * Render Alert Zones
 */
function renderAlertZones() {
    const container = document.getElementById('chart-alert-zones');
    if (!container) return;

    const dates = dailyBedsData.map(d => d.date);
    const bedCount = dailyBedsData.map(d => d.bed_count);
    
    const warningThreshold = summaryData.alerts.warning_threshold;
    const criticalThreshold = summaryData.alerts.critical_threshold;

    const trace = {
        x: dates,
        y: bedCount,
        mode: 'lines+markers',
        name: 'Bed Count',
        line: { color: '#2E86AB', width: 2 },
        marker: { size: 4 }
    };

    const layout = {
        title: 'Bed Occupancy with Alert Thresholds',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Bed Count' },
        hovermode: 'x unified',
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { family: 'Outfit, sans-serif', color: '#ccc' },
        margin: { t: 40, r: 20, b: 40, l: 60 },
        shapes: [
            {
                type: 'rect',
                x0: dates[0], x1: dates[dates.length - 1],
                y0: criticalThreshold, y1: Math.max(...bedCount) * 1.1,
                fillcolor: 'rgba(239, 68, 68, 0.1)',
                line: { color: '#ef4444' }
            },
            {
                type: 'rect',
                x0: dates[0], x1: dates[dates.length - 1],
                y0: warningThreshold, y1: criticalThreshold,
                fillcolor: 'rgba(251, 146, 60, 0.1)',
                line: { color: 'orange' }
            },
            {
                type: 'line',
                x0: dates[0], x1: dates[dates.length - 1],
                y0: warningThreshold, y1: warningThreshold,
                line: { color: 'orange', width: 2, dash: 'dash' }
            },
            {
                type: 'line',
                x0: dates[0], x1: dates[dates.length - 1],
                y0: criticalThreshold, y1: criticalThreshold,
                line: { color: '#ef4444', width: 2, dash: 'dash' }
            }
        ],
        annotations: [
            {
                x: dates[0],
                y: criticalThreshold,
                text: 'CRITICAL',
                showarrow: false,
                xanchor: 'left',
                yanchor: 'bottom',
                font: { color: '#ef4444', size: 10, weight: 'bold' }
            },
            {
                x: dates[0],
                y: warningThreshold,
                text: 'WARNING',
                showarrow: false,
                xanchor: 'left',
                yanchor: 'bottom',
                font: { color: 'orange', size: 10, weight: 'bold' }
            }
        ]
    };

    const config = { responsive: true, displayModeBar: true };

    Plotly.newPlot(container, [trace], layout, config);
}

/**
 * Render Statistics Summary Table
 */
function renderStatisticsTable() {
    const container = document.getElementById('statistics-table');
    if (!container) return;

    const stats = summaryData;
    
    const html = `
        <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
                <thead>
                    <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                        <th style="padding: 10px; text-align: left; border: 1px solid #444;">Metric</th>
                        <th style="padding: 10px; text-align: right; border: 1px solid #444;">Value</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="background: transparent; color: white;">
                        <td colspan="2" style="padding: 8px; background: #F18F01; color: white; font-weight: bold; border: 1px solid #444;">DATA SUMMARY</td>
                    </tr>
                    <tr style="background: rgba(255,255,255,0.05);">
                        <td style="padding: 8px; border: 1px solid #444;">Total Patients</td>
                        <td style="padding: 8px; text-align: right; border: 1px solid #444;">${stats.data_summary.total_patients.toLocaleString()}</td>
                    </tr>
                    <tr style="background: transparent;">
                        <td style="padding: 8px; border: 1px solid #444;">Total Encounters</td>
                        <td style="padding: 8px; text-align: right; border: 1px solid #444;">${stats.data_summary.total_encounters.toLocaleString()}</td>
                    </tr>
                    <tr style="background: rgba(255,255,255,0.05);">
                        <td style="padding: 8px; border: 1px solid #444;">Clean Encounters</td>
                        <td style="padding: 8px; text-align: right; border: 1px solid #444;">${stats.data_summary.clean_encounters.toLocaleString()}</td>
                    </tr>
                    <tr style="background: transparent;">
                        <td colspan="2" style="padding: 8px; background: #F18F01; color: white; font-weight: bold; border: 1px solid #444;">BED OCCUPANCY</td>
                    </tr>
                    <tr style="background: rgba(255,255,255,0.05);">
                        <td style="padding: 8px; border: 1px solid #444;">Average Daily Beds</td>
                        <td style="padding: 8px; text-align: right; border: 1px solid #444;">${stats.bed_occupancy.avg_daily_beds.toFixed(2)}</td>
                    </tr>
                    <tr style="background: transparent;">
                        <td style="padding: 8px; border: 1px solid #444;">Median Daily Beds</td>
                        <td style="padding: 8px; text-align: right; border: 1px solid #444;">${stats.bed_occupancy.median_daily_beds.toFixed(2)}</td>
                    </tr>
                    <tr style="background: rgba(255,255,255,0.05);">
                        <td style="padding: 8px; border: 1px solid #444;">Max Daily Beds</td>
                        <td style="padding: 8px; text-align: right; border: 1px solid #444;">${stats.bed_occupancy.max_daily_beds}</td>
                    </tr>
                    <tr style="background: transparent;">
                        <td colspan="2" style="padding: 8px; background: #F18F01; color: white; font-weight: bold; border: 1px solid #444;">FORECASTS & ALERTS</td>
                    </tr>
                    <tr style="background: rgba(255,255,255,0.05);">
                        <td style="padding: 8px; border: 1px solid #444;">7-Day MA Forecast</td>
                        <td style="padding: 8px; text-align: right; border: 1px solid #444;">${stats.forecasts.ma_7day.toFixed(2)} beds/day</td>
                    </tr>
                    <tr style="background: transparent;">
                        <td style="padding: 8px; border: 1px solid #444;">Warning Threshold</td>
                        <td style="padding: 8px; text-align: right; border: 1px solid #444;">${stats.alerts.warning_threshold.toFixed(0)} beds</td>
                    </tr>
                    <tr style="background: rgba(255,255,255,0.05);">
                        <td style="padding: 8px; border: 1px solid #444;">Critical Threshold</td>
                        <td style="padding: 8px; text-align: right; border: 1px solid #444;">${stats.alerts.critical_threshold.toFixed(0)} beds</td>
                    </tr>
                    <tr style="background: transparent;">
                        <td style="padding: 8px; border: 1px solid #444;">Current Status</td>
                        <td style="padding: 8px; text-align: right; border: 1px solid #444;">${stats.alerts.current_beds} beds</td>
                    </tr>
                </tbody>
            </table>
        </div>
    `;

    container.innerHTML = html;
}

/**
 * Show error message
 */
function showError(message) {
    console.error(message);
    
    // Create prominent error banner
    const errorBanner = document.createElement('div');
    errorBanner.style.cssText = `
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 20px;
        border-radius: 8px;
        margin: 20px;
        font-weight: 600;
        z-index: 1000;
        position: fixed;
        top: 20px;
        left: 20px;
        right: 20px;
        max-width: 500px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    `;
    
    errorBanner.innerHTML = `
        <div style="font-size: 18px; margin-bottom: 10px;">❌ Error Loading Data</div>
        <div style="font-size: 14px; line-height: 1.6;">
            <p>${message}</p>
            <p style="margin-top: 10px;"><strong>Fix:</strong></p>
            <ol style="margin: 10px 0; padding-left: 20px;">
                <li>Open PowerShell in project folder</li>
                <li>Run: <code style="background: rgba(0,0,0,0.3); padding: 5px;">python -m http.server 8000</code></li>
                <li>Visit: <code style="background: rgba(0,0,0,0.3); padding: 5px;">http://localhost:8000/dashboard.html</code></li>
            </ol>
        </div>
    `;
    
    document.body.insertBefore(errorBanner, document.body.firstChild);
}

/**
 * Refresh data and charts
 */
async function refreshDashboard() {
    const btn = document.getElementById('refresh-btn');
    if (btn) {
        btn.innerHTML = '<i data-lucide="loader"></i> Refreshing...';
        btn.disabled = true;
    }

    console.log('🔄 Refreshing dashboard...');
    dailyBedsData = null;
    summaryData = null;
    
    await initializeDashboard();
    
    if (btn) {
        btn.innerHTML = '<i data-lucide="refresh-cw"></i> Refresh Data';
        btn.disabled = false;
    }
    console.log('✅ Refresh complete');
}

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('📊 Creating interactive Plotly dashboard...');
    initializeDashboard();

    // Add refresh button listener
    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', refreshDashboard);
    }
});
