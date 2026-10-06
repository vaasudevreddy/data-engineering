# Day 15 — ETL Reliability, Retry, Idempotency and Backfill

## Objective

Build a reliable Extract, Transform, Load (ETL) pipeline that can safely handle failures, retries, repeated execution, and historical data reprocessing.

## Pipeline Flow

```text
Source CSV
    ↓
Extract Orders
    ↓
Retry Mechanism
    ↓
Database Transaction
    ↓
Idempotent Load
    ↓
PostgreSQL