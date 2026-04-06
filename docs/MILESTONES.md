# Project Milestones & Branching Strategy

## 🎯 15 Learning Milestones

### PR 1: Project Foundation (M1-M3)
- **M1**: Problem Framing → `feature/problem-definition`
- **M2**: Project Setup → `setup/project-structure`
- **M3**: Data Collection → `data/data-ingestion`

### PR 2: Data Processing (M4-M6)
- **M4**: Data Understanding → `analysis/data-understanding`
- **M5**: Data Cleaning → `data/data-cleaning`
- **M6**: Feature Engineering → `feature/feature-engineering`

### PR 3: Exploratory Analysis (M7-M10)
- **M7**: Univariate Analysis → `analysis/univariate`
- **M8**: Bivariate Analysis → `analysis/bivariate`
- **M9**: Time Series Analysis → `analysis/time-series`
- **M10**: Correlation Analysis → `analysis/correlation`

### PR 4: Forecasting & Alerts (M11-M13)
- **M11**: Moving Average Forecast → `forecast/moving-average`
- **M12**: Trend-Based Forecasting → `forecast/trend-analysis`
- **M13**: Alert System → `feature/alerts`

### PR 5: Visualization & Documentation (M14-M15)
- **M14**: Visualization Dashboard → `viz/dashboard`
- **M15**: Documentation & Insights → `docs/readme`

## 🌿 Git Workflow

```bash
# For each milestone
git checkout -b <branch-name>
# ... make changes ...
git add .
git commit -m "feat: <milestone description>"
git push origin <branch-name>
# Create PR on GitHub
```
