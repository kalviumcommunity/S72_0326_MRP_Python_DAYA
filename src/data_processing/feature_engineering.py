"""
Milestone 6: Feature Engineering
Create features: bed_occupancy_rate, icu_ratio, oxygen_per_patient
"""

import pandas as pd
import numpy as np

def calculate_bed_occupancy_rate(encounters_df):
    """Calculate daily bed occupancy rate."""
    if 'START' in encounters_df.columns and 'STOP' in encounters_df.columns:
        encounters_df['START'] = pd.to_datetime(encounters_df['START'])
        encounters_df['STOP'] = pd.to_datetime(encounters_df['STOP'])
        
        # Calculate length of stay
        encounters_df['length_of_stay'] = (
            encounters_df['STOP'] - encounters_df['START']
        ).dt.total_seconds() / 86400  # Convert to days
        
        # Daily occupancy
        daily_occupancy = encounters_df.groupby(
            encounters_df['START'].dt.date
        ).size()
        
        return daily_occupancy
    return None

def calculate_icu_ratio(encounters_df):
    """Calculate ICU admission ratio."""
    if 'ENCOUNTERCLASS' in encounters_df.columns:
        total = len(encounters_df)
        icu_count = len(encounters_df[
            encounters_df['ENCOUNTERCLASS'].str.contains('intensive|icu', 
                                                         case=False, 
                                                         na=False)
        ])
        icu_ratio = icu_count / total if total > 0 else 0
        
        print(f"ICU Ratio: {icu_ratio:.2%} ({icu_count}/{total})")
        return icu_ratio
    return None

def calculate_oxygen_per_patient(procedures_df, encounters_df):
    """Estimate oxygen usage per patient."""
    if 'DESCRIPTION' in procedures_df.columns:
        oxygen_procedures = procedures_df[
            procedures_df['DESCRIPTION'].str.contains(
                'oxygen|ventilat|respirat', 
                case=False, 
                na=False
            )
        ]
        
        oxygen_count = len(oxygen_procedures)
        total_patients = encounters_df['PATIENT'].nunique() if 'PATIENT' in encounters_df.columns else 1
        
        oxygen_per_patient = oxygen_count / total_patients
        print(f"Oxygen procedures per patient: {oxygen_per_patient:.2f}")
        
        return oxygen_per_patient
    return None

def create_time_features(df, date_col='START'):
    """Extract time-based features."""
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col])
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        df['day_of_week'] = df[date_col].dt.dayofweek
        df['quarter'] = df[date_col].dt.quarter
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    return df

def engineer_features(ca_data):
    """Main feature engineering pipeline."""
    print("\n" + "="*60)
    print("FEATURE ENGINEERING - MILESTONE 6")
    print("="*60)
    
    features = {}
    
    # Bed occupancy
    if 'encounters' in ca_data:
        print("\n📊 Calculating bed occupancy rate...")
        occupancy = calculate_bed_occupancy_rate(ca_data['encounters'])
        if occupancy is not None:
            features['daily_bed_occupancy'] = occupancy
            print(f"Average daily occupancy: {occupancy.mean():.2f} beds")
    
    # ICU ratio
    if 'encounters' in ca_data:
        print("\n🏥 Calculating ICU ratio...")
        icu_ratio = calculate_icu_ratio(ca_data['encounters'])
        features['icu_ratio'] = icu_ratio
    
    # Oxygen per patient
    if 'procedures' in ca_data and 'encounters' in ca_data:
        print("\n💨 Calculating oxygen usage per patient...")
        oxygen_pp = calculate_oxygen_per_patient(
            ca_data['procedures'], 
            ca_data['encounters']
        )
        features['oxygen_per_patient'] = oxygen_pp
    
    # Time features
    if 'encounters' in ca_data:
        print("\n📅 Creating time-based features...")
        ca_data['encounters'] = create_time_features(ca_data['encounters'])
        print("Added: year, month, day_of_week, quarter, is_weekend")
    
    return features
