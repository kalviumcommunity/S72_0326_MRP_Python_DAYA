"""
Milestone 7: Univariate Analysis
Analyze individual variables using histograms and summary statistics
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def plot_histogram(data, column, title=None, bins=30, save_path=None):
    """Create histogram for a single variable."""
    plt.figure(figsize=(10, 6))
    plt.hist(data[column].dropna(), bins=bins, edgecolor='black', alpha=0.7)
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.title(title or f'Distribution of {column}')
    plt.grid(axis='y', alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def analyze_numeric_variable(data, column):
    """Comprehensive analysis of numeric variable."""
    print(f"\n{'='*60}")
    print(f"UNIVARIATE ANALYSIS: {column}")
    print(f"{'='*60}")
    
    series = data[column].dropna()
    
    print(f"\n📊 Summary Statistics:")
    print(f"  Count: {len(series)}")
    print(f"  Mean: {series.mean():.2f}")
    print(f"  Median: {series.median():.2f}")
    print(f"  Std Dev: {series.std():.2f}")
    print(f"  Min: {series.min():.2f}")
    print(f"  Max: {series.max():.2f}")
    print(f"  Q1 (25%): {series.quantile(0.25):.2f}")
    print(f"  Q3 (75%): {series.quantile(0.75):.2f}")
    
    # Skewness
    skew = series.skew()
    print(f"\n📈 Skewness: {skew:.2f}")
    if abs(skew) < 0.5:
        print("  → Fairly symmetric")
    elif skew > 0:
        print("  → Right-skewed (tail on right)")
    else:
        print("  → Left-skewed (tail on left)")
    
    return {
        'mean': series.mean(),
        'median': series.median(),
        'std': series.std(),
        'skewness': skew
    }

def analyze_categorical_variable(data, column, top_n=10):
    """Analyze categorical variable."""
    print(f"\n{'='*60}")
    print(f"CATEGORICAL ANALYSIS: {column}")
    print(f"{'='*60}")
    
    value_counts = data[column].value_counts()
    
    print(f"\n📊 Unique Values: {len(value_counts)}")
    print(f"\nTop {top_n} Categories:")
    print(value_counts.head(top_n))
    
    print(f"\n📈 Percentage Distribution (Top {top_n}):")
    pct = (value_counts.head(top_n) / len(data) * 100).round(2)
    for cat, percentage in pct.items():
        print(f"  {cat}: {percentage}%")
    
    return value_counts
