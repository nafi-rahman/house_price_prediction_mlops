#!/usr/bin/env python3
"""
Phase-1 data-quality gate for kc_house_data.csv
- Reads CSV into a pandas DataFrame
- Creates / updates an ExpectationSuite
- Runs a Checkpoint → generates Data Docs
- Exits 0 on success, 1 on failure
"""

import pathlib
import sys
import pandas as pd
import great_expectations as gx
from great_expectations.checkpoint import UpdateDataDocsAction

# ------------------------------------------------------------------
# 1. Data Context
# ------------------------------------------------------------------
context = gx.get_context()   # now always a FileDataContext
# context = context.convert_to_file_context() #run once for folder in scripts/gx


# ------------------------------------------------------------------
# 2. Pandas Data Source + Data Asset (idempotent)
# ------------------------------------------------------------------
if "kc_house_datasource" in context.data_sources.all():
    data_source = context.data_sources.get("kc_house_datasource")
else:
    data_source = context.data_sources.add_pandas(name="kc_house_datasource")

data_asset = data_source.add_dataframe_asset(name="kc_house_data")
batch_def = data_asset.add_batch_definition_whole_dataframe("whole_file")

# ------------------------------------------------------------------
# 3. Load CSV
# ------------------------------------------------------------------
csv_path = pathlib.Path(__file__).resolve().parent.parent / "data" / "raw" / "kc_house_data.csv"
if not csv_path.exists():
    raise FileNotFoundError(csv_path)

df = pd.read_csv(csv_path)

# ------------------------------------------------------------------
# 4. Expectation Suite – realistic rules for this CSV
# ------------------------------------------------------------------
suite_name = "kc_house_raw"

suite = context.suites.add_or_update(
    gx.ExpectationSuite(
        name=suite_name,
        expectations=[
            # Core columns present & ordered
            gx.expectations.ExpectTableColumnsToMatchOrderedList(
                column_list=[
                    "id", "date", "price", "bedrooms", "bathrooms", "sqft_living",
                    "sqft_lot", "floors", "waterfront", "view", "condition", "grade",
                    "sqft_above", "sqft_basement", "yr_built", "yr_renovated",
                    "zipcode", "lat", "long", "sqft_living15", "sqft_lot15"
                ]
            ),
            # Non-null critical fields
            gx.expectations.ExpectColumnValuesToNotBeNull(column="price"),
            gx.expectations.ExpectColumnValuesToNotBeNull(column="bedrooms"),
            gx.expectations.ExpectColumnValuesToNotBeNull(column="bathrooms"),
            # Value ranges that fit the sample
            gx.expectations.ExpectColumnValuesToBeBetween(
                column="price", min_value=1e4, max_value=1e7
            ),
            gx.expectations.ExpectColumnValuesToBeBetween(
                column="bedrooms", min_value=0, max_value=33   # 33 is present!
            ),
            gx.expectations.ExpectColumnValuesToBeBetween(
                column="bathrooms", min_value=0, max_value=10
            ),
            gx.expectations.ExpectColumnValuesToBeInSet(
                column="waterfront", value_set=[0, 1]
            ),
        ]
    )
)

# ------------------------------------------------------------------
# 5. Validation Definition
# ------------------------------------------------------------------
validation_def = gx.ValidationDefinition(
    data=batch_def,
    suite=suite,
    name="kc_house_validation",
)
context.validation_definitions.add(validation_def)

# ------------------------------------------------------------------
# 6. Checkpoint (builds Data Docs)
# ------------------------------------------------------------------
checkpoint = gx.Checkpoint(
    name="kc_house_checkpoint",
    validation_definitions=[validation_def],
    actions=[UpdateDataDocsAction(name="update_all_data_docs")],
)
context.checkpoints.add(checkpoint)

# ------------------------------------------------------------------
# 7. Run the checkpoint
# ------------------------------------------------------------------
checkpoint_result = checkpoint.run(batch_parameters={"dataframe": df})

# ------------------------------------------------------------------
# 8. Report & exit
# ------------------------------------------------------------------
print("Checkpoint passed:", checkpoint_result.success)

# Iterate over each ValidationDefinition that ran
for validation_def_name, suite_validation_result in checkpoint_result.run_results.items():
    print(f"\nValidation Definition: {validation_def_name}")
    for expectation_result in suite_validation_result.results:
        print(f"  {expectation_result.expectation_config.type}: "
              f"{'✅' if expectation_result.success else '❌'}")

# Open Data Docs (built by UpdateDataDocsAction)
context.open_data_docs()

if not checkpoint_result.success:
    sys.exit(1)
