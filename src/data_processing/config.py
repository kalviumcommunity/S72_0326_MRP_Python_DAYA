"""Configuration for data paths and parameters."""

from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASETS_DIR = BASE_DIR / "Datasets"
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FEATURES_DIR = DATA_DIR / "features"
OUTPUTS_DIR = BASE_DIR / "outputs"

# Dataset paths
CA_HOSPITAL_DIR = DATASETS_DIR / "Ca"
ICU_DIR = DATASETS_DIR / "ICU"
HOSPITAL_RECORDS_DIR = DATASETS_DIR / "Hospitals Records"

# CA Hospital dataset files
CA_DATASETS = {
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

# Create directories if they don't exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, FEATURES_DIR, OUTPUTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
