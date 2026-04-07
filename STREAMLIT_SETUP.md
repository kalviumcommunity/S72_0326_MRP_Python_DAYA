# Streamlit Dashboard - Complete Setup Guide 🚀

## Quick Start (Local)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Dashboard
```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## Google Colab Integration

### Option A: Simple - Manual Refresh
**Best for:** Quick testing, learning

```colab
# Cell 1: Clone repo and install
!git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
%cd YOUR_REPO
!pip install -r requirements.txt -q

# Cell 2: Run analysis and generate data
!python run_complete_analysis.py
!python generate_visualizations.py

# Cell 3: Display in Colab
import pandas as pd
import json

daily_beds = pd.read_csv('data/processed/daily_bed_occupancy.csv')
with open('data/processed/analysis_summary.json') as f:
    summary = json.load(f)

print("✅ Data updated successfully!")
print(f"Latest bed count: {daily_beds.iloc[-1]['bed_count']}")
```

---

### Option B: Real-Time - Streamlit Cloud

**Best for:** Public access, automated updates

#### Step 1: Push to GitHub
```bash
git add .
git commit -m "Add Streamlit dashboard"
git push origin main
```

#### Step 2: Deploy on Streamlit Cloud
1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository and `app.py`
5. Deploy!

Your app is live at: `https://YOUR_USERNAME-YOUR_REPO.streamlit.app`

#### Step 3: Auto-Update Data (Optional)
Create `.github/workflows/update-data.yml`:

```yaml
name: Auto-Update Data
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt -q
      
      - name: Run analysis
        run: |
          python run_complete_analysis.py
          python generate_visualizations.py
      
      - name: Commit and push
        run: |
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git config --global user.name "github-actions[bot]"
          git add data/processed/ outputs/
          git diff-index --quiet HEAD || git commit -m "Auto-update: $(date -u +'%Y-%m-%d %H:%M:%S UTC')"
          git push
```

Then Streamlit Cloud auto-rebuilds whenever data changes!

---

### Option C: Advanced - Firebase Real-Time

**Best for:** Truly real-time updates in Colab

#### Step 1: Create Firebase Project
1. Go to [firebase.google.com](https://firebase.google.com)
2. Create a new project
3. Enable Realtime Database
4. Download service account key

#### Step 2: Update Colab Script
```colab
!pip install firebase-admin -q

import firebase_admin
from firebase_admin import credentials, db
import json

# Initialize Firebase
cred = credentials.Certificate('firebase-key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://YOUR_PROJECT.firebaseio.com'
})

# Load and upload data
with open('data/processed/analysis_summary.json') as f:
    summary = json.load(f)

ref = db.reference('healthcare')
ref.set({
    'summary': summary,
    'updated_at': str(pd.Timestamp.now())
})

print("✅ Data synced to Firebase!")
```

#### Step 3: Read from Firebase in Streamlit
```python
# In app.py
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('firebase-key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://YOUR_PROJECT.firebaseio.com'
})

@st.cache_data(ttl=60)  # Refresh every 60 seconds
def get_realtime_data():
    ref = db.reference('healthcare/summary')
    return ref.get()

summary = get_realtime_data()
```

---

## Features

✅ **Interactive Charts** - Zoom, pan, hover for details  
✅ **Real-time Metrics** - Live status and alerts  
✅ **Multiple Visualizations** - Trends, distributions, patterns  
✅ **Data Download** - Export CSV and JSON  
✅ **Auto-Refresh** - Manual refresh button  
✅ **Alert System** - Warning and critical thresholds  
✅ **Professional UI** - Glass morphism, custom styling  
✅ **Responsive Design** - Works on mobile and desktop  

---

## Dashboard Sections

1. **🏥 Header** - DAYA branding and overview
2. **📊 Key Metrics** - 6 main KPIs at a glance
3. **📈 Trend Analysis** - Bed occupancy with moving averages
4. **📊 Distribution & Patterns** - Histograms and box plots
5. **🗓️ Time Patterns** - Monthly and weekly trends
6. **🔮 Forecast & Alerts** - 7-day forecast and status
7. **📋 Statistics Table** - Complete summary
8. **📥 Download Section** - Export data
9. **⚙️ Sidebar** - Info and refresh button

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit plotly
```

### Dashboard not showing data
- Check file paths in `app.py` match your structure
- Ensure `data/processed/daily_bed_occupancy.csv` exists
- Ensure `data/processed/analysis_summary.json` exists

### Charts not rendering
- Update plotly: `pip install --upgrade plotly`
- Clear Streamlit cache: `streamlit cache clear`

### Firebase authentication fails
- Download service account JSON from Firebase console
- Place in project root directory
- Ensure JSON path is correct in code

---

## Environment Variables (for Cloud Deployment)

Create `.streamlit/secrets.toml`:
```toml
firebase_project = "YOUR_PROJECT_ID"
firebase_key = "YOUR_PRIVATE_KEY"
github_token = "YOUR_GITHUB_TOKEN"
```

Then access in code:
```python
import streamlit as st
firebase_project = st.secrets["firebase_project"]
```

---

## Performance Tips

1. **Use Caching** - `@st.cache_data` already applied
2. **Large Datasets** - Consider date filtering
3. **Multiple Users** - Deploy with `--logger.level=error`
4. **Update Frequency** - Balance real-time vs load
   - Local: every minute
   - Cloud: every 6 hours
   - Firebase: true real-time

---

## Next Steps

1. ✅ Run `streamlit run app.py` locally
2. ✅ Test all visualizations
3. ✅ Deploy to Streamlit Cloud (free)
4. ✅ Set up automated data updates
5. ✅ Share dashboard link with team

---

## Support & Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [Plotly Charts](https://plotly.com/python)
- [Streamlit Cloud](https://streamlit.io/cloud)
- [Firebase Guide](https://firebase.google.com/docs)

---

Happy forecasting! 📊🚀
