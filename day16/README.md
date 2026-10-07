# Day 16 — Logging and Observability

## Objective

Add structured logging to a data pipeline so that pipeline execution, database operations, successful steps, and failures can be tracked.

## Pipeline Flow

```text
Source CSV
    ↓
Extract Orders
    ↓
PostgreSQL
    ↓
Load Orders
    ↓
Pipeline Completion