"""
Milestone 10: Correlation Analysis
Compute correlation matrix and identify strong relationships
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def compute_correlation_matrix(data, numeric_only=True):
    """Compute correlation matrix for numeric columns."""
    if numeric_only:
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        corr_data = data[numeric_cols]
    else:
        corr_data = data
    
    corr_matrix = corr_data.corr()
    
    print(f"\n{'='*60}")
    print("CORRELATION MATRIX")
    print(f"{'='*60}")
    print(f"\nAnalyzing {len(corr_matrix)} numeric variables")
    
    return corr_matrix

def plot_correlation_heatmap(corr_matrix, title=None, save_path=None):
    """Create correlation heatmap."""
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        fmt='.2f', 
        cmap='coolwarm',
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.8}
    )
    plt.title(title or 'Correlation Heatmap')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def find_strong_correlations(corr_matrix, threshold=0.7):
    """Identify strong correlations."""
    print(f"\n🔍 Strong Correlations (|r| > {threshold}):")
    
    strong_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_value = corr_matrix.iloc[i, j]
            if abs(corr_value) > threshold:
                var1 = corr_matrix.columns[i]
                var2 = corr_matrix.columns[j]
                strong_corr.append((var1, var2, corr_value))
                print(f"  {var1} ↔ {var2}: {corr_value:.3f}")
    
    if not strong_corr:
        print("  No strong correlations found")
    
    return strong_corr

def analyze_correlations(data):
    """Complete correlation analysis."""
    print(f"\n{'='*60}")
    print("CORRELATION ANALYSIS - MILESTONE 10")
    print(f"{'='*60}")
    
    # Compute correlation matrix
    corr_matrix = compute_correlation_matrix(data)
    
    # Display full matrix
    print(f"\n📊 Full Correlation Matrix:")
    print(corr_matrix)
    
    # Find strong correlations
    strong = find_strong_correlations(corr_matrix, threshold=0.7)
    
    # Find moderate correlations
    print(f"\n📈 Moderate Correlations (0.4 < |r| < 0.7):")
    moderate = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_value = corr_matrix.iloc[i, j]
            if 0.4 < abs(corr_value) <= 0.7:
                var1 = corr_matrix.columns[i]
                var2 = corr_matrix.columns[j]
                moderate.append((var1, var2, corr_value))
                print(f"  {var1} ↔ {var2}: {corr_value:.3f}")
    
    if not moderate:
        print("  No moderate correlations found")
    
    return {
        'matrix': corr_matrix,
        'strong': strong,
        'moderate': moderate
    }
