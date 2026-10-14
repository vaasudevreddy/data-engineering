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