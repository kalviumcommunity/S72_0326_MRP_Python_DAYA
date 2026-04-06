"""
Milestone 5: Data Cleaning
Handle missing values, remove duplicates, standardize date formats
"""

import pandas as pd
import numpy as np
from pathlib import Path

def clean_dates(df, date_columns):
    """Standardize date formats."""
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def handle_missing_values(df, strategy='drop', threshold=0.5):
    """
    Handle missing values.
    strategy: 'drop', 'fill_mean', 'fill_median', 'fill_mode'
    threshold: drop columns with missing % > threshold
    """
    print(f"\n🔍 Missing values before cleaning:")
    print(df.isnull().sum()[df.isnull().sum() > 0])
    
    # Drop columns with too many missing values
    missing_pct = df.isnull().sum() / len(df)
    cols_to_drop = missing_pct[missing_pct > threshold].index
    if len(cols_to_drop) > 0:
        print(f"\n❌ Dropping columns: {list(cols_to_drop)}")
        df = df.drop(columns=cols_to_drop)
    
    # Handle remaining missing values
    if strategy == 'drop':
        df = df.dropna()
    elif strategy == 'fill_mean':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif strategy == 'fill_median':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    print(f"\n✅ Missing values after cleaning:")
    remaining = df.isnull().sum().sum()
    print(f"Total: {remaining}")
    
    return df

def remove_duplicates(df):
    """Remove duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    removed = before - after
    print(f"\n🗑️  Removed {removed} duplicate rows ({removed/before*100:.2f}%)")
    return df

def clean_dataset(df, name="Dataset", date_cols=None):
    """Complete cleaning pipeline."""
    print(f"\n{'='*60}")
    print(f"CLEANING: {name}")
    print(f"{'='*60}")
    print(f"Initial shape: {df.shape}")
    
    # Remove duplicates
    df = remove_duplicates(df)
    
    # Clean dates
    if date_cols:
        df = clean_dates(df, date_cols)
    
    # Handle missing values
    df = handle_missing_values(df, strategy='fill_median')
    
    print(f"\nFinal shape: {df.shape}")
    return df
