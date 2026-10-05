# Day 14 — Data Quality and Automated Testing

## Objective

Build a production-style data pipeline with data quality validation and automated tests.

## Pipeline Flow

CSV Source
→ Schema Validation
→ Data Extraction
→ Data Quality Checks
→ PostgreSQL
→ Automated Tests

## Project Structure

```text
day14/
├── source_customers.csv
├── config.py
├── metadata.py
├── schema.py
├── extract.py
├── quality.py
├── database.py
├── pipeline.py
├── tests/
│   └── test_quality.py
└── README.md