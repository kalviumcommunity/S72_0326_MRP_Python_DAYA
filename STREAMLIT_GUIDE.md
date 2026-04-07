"""
Instructions for running the Streamlit Dashboard
"""

# OPTION 1: Install Streamlit and run locally
# ============================================

# 1. Install Streamlit
pip install streamlit plotly

# 2. Run the dashboard
streamlit run app.py

# 3. Open in browser (Streamlit will show the URL, typically http://localhost:8501)


# OPTION 2: Run on Google Colab
# =============================

# In Google Colab, use this code:
"""
!pip install streamlit plotly -q

# Create a tunnel to expose local server
!npm install -g localtunnel

# In terminal 1: Run streamlit
!streamlit run /path/to/app.py --server.port 8501 &

# In terminal 2: Create tunnel
!lt --port 8501
"""


# OPTION 3: Deploy on Streamlit Cloud (Free)
# ===========================================

# 1. Push your project to GitHub
# 2. Go to https://streamlit.io/cloud
# 3. Sign in with GitHub
# 4. Click "New app" and select your repository
# 5. Specify the path to app.py
# 6. Deploy!

# Cloud URL will be: https://your-username-appname.streamlit.app


# ============================================
# FEATURES
# ============================================

# ✅ Real-time interactive charts using Plotly
# ✅ Key metrics with current status
# ✅ Bed occupancy trends with moving averages
# ✅ Alert thresholds visualization
# ✅ Distribution & pattern analysis
# ✅ Time-based patterns (monthly & weekly)
# ✅ Statistics summary table
# ✅ Data download options
# ✅ Auto-refresh capability
# ✅ Responsive design
# ✅ Professional styling


# ============================================
# FOR GOOGLE COLAB INTEGRATION
# ============================================

# To auto-refresh data from Colab:

# 1. Schedule Colab notebook to run periodically:
#    - Use Google Cloud Scheduler
#    - Or run it manually and it updates the CSVs

# 2. Streamlit automatically detects file changes

# 3. Users can click "Refresh Data" button to reload

# 4. Deploy Streamlit Cloud app for public access


# ============================================
# FILE STRUCTURE REQUIRED
# ============================================

# Your project should have:
# ├── app.py                          <- Main Streamlit app (NEW)
# ├── data/
# │   └── processed/
# │       ├── daily_bed_occupancy.csv
# │       └── analysis_summary.json
# ├── requirements.txt
# └── ... (your other files)
