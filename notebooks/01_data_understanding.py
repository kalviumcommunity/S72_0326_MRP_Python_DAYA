"""
Milestone 4: Data Understanding
Explore datasets using head(), info(), describe()
"""

import pandas as pd
import sys
sys.path.append('..')
from src.data_processing.ingest_data import main as load_data

# Load all datasets
print("Loading datasets...")
data = load_data()

print("\n" + "="*60)
print("DATA UNDERSTANDING - MILESTONE 4")
print("="*60)

# CA Hospital - Patients
if 'patients' in data['ca_hospital']:
    patients = data['ca_hospital']['patients']
    print("\n📊 PATIENTS DATASET")
    print(f"Shape: {patients.shape}")
    print("\nFirst 5 rows:")
    print(patients.head())
    print("\nData types:")
    print(patients.info())
    print("\nSummary statistics:")
    print(patients.describe())

# CA Hospital - Encounters
if 'encounters' in data['ca_hospital']:
    encounters = data['ca_hospital']['encounters']
    print("\n\n📊 ENCOUNTERS DATASET")
    print(f"Shape: {encounters.shape}")
    print("\nFirst 5 rows:")
    print(encounters.head())
    print("\nColumn info:")
    print(encounters.info())
