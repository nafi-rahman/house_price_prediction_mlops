# This script will download the Kaggle House Sales in King County, USA dataset and initialize DVC for it.
# It assumes you have Kaggle API credentials set up (kaggle.json in ~/.kaggle/).

import os
import subprocess
import shutil

# --- Configuration ---
KAGGLE_SLUG = "harlfoxem/housesalesprediction"
KAGGLE_CSV_NAME = "kc_house_data.csv"
RAW_DATA_DIR = "data/raw"
FULL_DATASET_PATH = os.path.join(RAW_DATA_DIR, KAGGLE_CSV_NAME)
# -------------------

def download_kaggle_dataset():
    """Downloads the specified Kaggle dataset."""
    print(f"Ensuring directory {RAW_DATA_DIR} exists...")
    os.makedirs(RAW_DATA_DIR, exist_ok=True)

    print(f"Attempting to download Kaggle dataset '{KAGGLE_SLUG}' to {RAW_DATA_DIR}...")
    try:
        # Construct the kaggle command
        kaggle_command = ["kaggle", "datasets", "download", "-d", KAGGLE_SLUG, "-p", RAW_DATA_DIR, "--unzip"]
        
        # Use subprocess to run the kaggle command
        subprocess.run(kaggle_command, check=True)
        print(f"Dataset downloaded and unzipped to {FULL_DATASET_PATH}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading Kaggle dataset: {e}")
        print("Please ensure you have the Kaggle API installed and configured (kaggle.json in ~/.kaggle/).")
        print("You might need to install it: pip install kaggle")
        print("And configure it by downloading your API token from Kaggle and placing it in ~/.kaggle/kaggle.json")
        # Exit if download fails, as subsequent steps depend on it
        exit(1)
    except FileNotFoundError:
        print("Kaggle command not found. Please ensure Kaggle API is installed and in your PATH.")
        exit(1)

def initialize_dvc_for_data():
    """Initializes DVC and adds the raw dataset."""
    print(f"Adding {FULL_DATASET_PATH} to DVC...")
    try:
        # Add the raw dataset to DVC
        subprocess.run(["dvc", "add", FULL_DATASET_PATH], check=True)
        print(f"Successfully added {FULL_DATASET_PATH} to DVC.")
        print("Remember to commit the generated .dvc file to Git: git add data/raw/kc_house_data.csv.dvc")
        print("And ensure .gitignore correctly ignores the actual data file (data/raw/kc_house_data.csv).")
    except subprocess.CalledProcessError as e:
        print(f"Error adding data to DVC: {e}")
        print("Please ensure DVC is installed and initialized in this project.")
        print("You might need to run: dvc init")
        exit(1)

if __name__ == "__main__":
    download_kaggle_dataset()
    initialize_dvc_for_data()

    # Optional: Verify DVC status
    print("\nVerifying DVC status:")
    try:
        subprocess.run(["dvc", "status"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error checking DVC status: {e}")

