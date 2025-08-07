# MLOps House Price Prediction 🏡

An end-to-end MLOps project for predicting house prices in King County, USA. This repository demonstrates a production-ready machine learning workflow, focusing on **data quality**, **versioning**, and **pipeline automation** using modern MLOps tools.

### 📖 Table of Contents

- Core Technologies
- Master Plan
- Getting Started
- Project Structure
- What's Next

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

### Phase 1: Data Versioning, Validation & Preprocessing (DVC + Great Expectations) (✅ Complete)

This phase establishes the data foundation of your pipeline, focusing on quality and traceability.

- **Done:** The raw `kc_house_data.csv` dataset has been versioned using **DVC**. A robust data quality gate has been implemented with **Great Expectations 1.x** to validate the raw data's schema and content. An `ExpectationSuite` named `kc_house_raw` has been defined. The `src/data_loader.py` script now uses this suite to validate the data.
- **Done:** A preprocessing script (`src/preprocess_data.py`) has been developed and executed. This script cleans the data, engineers new features, and encodes categorical variables. The processed data is now available at `data/processed/kc_house_data_processed.csv`.
- **Remaining:** The final step for this phase is to version the processed data using DVC.

### Phase 2: Model Training & Advanced Experiment Tracking (MLflow + Optuna) (✅ In Progress)

- We are currently preparing to train a regression model on the preprocessed data.
- This phase will use **Optuna** for sophisticated hyperparameter optimization.
- We will integrate **MLflow** into the training script to log every run, including parameters, metrics, and model artifacts.
- The best-performing model will be programmatically registered to the MLflow Model Registry.

### Phase 3: Orchestration & Workflow Automation (Prefect) (⏳ Upcoming)

- Use **Prefect** to define a workflow that orchestrates the entire pipeline.
- Implement a feedback loop by configuring a trigger for the Prefect flow.

### Phase 4: Model Serving & User Interface (FastAPI + Streamlit) (⏳ Upcoming)

- Develop a Python script (`src/serve.py`) using **FastAPI** to create a REST API endpoint.
- Build a simple **Streamlit** application to serve as a front-end.

### Phase 5: Containerization & CI/CD (GitHub Actions + Docker) (⏳ Upcoming)

- Create two multi-stage **Dockerfiles** for the training pipeline and serving application.
- Define a **GitHub Actions** workflow to automate the CI/CD pipeline.

### Phase 6: Monitoring & Model Governance (Evidently/DVC-Live + MLflow) (⏳ Upcoming)

- Use **Evidently** to monitor for data and model drift.
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
    
4. **Run the data preprocessing script.** This script will load the validated data, clean it, engineer new features, and save the processed data.
    
    ```
    python src/preprocess_data.py
    
    ```
    
    **Expected Output:** You should see messages confirming that data validation and preprocessing were successful, followed by the head of the processed DataFrame.
    

### 📂 Project Structure

```
.
├── configs/
│   └── config.yaml             # Project-wide configuration for file paths and parameters
├── data/
│   ├── raw/
│   │   └── kc_house_data.csv   # Raw dataset (DVC-tracked)
│   └── processed/
│       └── kc_house_data_processed.csv # Processed dataset
├── great_expectations/         # Great Expectations project folder
│   ├── expectations/
│   │   └── kc_house_raw.json   # Our saved expectation suite
│   ├── great_expectations.yml  # Main GX configuration file
│   └── uncommitted/
│       └── data_docs/          # HTML validation reports (ignored by Git)
├── scripts/
│   └── create_expectation_suite.py # Script to define our data quality rules
├── src/
│   ├── data_loader.py          # Loads and validates raw data
│   └── preprocess_data.py      # Cleans, engineers features, and saves processed data
├── .dvcignore
├── .gitignore
├── pyproject.toml
└── README.md

```

### 🚀 What's Next

With data validation and preprocessing complete, we are now officially ready to begin **Phase 2: Model Training & Advanced Experiment Tracking**. This next step will involve using the processed data to train a model and systematically track our experiments with MLflow.
