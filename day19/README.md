# Day 19 – End-to-End Data Pipeline with Apache Airflow

## Objective
Build and execute a data-processing pipeline orchestrated by Apache Airflow.

## Project Structure
- `data/orders.csv` — input orders dataset
- `data/processed_orders.csv` — processed output
- `process_orders.py` — Python data-processing script

## Pipeline Workflow
1. Read order data from a CSV file.
2. Convert quantity and price into numeric values.
3. Calculate each order's total value.
4. Write the processed records to a new CSV file.

## Airflow Implementation
- Workflow ID: `day19_orders_pipeline`
- Task: `process_orders`
- Used Docker Compose to run Apache Airflow.
- Mounted the Day 19 project folder into the Airflow containers.
- Executed the Python script through an Airflow task.

## Validation
- Successfully processed 8 orders.
- Verified the generated output file.
- Confirmed that the Airflow task completed successfully.

## Technologies
- Python
- Apache Airflow 3.3.2
- Docker Compose
- CSV data processing

## Key Takeaway
Apache Airflow can orchestrate Python data-processing scripts, monitor execution, and provide logs for troubleshooting.



## Day 20 – Data Quality and Validation

- Created `validate_orders.py` to validate input data.
- Checked required fields for missing values.
- Detected duplicate order identifiers.
- Validated numeric quantities and prices.
- Rejected zero or negative quantities and negative prices.
- Tested duplicate data and confirmed validation fails.
- Integrated validation into the Airflow workflow.
- Confirmed processing is blocked when validation fails.
- Verified that valid data passes validation and processes successfully.

## Key Takeaway

Data validation before processing helps prevent invalid records from entering a data pipeline.


## Day 21 — Logging and Error Handling

- Added Python logging to `validate_orders.py`.
- Logged the start of validation and the input filename.
- Logged successful validation with the number of orders checked.
- Logged validation errors and exited with a non-zero status when validation failed.
- Verified the validation task and processing task in Apache Airflow.

**Result:** The validation task successfully checked all 8 orders, and the processing task completed successfully.


## Day 22 — Configurable Input Files

- Updated `validate_orders.py` to accept an input CSV filename as a command-line argument.
- Updated `process_orders.py` to accept an input CSV filename instead of always using `orders.csv`.
- Updated the Apache Airflow pipeline to pass the selected filename to both tasks.
- Tested the processing script locally and verified the Airflow pipeline successfully.

**Result:** Both validation and processing tasks completed successfully using `orders.csv`.



## Day 23 — Environment-Based Configuration

- Added the `ORDERS_INPUT_FILE` environment variable to the shared Airflow Docker Compose configuration.
- Updated `day19_pipeline.py` to read the input filename using Python's `os.getenv()`.
- Updated both validation and processing tasks to use the configured filename.
- Verified that Docker Compose resolves `ORDERS_INPUT_FILE` to `orders.csv`.
- Confirmed that the Airflow validation and processing tasks succeeded.

**Key learning:** Environment variables separate configuration from application code, making pipelines easier to configure across environments.



## Day 24 — Robust CSV Validation

- Added checks for empty CSV files.
- Added checks for missing required column headers.
- Preserved existing validation for required values, duplicate order IDs, quantities, and prices.
- Tested valid input, missing columns, and empty files.
- Removed temporary test files and verified the original 8 orders still pass validation.
- Verified the updated validation and processing tasks in Apache Airflow.

**Result:** Both Airflow tasks completed successfully with the normal input file.





## Day 25: Automated Testing

Created automated tests using pytest to verify order data validation.

### Tests implemented
- Valid orders pass validation.
- Empty CSV files are rejected.
- CSV files with missing required columns are rejected.

### Full test suite
Command:
`python3 -m pytest -v`

Result: 13 tests passed.

### Key concepts learned
- Automated testing with pytest
- Assertions and exit codes
- Testing invalid input
- Temporary files using pytest's `tmp_path` fixture
- Running tests across multiple project directories





## Day 26: Testing Data Processing

Created automated tests for the order-processing script using pytest.

### Tests implemented
- Verify that processed order totals match calculations from the original input.
- Verify that invalid numeric quantities cause processing to fail.
- Run processing tests alongside existing validation tests.

### Full test suite
Command:
`python3 -m pytest -v`

Result: 15 tests passed.

### Key concepts learned
- Testing data transformations
- Comparing expected and actual results
- Testing invalid numeric input
- Checking process exit codes
- Running the complete test suite




## Day 27: Safer Data Processing

Improved the order-processing script to reject invalid input before writing output.

### Improvements
- Reject empty CSV files.
- Reject non-numeric quantities and prices.
- Reject quantities that are zero or negative.
- Reject negative prices.
- Preserve existing output when input validation fails.

### Testing
Command: `python3 -m pytest -v`

Result: 16 tests passed.

### Key concepts learned
- Input validation
- Exception handling
- Safe output management
- Regression testing





## Day 28: Safe Output Writing

Updated the order-processing pipeline to write results to a temporary file before replacing the final output.

### Improvements
- Write processed orders to a temporary file.
- Replace the final output only after the temporary write succeeds.
- Clean up the temporary file when writing fails.
- Test that existing output is preserved when the temporary output path cannot be opened.

### Testing
Command: `python3 -m pytest -v`

Result: 17 tests passed.

### Key concepts learned
- Temporary files
- Safe output replacement
- Exception handling and cleanup
- Testing file-writing failures





## Day 29 — Reusable Processing Functions

- Created a reusable `calculate_total()` function.
- Refactored order processing into a `process_orders()` function.
- Used `if __name__ == "__main__":` to separate imports from script execution.
- Added a unit test for the total calculation.
- Verified all 18 automated tests pass.
- Confirmed the pipeline processes all 8 orders successfully.







## Day 30 — Modular Order Processing Pipeline

- Created `load_orders()` to read input data.
- Created `validate_and_process_orders()` to validate orders and calculate totals.
- Created `write_orders()` to save output safely using a temporary file.
- Kept `process_orders()` as the main pipeline coordinator.
- Added a unit test for `write_orders()`.
- Verified all 19 automated tests pass.
- Confirmed the pipeline processes all 8 orders successfully.

### Key Learning

Separation of concerns: each function has a specific responsibility, making the pipeline easier to test, maintain, and reuse.

