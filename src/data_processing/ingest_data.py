"""
Data Ingestion Script
Loads raw datasets from Datasets folder and performs initial validation.
"""

import pandas as pd
import os
from pathlib import Path

# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASETS_DIR = BASE_DIR / "Datasets"
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

def load_ca_hospital_data():
    """Load CA Hospital Dataset (Q1 2025)."""
    ca_dir = DATASETS_DIR / "Ca"
    
    datasets = {
        'patients': 'patients.csv',
        'encounters': 'encounters.csv',
        'providers': 'providers.csv',
        'procedures': 'procedures.csv',
        'medications': 'medications.csv',
        'lab_tests': 'lab_tests.csv',
        'diagnoses': 'diagnoses.csv',
        'claims_billing': 'claims_and_billing.csv',
        'denials': 'denials.csv'
    }
    
    loaded_data = {}
    for name, filename in datasets.items():
        filepath = ca_dir / filename
        if filepath.exists():
            df = pd.read_csv(filepath)
            loaded_data[name] = df
            print(f"✓ Loaded {name}: {df.shape[0]} rows, {df.shape[1]} columns")
        else:
            print(f"✗ Missing: {filename}")
    
    return loaded_data

def load_icu_data():
    """Load ICU Patient Dataset (2025)."""
    icu_dir = DATASETS_DIR / "ICU"
    
    X_train_path = icu_dir / "X_train_2025.csv"
    y_train_path = icu_dir / "y_train_2025.csv"
    
    icu_data = {}
    if X_train_path.exists():
        icu_data['X_train'] = pd.read_csv(X_train_path)
        print(f"✓ Loaded ICU X_train: {icu_data['X_train'].shape}")
    
    if y_train_path.exists():
        icu_data['y_train'] = pd.read_csv(y_train_path)
        print(f"✓ Loaded ICU y_train: {icu_data['y_train'].shape}")
    
    return icu_data

def load_hospital_records():
    """Load Hospital Patient Records (2021-2024)."""
    records_dir = DATASETS_DIR / "Hospitals Records"
    records_path = records_dir / "hospital_records_2021_2024_with_bills.csv"
    
    if records_path.exists():
        df = pd.read_csv(records_path)
        print(f"✓ Loaded Hospital Records: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    else:
        print("✗ Missing: hospital_records_2021_2024_with_bills.csv")
        return None

def main():
    """Main ingestion function."""
    print("=" * 60)
    print("HEALTHCARE RESOURCE FORECASTING - DATA INGESTION")
    print("=" * 60)
    
    print("\n📊 Loading CA Hospital Dataset (Q1 2025)...")
    ca_data = load_ca_hospital_data()
    
    print("\n🏥 Loading ICU Dataset (2025)...")
    icu_data = load_icu_data()
    
    print("\n📈 Loading Hospital Records (2021-2024)...")
    hospital_records = load_hospital_records()
    
    print("\n" + "=" * 60)
    print("✓ Data ingestion complete!")
    print("=" * 60)
    
    return {
        'ca_hospital': ca_data,
        'icu': icu_data,
        'hospital_records': hospital_records
    }

if __name__ == "__main__":
    data = main()
