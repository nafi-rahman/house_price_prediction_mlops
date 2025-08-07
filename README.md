# MLOps House Price Prediction 🏡

An end-to-end MLOps project for predicting house prices in King County, USA. This repository demonstrates a production-ready machine learning workflow, focusing on **data quality**, **versioning**, and **pipeline automation** using modern MLOps tools.

### 📖 Table of Contents

- [Core Technologies]
- [Master Plan]
- [Getting Started]
- [Project Structure]
- [What's Next]

### 🛠️ Core Technologies

- **Python 🐍:** The primary language for all scripts.
- **Poetry 📦:** For dependency management and project isolation.
- **DVC (Data Version Control) 💾:** To version and manage the raw dataset.
- **Great Expectations 📝:** To enforce data quality and create living documentation for our raw data.
- **Git 🌳:** For version control of all code and configurations.

### 🗺️ Master Plan

This project is structured into several phases to build a complete MLOps pipeline.

### Phase 0: Project Setup & Foundational Engineering (✅ Complete)

This phase established a professional and scalable project structure.

- **Project Scaffolding:** Created a clean Python package structure with subdirectories for `data/`, `models/`, `configs/`, `notebooks/`, and `src/`. The `src/` directory contains modular scripts for each pipeline stage.
- **Dependency Management:** Used **Poetry** to manage dependencies. A `pyproject.toml` file declares project dependencies, and a `poetry.lock` file ensures perfect reproducibility.
- **Configuration Management:** Implemented a configuration file (`configs/config.yaml`) to store all hyperparameters, file paths, and environment settings.
- **Version Control:** Initialized a Git repository and created a `.gitignore` file to exclude large files and virtual environments.

### Phase 1: Data Versioning, Validation & Preprocessing (DVC + Great Expectations) (✅ In Progress)

This phase establishes the data foundation of your pipeline, focusing on quality and traceability.

- **Done:** The raw `kc_house_data.csv` dataset has been versioned using **DVC**. A robust data quality gate has been implemented with **Great Expectations 1.x** to validate the raw data's schema and content. Our Great Expectations project is configured, and an `ExpectationSuite` named `kc_house_raw` has been defined. The `src/data_loader.py` script now uses this suite to validate the data before any further processing.
- **Remaining:** The next step is to develop a preprocessing script (`src/preprocess_data.py`) to handle cleaning, feature engineering, and encoding. We will then version the processed data using DVC.

### Phase 2: Model Training & Advanced Experiment Tracking (MLflow + Optuna) (⏳ Upcoming)

- Refine the training script (`src/train.py`) to use **Optuna** for sophisticated hyperparameter optimization.
- Integrate **MLflow** into the training script to log every run, including parameters, metrics (RMSE, MAE, R²), and model artifacts.
- Programmatically register the champion model to the MLflow Model Registry.

### Phase 3: Orchestration & Workflow Automation (Prefect) (⏳ Upcoming)

- Use **Prefect** to define a workflow that orchestrates the entire pipeline.
- Implement a feedback loop by configuring a trigger for the Prefect flow, such as a scheduled nightly run.
- Add robust error handling to automatically retry tasks on failure.

### Phase 4: Model Serving & User Interface (FastAPI + Streamlit) (⏳ Upcoming)

- Develop a Python script (`src/serve.py`) using **FastAPI** to create a REST API endpoint.
- Build a simple **Streamlit** application to serve as a front-end, making requests to the FastAPI endpoint.
- Deploy the Streamlit UI and the FastAPI backend to a free PaaS tier.

### Phase 5: Containerization & CI/CD (GitHub Actions + Docker) (⏳ Upcoming)

- Create two multi-stage **Dockerfiles**: one for the training pipeline and a lightweight image for the FastAPI serving application.
- Define a **GitHub Actions** workflow triggered on a push to the main branch to automate the CI/CD pipeline.

### Phase 6: Monitoring & Model Governance (Evidently/DVC-Live + MLflow) (⏳ Upcoming)

- Use **Evidently** to monitor for data and model drift.
- Configure a scheduled job to compare production data to training data and generate a drift report.
- Document a rollback procedure using the MLflow Model Registry.

### ▶️ Getting Started

Follow these steps exactly to set up and run the project from a fresh clone.

### Prerequisites

- Python 3.10+
- Git
- DVC (Data Version Control)

### Setup

1. Clone the repository and navigate into the project directory:
    
    ```
    git clone <repository-url>
    cd mlops-house-price-prediction
    
    ```
    
2. Install Poetry and the project dependencies:
    
    ```
    pip install poetry
    poetry install
    
    ```
    
3. Activate the Poetry shell:
    
    ```
    poetry shell
    
    ```
    

### Running the Project

1. **Pull the raw dataset** using DVC. This will download the `kc_house_data.csv` file:
    
    ```
    dvc pull
    
    ```
    
2. **Create the Great Expectations expectation suite.** The script `scripts/create_expectation_suite.py` will generate the `kc_house_raw.json` file and build the `Data Docs`.
    
    ```
    python scripts/create_expectation_suite.py
    
    ```
    
    A browser window will open showing the Data Docs report. You can close this window after reviewing.
    
3. **Run the data loader script** to validate the raw data. This script uses the Great Expectations suite we just created, as configured in `configs/config.yaml`.
    
    ```
    python src/data_loader.py
    
    ```
    
    **Expected Output:** You should see a message indicating "Data validation successful!" followed by the head of the DataFrame, confirming that our data quality gate is working as intended.
    

### 📂 Project Structure

```
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

```

### 🚀 What's Next

With data validation successfully implemented, we are now ready to begin the next task in Phase 1: **Data Preprocessing**. We will create `src/preprocess_data.py` to prepare our validated dataset for the model training phase.
