# Day 13 — Schema Evolution and Metadata-Driven Pipeline

## Overview

Day 13 focuses on two important Data Engineering concepts:

- Schema evolution
- Metadata-driven pipelines

The project demonstrates how a pipeline can detect changes in source data structure and process different datasets using the same pipeline code.

## Technologies

- Python
- PostgreSQL
- CSV
- psycopg
- python-dotenv
- Git

## Project Structure

```text
day13/
├── source_orders.csv
├── source_customers.csv
├── config.py
├── metadata.py
├── schema.py
├── extract.py
├── validate.py
├── database.py
├── pipeline.py
└── README.md

