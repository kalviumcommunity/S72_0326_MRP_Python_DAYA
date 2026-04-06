# Git Workflow Guide - Healthcare Resource Forecasting

## 🎯 Current Status
✅ **M1 Complete**: Problem definition pushed to GitHub
✅ **Branch**: `feature/problem-definition` created and pushed
✅ **Main branch**: Initialized with project structure

## 📋 Next Steps - PR 1: Project Foundation

### Step 1: Create PR for M1
1. Go to: https://github.com/kalviumcommunity/S72_0326_MRP_Python_DAYA/pulls
2. Click "New Pull Request"
3. Base: `main` ← Compare: `feature/problem-definition`
4. Title: `PR 1.1: Define Problem Statement (M1)`
5. Description:
```
## Milestone 1: Problem Framing

### Changes
- Added comprehensive problem definition document
- Defined key objectives and success metrics
- Outlined expected outputs and constraints

### Files Added
- `docs/PROBLEM_DEFINITION.md`
- `docs/MILESTONES.md`
- Project structure setup
```
6. Create PR and merge it

### Step 2: M2 - Project Setup (Already Done!)
The project structure is already set up. Create a new branch:

```bash
git checkout main
git pull origin main
git checkout -b setup/project-structure
git add .
git commit -m "feat(M2): Set up project structure with folders and dependencies"
git push -u origin setup/project-structure
```

Create PR with title: `PR 1.2: Project Structure Setup (M2)`

### Step 3: M3 - Data Ingestion
```bash
git checkout main
git pull origin main
git checkout -b data/data-ingestion
# The ingest_data.py is already created
# Test it:
python src/data_processing/ingest_data.py
git add .
git commit -m "feat(M3): Implement data ingestion for all three datasets"
git push -u origin data/data-ingestion
```

Create PR with title: `PR 1.3: Data Ingestion Implementation (M3)`

## 🔄 Complete PR 1 Workflow
After all 3 PRs are merged, you'll have completed PR 1: Project Foundation

---

## 📊 PR 2: Data Processing (M4-M6)

### M4: Data Understanding
```bash
git checkout main
git pull
git checkout -b analysis/data-understanding
```

**Prompt for yourself:**
"Explore dataset using head(), info(), describe(). Identify key variables and data types."

Create file: `notebooks/01_data_understanding.ipynb`

### M5: Data Cleaning
```bash
git checkout -b data/data-cleaning
```

**Prompt:**
"Handle missing values, remove duplicates, and standardize date formats."

Create file: `src/data_processing/clean_data.py`

### M6: Feature Engineering
```bash
git checkout -b feature/feature-engineering
```

**Prompt:**
"Create new features such as bed occupancy rate, ICU ratio, and oxygen per patient."

Create file: `src/data_processing/feature_engineering.py`

---

## 🔍 PR 3: Exploratory Analysis (M7-M10)

Follow same pattern for:
- M7: `analysis/univariate`
- M8: `analysis/bivariate`
- M9: `analysis/time-series`
- M10: `analysis/correlation`

---

## 📈 PR 4: Forecasting & Alerts (M11-M13)

- M11: `forecast/moving-average`
- M12: `forecast/trend-analysis`
- M13: `feature/alerts`

---

## 📊 PR 5: Visualization & Documentation (M14-M15)

- M14: `viz/dashboard`
- M15: `docs/readme`

---

## 💡 Pro Tips

1. **Always pull before creating new branch**:
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Commit message format**:
   ```
   feat(M#): Brief description
   ```

3. **Before pushing, test your code**:
   ```bash
   python src/data_processing/ingest_data.py
   ```

4. **Keep PRs focused**: Each PR should complete 1-3 related milestones

5. **Document as you go**: Update README.md checklist after each milestone
