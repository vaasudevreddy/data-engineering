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

