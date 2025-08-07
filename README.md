MLOps House Price Prediction 🏡
An end-to-end MLOps project for predicting house prices in King County, USA. This repository demonstrates a production-ready machine learning workflow, focusing on data quality, versioning, and pipeline automation using modern MLOps tools.

📖 Table of Contents
Core Technologies

Master Plan

Getting Started

Project Structure

What's Next

🛠️ Core Technologies
Python 🐍: The primary language for all scripts.

Poetry 📦: For dependency management and project isolation.

DVC (Data Version Control) 💾: To version and manage the raw dataset.

Great Expectations 📝: To enforce data quality and create living documentation for our raw data.

Git 🌳: For version control of all code and configurations.

🗺️ Master Plan
This project is structured into four main phases to build a complete MLOps pipeline.

Phase 1: Data Versioning, Validation & Preprocessing (✅ In Progress)
Done: The raw kc_house_data.csv dataset has been versioned using DVC. A robust data quality gate has been implemented with Great Expectations 1.x to validate the raw data's schema and content. Our Great Expectations project is configured to be a FileDataContext, and an ExpectationSuite named kc_house_raw has been defined and saved. The src/data_loader.py script now uses this suite to validate the data before any further processing.

Remaining: The next step is to build a preprocessing script (src/preprocess_data.py) to clean the data, handle missing values, and engineer new features. We will then version the processed data using DVC.

Phase 2: Model Training & Evaluation (⏳ Upcoming)
Train a regression model on the preprocessed data.

Track model artifacts, hyperparameters, and performance metrics using an experiment tracker (e.g., MLflow).

Select the best-performing model for deployment.

Phase 3: Model Packaging & CI/CD (⏳ Upcoming)
Containerize the trained model using Docker.

Automate the pipeline using a CI/CD tool (e.g., GitHub Actions) to retrain the model when new data or code is committed.

Phase 4: Deployment & Monitoring (⏳ Upcoming)
Deploy the model as a production API endpoint.

Set up monitoring to track model performance, data drift, and model drift in a live environment.

▶️ Getting Started
Follow these steps exactly to set up and run the project from a fresh clone.

Prerequisites
Python 3.10+

Git

DVC (Data Version Control)

Setup
Clone the repository and navigate into the project directory:

git clone <repository-url>
cd mlops-house-price-prediction

Install Poetry and the project dependencies:

pip install poetry
poetry install

Activate the Poetry shell:

poetry shell

Running the Project
Pull the raw dataset using DVC. This will download the kc_house_data.csv file:

dvc pull

Create the Great Expectations expectation suite. The script scripts/create_expectation_suite.py will generate the kc_house_raw.json file and build the Data Docs.

python scripts/create_expectation_suite.py

A browser window will open showing the Data Docs report. You can close this window after reviewing.

Run the data loader script to validate the raw data. This script uses the Great Expectations suite we just created, as configured in configs/config.yaml.

python src/data_loader.py

Expected Output: You should see a message indicating "Data validation successful!" followed by the head of the DataFrame, confirming that our data quality gate is working as intended.

📂 Project Structure
.
├── configs/
│   └── config.yaml             # Project-wide configuration for file paths and parameters
├── data/
│   ├── raw/
│   │   └── kc_house_data.csv   # Raw dataset (DVC-tracked)
│   └── processed/              # Processed data will be stored here
├── great_expectations/         # Great Expectations project folder
│   ├── expectations/
│   │   └── kc_house_raw.json   # Our saved expectation suite
│   ├── great_expectations.yml  # Main GX configuration file
│   └── uncommitted/
│       └── data_docs/          # HTML validation reports (ignored by Git)
├── scripts/
│   └── create_expectation_suite.py # Script to define our data quality rules
├── src/
│   └── data_loader.py          # Loads and validates raw data
├── .dvcignore
├── .gitignore
├── pyproject.toml
└── README.md

🚀 What's Next
With data validation successfully implemented, we are now ready to begin the next task in Phase 1: Data Preprocessing. We will create src/preprocess_data.py to prepare our validated dataset for the model training phase.