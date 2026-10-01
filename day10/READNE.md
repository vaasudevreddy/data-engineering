# Day 10 — Incremental Data Loading with Python and PostgreSQL

## Overview

This project demonstrates how to build an incremental data pipeline using Python and PostgreSQL.

Instead of processing the entire source dataset every time the pipeline runs, the pipeline keeps track of the last successfully processed record using a watermark.

The pipeline processes only new records during subsequent executions.

The project demonstrates important Data Engineering concepts such as:

- Full loading
- Incremental loading
- Watermarks
- High-water marks
- Upserts
- Idempotency
- Duplicate prevention
- PostgreSQL transactions
- Pipeline state management
- Failure and restart concepts

---

## Architecture

```text
                    source_orders.csv
                           |
                           v
                    Python Pipeline
                           |
                    Read Watermark
                           |
                           v
                 Find New Orders
                           |
                           v
                      Transform
                           |
                           v
                     PostgreSQL
                    /           \
                   /             \
                  v               v
       incremental_orders    pipeline_watermark