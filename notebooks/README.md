# Jupyter Notebooks - Healthcare Resource Forecasting

## 📓 Available Notebooks

### 1. Complete Analysis (`01_Complete_Analysis.ipynb`)
**What it does:**
- Loads 3 datasets (60K patients, 70K encounters)
- Cleans data (removes invalid records)
- Engineers features (moving averages, time features)
- Performs EDA (univariate, time series analysis)
- Generates forecasts (MA and trend-based)
- Creates alert system
- Exports results to CSV and JSON

**Run time:** ~2-3 minutes

**Outputs:**
- `data/processed/daily_bed_occupancy.csv`
- `data/processed/analysis_summary.json`

---

### 2. Visualizations (`02_Visualizations.ipynb`)
**What it does:**
- Loads processed data from notebook 1
- Creates 6 professional visualizations:
  1. Bed occupancy trend with moving averages
  2. Distribution histogram
  3. Monthly pattern chart
  4. Weekly pattern chart
  5. 7-day forecast comparison
  6. Alert zones visualization

**Run time:** ~1-2 minutes

**Outputs:**
- 6 PNG files in `outputs/` folder (300 DPI)

---

## 🚀 How to Run in Google Colab

### Option 1: Upload to Google Drive
1. Upload your `Datasets/` folder to Google Drive
2. Upload the notebooks to Google Drive
3. Open notebook in Google Colab
4. Mount Google Drive:
```python
from google.colab import drive
drive.mount('/content/drive')
%cd /content/drive/MyDrive/your-project-folder
```
5. Run all cells

### Option 2: Direct Upload to Colab
1. Open Google Colab: https://colab.research.google.com/
2. Click "Upload" and select the notebook
3. Upload your `Datasets/` folder using the file browser
4. Run all cells

### Option 3: GitHub Integration
1. Go to: https://colab.research.google.com/
2. Click "GitHub" tab
3. Enter: `kalviumcommunity/S72_0326_MRP_Python_DAYA`
4. Select the notebook
5. Upload datasets when prompted

---

## 📋 Running Order

**Run notebooks in this order:**

1. **First:** `01_Complete_Analysis.ipynb`
   - This processes the raw data and creates the analysis

2. **Second:** `02_Visualizations.ipynb`
   - This uses the output from notebook 1 to create charts

---

## 📁 Required Folder Structure

```
your-project/
├── Datasets/
│   ├── Ca/
│   │   ├── patients.csv
│   │   ├── encounters.csv
│   │   ├── procedures.csv
│   │   └── providers.csv
│   ├── ICU/
│   │   ├── X_train_2025.csv
│   │   └── y_train_2025.csv
│   └── Hospitals Records/
│       └── hospital_records_2021_2024_with_bills.csv
├── notebooks/
│   ├── 01_Complete_Analysis.ipynb
│   └── 02_Visualizations.ipynb
├── data/
│   └── processed/  (created automatically)
└── outputs/  (created automatically)
```

---

## 🔧 Troubleshooting

### "File not found" error
- Make sure your `Datasets/` folder is in the same directory as the notebooks
- Check that CSV files are named exactly as shown above

### "Module not found" error
- Run the first cell that installs packages:
```python
!pip install pandas numpy matplotlib seaborn scipy -q
```

### Memory issues in Colab
- The free tier should be sufficient for these datasets
- If you get memory errors, restart runtime and run again

---

## 💡 Tips for Google Colab

1. **Save your work:** Colab auto-saves, but download notebooks periodically
2. **Runtime limits:** Free tier has ~12 hour limit, plenty for this project
3. **GPU not needed:** These notebooks use CPU only
4. **Download outputs:** Right-click files in file browser to download

---

## 📊 Expected Results

After running both notebooks, you should have:

**Data files:**
- `daily_bed_occupancy.csv` (36 rows)
- `analysis_summary.json` (complete statistics)

**Visualizations:**
- 6 high-resolution PNG charts

**Key metrics:**
- Average daily beds: ~787
- ICU ratio: ~20.1%
- Trend: Decreasing (-0.53 beds/day)
- 7-day forecast: ~777 beds/day

---

## 🎓 Learning Outcomes

By running these notebooks, you'll learn:
- Data cleaning and preprocessing
- Feature engineering for time series
- Exploratory data analysis (EDA)
- Statistical forecasting methods
- Data visualization best practices
- Professional data science workflow

---

## 📞 Need Help?

If you encounter issues:
1. Check the error message carefully
2. Verify file paths and names
3. Ensure all packages are installed
4. Restart runtime and try again

---

**Happy Analyzing! 📊🚀**
