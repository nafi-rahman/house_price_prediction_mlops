#!/usr/bin/env python3
"""
This script loads the raw data, validates it using Great Expectations,
and returns a pandas DataFrame if the validation is successful.
"""
import pathlib
import sys
import pandas as pd
import great_expectations as gx

def load_data(
    data_file_path: pathlib.Path,
    gx_suite_name: str,
    gx_datasource_name: str,
    gx_data_asset_name: str,
) -> pd.DataFrame:
    """
    Loads data from a specified path and validates it using a Great Expectations suite.

    Args:
        data_file_path: The path to the data file.
        gx_suite_name: The name of the Great Expectations suite to use for validation.
        gx_datasource_name: The name of the Great Expectations datasource.
        gx_data_asset_name: The name of the Great Expectations data asset.

    Returns:
        A pandas DataFrame of the validated data.

    Raises:
        FileNotFoundError: If the data file does not exist.
        ValueError: If data validation fails.
    """
    print(f"Loading data from {data_file_path}...")
    if not data_file_path.exists():
        raise FileNotFoundError(f"Data file not found at: {data_file_path}")

    # Load the data into a pandas DataFrame
    df = pd.read_csv(data_file_path)

    # Get the Great Expectations context and validator
    context = gx.get_context()
    validator = context.get_validator(
        batch_definition_name=gx_data_asset_name,
        batch_identifiers={"dataframe": df},
        expectation_suite_name=gx_suite_name,
        datasource_name=gx_datasource_name,
    )

    # Validate the data
    print("Running Great Expectations data validation...")
    validation_result = validator.validate()

    if not validation_result.success:
        print("Data validation failed! ❌")
        # Build and open the data docs to see the report
        context.open_data_docs()
        raise ValueError("Data validation failed. Check Data Docs for details.")
    
    print("Data validation successful! ✅")
    return df

if __name__ == "__main__":
    # In a real pipeline, these values would come from a configuration file
    # For this example, we'll hardcode them to demonstrate the script
    config_file = pathlib.Path(__file__).resolve().parent.parent / "configs" / "config.yaml"
    if not config_file.exists():
        print(f"Error: {config_file} not found. Please create the config file.")
        sys.exit(1)

    import yaml
    with open(config_file) as f:
        config = yaml.safe_load(f)

    raw_data_path = pathlib.Path(__file__).resolve().parent.parent / config['data_paths']['raw_data_path']

    try:
        validated_df = load_data(
            data_file_path=raw_data_path,
            gx_suite_name=config['great_expectations']['suite_name'],
            gx_datasource_name=config['great_expectations']['datasource_name'],
            gx_data_asset_name=config['great_expectations']['data_asset_name'],
        )
        print("\nValidated DataFrame head:")
        print(validated_df.head())
    except (FileNotFoundError, ValueError) as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

