# Day 11 — Production-Style Incremental ETL Pipeline

## Overview

Day 11 focuses on building a modular, production-style **Extract, Transform, Load (ETL)** pipeline using Python and PostgreSQL.

The goal of this project is to move beyond a simple data-loading script and implement concepts commonly used in real-world data engineering pipelines.

The pipeline reads order data from a CSV source, identifies records that have not yet been processed, validates them, loads them into PostgreSQL, and updates a watermark that records the latest successfully processed order.

### Concepts covered

- Configuration management
- Environment variables
- Logging
- Modular pipeline architecture
- Data extraction
- Data validation
- Incremental loading
- Watermarking
- Upsert operations
- Transaction management
- Rollback and failure handling
- Error handling
- Pipeline orchestration
- Idempotent processing

---

# Architecture

```text
                         CSV Source
                             |
                             v
                    +------------------+
                    |   Configuration  |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |     Extract      |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |     Validate     |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |    PostgreSQL    |
                    |   Insert/Update  |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | Update Watermark |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |      Commit      |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | Pipeline Complete|
                    +------------------+