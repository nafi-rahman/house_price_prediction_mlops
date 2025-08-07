# src/data_loader.py

import great_expectations as gx
import pandas as pd
import os
import yaml

# Load configuration
with open("configs/config.yaml", "r") as f:
    config = yaml.safe_load(f)

RAW_DATA_PATH = config["data"]["raw_data_path"]
EXPECTATION_SUITE_NAME = config["great_expectations"]["expectation_suite_name"]
DATASOURCE_NAME = config["great_expectations"]["datasource_name"] # Added this to config.yaml
DATA_ASSET_NAME = config["great_expectations"]["data_asset_name"] # Added this to config.yaml

def load_and_validate_data(data_path: str = RAW_DATA_PATH, suite_name: str = EXPECTATION_SUITE_NAME) -> pd.DataFrame:
    """
    Loads raw data and validates it using Great Expectations.

    Args:
        data_path (str): Path to the raw CSV data file.
        suite_name (str): Name of the Great Expectations suite to use for validation.

    Returns:
        pd.DataFrame: The loaded and validated DataFrame.

    Raises:
        ValueError: If data validation fails.
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Raw data file not found at: {data_path}")

    print(f"Loading data from {data_path}...")
    # Directly load with pandas for initial dataframe, then pass to GX validator
    df = pd.read_csv(data_path)
    print(f"Data loaded successfully. Shape: {df.shape}")

    print(f"Validating data against Expectation Suite: '{suite_name}'...")
    try:
        context = gx.get_context()
        
        # Get the data asset and build a batch request
        datasource = context.get_datasource(DATASOURCE_NAME)
        data_asset = datasource.get_asset(DATA_ASSET_NAME)
        batch_request = data_asset.build_batch_request(options={"path": data_path})

        # Get a validator for the batch and suite
        validator = context.get_validator(
            batch_request=batch_request,
            expectation_suite_name=suite_name
        )

        # Validate the data
        validation_result = validator.validate() # No need to pass suite_name again if already in get_validator

        if not validation_result.success:
            print("Data validation failed!")
            # Build and open Data Docs for detailed report
            context.build_data_docs()
            context.open_data_docs() # This will open the browser
            raise ValueError("Raw data failed Great Expectations validation. Check Data Docs for details.")
        else:
            print("Data validation successful!")
            return df

    except Exception as e:
        print(f"An error occurred during data validation: {e}")
        raise

if __name__ == "__main__":
    # Example usage:
    # First, ensure you have run the manual GX setup and `scripts/create_expectation_suite.py`
    try:
        validated_df = load_and_validate_data()
        print("\nValidated DataFrame head:")
        print(validated_df.head())
    except ValueError as e:
        print(f"Pipeline halted due to: {e}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
