"""
Milestone 8: Bivariate Analysis
Study relationships between variables using scatter plots
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def scatter_plot(data, x_col, y_col, title=None, save_path=None):
    """Create scatter plot for two variables."""
    plt.figure(figsize=(10, 6))
    plt.scatter(data[x_col], data[y_col], alpha=0.5)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(title or f'{y_col} vs {x_col}')
    plt.grid(alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def analyze_relationship(data, x_col, y_col):
    """Analyze relationship between two numeric variables."""
    print(f"\n{'='*60}")
    print(f"BIVARIATE ANALYSIS: {y_col} vs {x_col}")
    print(f"{'='*60}")
    
    # Remove missing values
    clean_data = data[[x_col, y_col]].dropna()
    
    # Correlation
    correlation = clean_data[x_col].corr(clean_data[y_col])
    print(f"\n📊 Pearson Correlation: {correlation:.3f}")
    
    if abs(correlation) > 0.7:
        print("  → Strong correlation")
    elif abs(correlation) > 0.4:
        print("  → Moderate correlation")
    else:
        print("  → Weak correlation")
    
    if correlation > 0:
        print("  → Positive relationship")
    else:
        print("  → Negative relationship")
    
    # Linear regression
    from scipy import stats
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        clean_data[x_col], 
        clean_data[y_col]
    )
    
    print(f"\n📈 Linear Regression:")
    print(f"  Slope: {slope:.4f}")
    print(f"  Intercept: {intercept:.4f}")
    print(f"  R-squared: {r_value**2:.4f}")
    print(f"  P-value: {p_value:.4e}")
    
    return {
        'correlation': correlation,
        'slope': slope,
        'r_squared': r_value**2,
        'p_value': p_value
    }

def cross_tabulation(data, cat1, cat2):
    """Create cross-tabulation for categorical variables."""
    print(f"\n{'='*60}")
    print(f"CROSS-TABULATION: {cat1} vs {cat2}")
    print(f"{'='*60}")
    
    crosstab = pd.crosstab(data[cat1], data[cat2])
    print("\n📊 Frequency Table:")
    print(crosstab)
    
    print("\n📈 Percentage Table:")
    print(pd.crosstab(data[cat1], data[cat2], normalize='all') * 100)
    
    return crosstab
