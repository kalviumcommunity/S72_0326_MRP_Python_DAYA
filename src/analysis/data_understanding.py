"""Data understanding utilities."""

import pandas as pd

def explore_dataset(df, name="Dataset"):
    """Generate comprehensive dataset overview."""
    print(f"\n{'='*60}")
    print(f"{name.upper()}")
    print(f"{'='*60}")
    
    print(f"\n📊 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    print(f"\n📋 Columns: {list(df.columns)}")
    
    print(f"\n🔍 Data Types:")
    print(df.dtypes)
    
    print(f"\n📈 Summary Statistics:")
    print(df.describe())
    
    print(f"\n❓ Missing Values:")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("No missing values!")
    
    print(f"\n👀 First 3 Rows:")
    print(df.head(3))
    
    return {
        'shape': df.shape,
        'columns': list(df.columns),
        'dtypes': df.dtypes.to_dict(),
        'missing': missing.to_dict()
    }
