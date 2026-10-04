# Day 12 — Advanced Incremental Loading with Timestamp and Composite Watermarks

## Overview

Day 12 extends the incremental data pipeline developed in the previous days.

The earlier pipeline used an integer-based watermark:

```text
order_id > last_processed_id
```

This works well for detecting newly inserted records with increasing identifiers, but it has an important limitation:

> If an existing record is updated while keeping the same `order_id`, the pipeline may never detect that change.

Day 12 solves this problem by introducing **timestamp-based incremental loading** using an `updated_at` column.

The project then improves the timestamp strategy further by introducing a **composite watermark** consisting of:

```text
(updated_at, order_id)
```

This provides a more reliable processing position when multiple records share the same timestamp.

The project also introduces important production concepts including:

- Timestamp-based incremental loading
- Detection of updates to existing records
- Composite watermarks
- Late-arriving data
- Lookback windows
- Change Data Capture (CDC)
- Upsert operations
- Transaction management
- Idempotent processing

---

# Technologies Used

- Python
- PostgreSQL
- Psycopg
- python-dotenv
- CSV
- Git
- GitHub

---

# Project Structure

```text
day12/
│
├── source_orders.csv
├── config.py
├── logger.py
├── database.py
├── extract.py
├── validate.py
├── pipeline.py
└── README.md
```

---

# Pipeline Architecture

```text
                   Source CSV
                       |
                       v
              Read Composite Watermark
                       |
                       v
                 Extract Changes
                       |
                       v
                    Validate
                       |
                       v
                PostgreSQL Upsert
                       |
                       v
             Update Composite Watermark
                       |
                       v
                     Commit
                       |
                       v
              Pipeline Completed
```

The final processing position is represented by:

```text
updated_at + order_id
```

rather than only an order identifier.

---

# Source Data

The source CSV contains:

```text
order_id,customer,amount,updated_at
```

Example:

```text
1001,Alice,50,2026-10-01 10:00:00
1002,Bob,80,2026-10-01 10:05:00
1003,Charlie,120,2026-10-01 10:10:00
1004,David,200,2026-10-01 10:15:00
1005,Eva,150,2026-10-01 10:20:00
```

The important addition compared with the previous pipeline is:

```text
updated_at
```

This field represents when a record was last changed.

---

# Why an Order ID Watermark Is Not Enough

The previous incremental strategy used:

```text
order_id > last_processed_id
```

Consider this source:

```text
order_id | customer | amount
---------|----------|-------
1001     | Alice    | 50
1002     | Bob      | 80
1003     | Charlie  | 120
```

Assume the pipeline has processed through:

```text
last_processed_id = 1003
```

Later, order `1001` changes:

```text
1001 | Alice | 75
```

The identifier is still:

```text
1001
```

Therefore:

```text
1001 > 1003
```

is false.

The pipeline would miss the update.

---

# Timestamp-Based Incremental Loading

Day 12 introduces an `updated_at` field.

Example:

```text
order_id | customer | amount | updated_at
---------|----------|--------|--------------------
1001     | Alice    | 50     | 2026-10-01 10:00:00
1002     | Bob      | 80     | 2026-10-01 10:05:00
```

If order `1002` changes:

```text
1002 | Bob | 150 | 2026-10-03 10:30:00
```

the pipeline can detect the change using:

```text
updated_at > last_processed_timestamp
```

This allows the pipeline to detect both:

```text
New records
+
Updated records
```

---

# Initial Timestamp Watermark

The initial watermark is:

```text
1900-01-01 00:00:00
```

This timestamp is intentionally older than the source records.

Therefore, during the first run:

```text
source timestamp > initial watermark
```

is true for all source records.

The first execution therefore performs the initial load.

---

# First Pipeline Run

The first execution produced:

```text
Pipeline started
Last processed timestamp: 1900-01-01 00:00:00
Orders extracted: 5
Orders validated: 5
Watermark updated to: 2026-10-01 10:20:00
Pipeline completed successfully
```

The resulting watermark became:

```text
2026-10-01 10:20:00
```

---

# Detecting an Update to an Existing Record

To test update detection, order `1002` was changed.

Original:

```text
1002,Bob,80,2026-10-01 10:05:00
```

Updated:

```text
1002,Bob,150,2026-10-03 10:30:00
```

Notice that:

```text
order_id = 1002
```

did not change.

However:

```text
updated_at
```

changed from:

```text
2026-10-01 10:05:00
```

to:

```text
2026-10-03 10:30:00
```

The pipeline successfully detected the update.

The execution produced:

```text
Last processed timestamp: 2026-10-01 10:20:00
Orders extracted: 1
Orders validated: 1
Watermark updated to: 2026-10-03 10:30:00
Pipeline completed successfully
```

This demonstrates that timestamp-based incremental loading can detect updates to previously processed records.

---

# Upsert

The target table uses an upsert strategy.

An upsert combines:

```text
UPDATE
+
INSERT
```

The PostgreSQL operation uses:

```sql
INSERT INTO day12_orders
    (order_id, customer, amount, updated_at)
VALUES
    (%s, %s, %s, %s)
ON CONFLICT (order_id)
DO UPDATE SET
    customer = EXCLUDED.customer,
    amount = EXCLUDED.amount,
    updated_at = EXCLUDED.updated_at;
```

If an order does not exist:

```text
INSERT
```

If the order already exists:

```text
UPDATE
```

For example, order `1002` already existed in PostgreSQL.

When its amount changed from:

```text
80
```

to:

```text
150
```

the upsert updated the existing record instead of creating a duplicate.

---

# Limitation of a Timestamp-Only Watermark

A timestamp watermark is better than using only `order_id`, but it introduces another edge case.

Imagine two records:

```text
1006 | Alice | 60 | 2026-10-04 11:00:00
1007 | Bob   | 90 | 2026-10-04 11:00:00
```

Both records have exactly the same timestamp.

If the pipeline stores only:

```text
2026-10-04 11:00:00
```

as its watermark, the timestamp alone cannot describe which record at that timestamp was processed last.

This can create boundary problems in pipelines that process records in batches or resume after partial processing.

---

# Composite Watermark

To make the processing position more precise, the project was upgraded to use a composite watermark.

Instead of storing only:

```text
last_processed_timestamp
```

the pipeline stores:

```text
last_processed_timestamp
last_processed_order_id
```

Together they form:

```text
(updated_at, order_id)
```

Example:

```text
(2026-10-03 10:30:00, 1002)
```

The extraction condition becomes conceptually:

```text
updated_at > last_processed_timestamp

OR

updated_at = last_processed_timestamp
AND
order_id > last_processed_order_id
```

This creates a deterministic ordering when multiple records share the same timestamp.

---

# Composite Watermark Example

Suppose the current processing position is:

```text
2026-10-04 11:00:00 | 1006
```

Another record exists:

```text
2026-10-04 11:00:00 | 1007
```

The timestamps are equal:

```text
11:00:00 = 11:00:00
```

so the pipeline compares the second part:

```text
1007 > 1006
```

The record can therefore be identified as coming after the stored composite position.

---

# Composite Watermark Database Design

The final watermark table contains:

```sql
CREATE TABLE day12_watermark (
    pipeline_name VARCHAR(100) PRIMARY KEY,
    last_processed_timestamp TIMESTAMP,
    last_processed_order_id INT
);
```

The processing state can therefore look like:

```text
pipeline_name          | last_processed_timestamp | last_processed_order_id
-----------------------|--------------------------|------------------------
day12_orders_pipeline  | 2026-10-03 10:30:00      | 1002
```

---

# Finding the Latest Processing Position

After processing a batch, the pipeline determines the latest record using:

```python
latest_order = max(
    valid_orders,
    key=lambda order: (
        order["updated_at"],
        order["order_id"]
    )
)
```

Records are therefore ordered first by:

```text
updated_at
```

and then by:

```text
order_id
```

The watermark is updated using both values.

---

# Final Composite Watermark Test

After upgrading the pipeline, the existing database position was:

```text
Last processed timestamp: 2026-10-03 10:30:00
Last processed order ID: 1002
```

Running the pipeline without new source changes produced:

```text
Pipeline started
Last processed timestamp: 2026-10-03 10:30:00
Last processed order ID: 1002
Orders extracted: 0
No new or changed orders found
```

This confirmed that the upgraded pipeline could correctly read and use the composite watermark.

---

# Late-Arriving Data

Another important production problem is **late-arriving data**.

Suppose the current watermark is:

```text
2026-10-04 11:00:00
```

but a record arrives later with:

```text
updated_at = 2026-10-04 10:30:00
```

The record arrived after the pipeline had already moved beyond that timestamp.

A strict condition such as:

```text
updated_at > watermark
```

would miss it.

---

# Event Time vs Arrival Time

Late-arriving data demonstrates an important distinction.

## Event Time

When the event actually happened.

Example:

```text
10:30
```

## Arrival or Ingestion Time

When the data pipeline actually received the event.

Example:

```text
11:30
```

Therefore:

```text
Event Time != Arrival Time
```

Data does not always arrive in chronological order.

---

# Lookback Window

One strategy for handling late-arriving data is a lookback window.

Instead of processing only:

```text
updated_at > watermark
```

a pipeline may intentionally look backwards.

For example:

```text
watermark = 11:00
lookback  = 1 hour
```

The extraction window could begin at:

```text
10:00
```

This allows recently late-arriving records to be reconsidered.

Because the target uses upsert logic, already processed records can be processed again without creating duplicate primary keys.

---

# Lookback Trade-Off

A larger lookback provides:

```text
More protection against late data
```

but also:

```text
More records reprocessed
More database work
Higher processing cost
```

A smaller lookback provides:

```text
Less reprocessing
```

but increases:

```text
Risk of missing very late data
```

The appropriate lookback period depends on the characteristics of the source system.

---

# Change Data Capture

**Change Data Capture (CDC)** is a technique used to identify changes occurring in a source system.

Instead of repeatedly scanning records and comparing timestamps, a Change Data Capture system can identify operations such as:

```text
INSERT
UPDATE
DELETE
```

Example:

```text
INSERT  1001  Alice
INSERT  1002  Bob
UPDATE  1002  Robert
DELETE  1001
```

This allows downstream systems to process the actual changes made to the source.

---

# Why Change Data Capture Is Useful

Our timestamp-based pipeline handles:

```text
INSERT  ✅
UPDATE  ✅
```

However, deletes are more difficult.

Imagine the source originally contains:

```text
1001 Alice
1002 Bob
1003 Charlie
```

Later:

```text
1002 Bob
```

is deleted.

The next source snapshot may simply contain:

```text
1001 Alice
1003 Charlie
```

A timestamp-based extraction process does not automatically know that `1002` was deleted.

Change Data Capture can explicitly represent:

```text
DELETE 1002
```

which allows the target system to react appropriately.

---

# Timestamp Incremental Loading vs Change Data Capture

| Capability | Timestamp Watermark | Change Data Capture |
|---|---|---|
| Detect inserts | Yes | Yes |
| Detect updates | Yes | Yes |
| Detect deletes | Difficult | Yes |
| Requires `updated_at` | Usually | Not necessarily |
| Captures operation type | No | Yes |
| Complexity | Lower | Higher |
| Suitable for batch processing | Yes | Yes |
| Suitable for change streams | Limited | Yes |

---

# Example Change Data Capture Architecture

A more advanced architecture may look like:

```text
PostgreSQL
     |
     v
Database Change Log
     |
     v
Change Data Capture
     |
     v
Event Streaming Platform
     |
     v
Data Processing
     |
     +----------------+
     |                |
     v                v
Data Lake        Data Warehouse
```

Technologies such as Debezium can be used to capture database changes and publish change events.

Implementation of such infrastructure is outside the scope of this Day 12 project, but understanding why it exists is important for future data engineering work.

---

# Transaction Management

The pipeline loads records and updates the watermark as part of the same logical processing operation.

The intended sequence is:

```text
Extract
   |
   v
Validate
   |
   v
Load / Upsert
   |
   v
Update Watermark
   |
   v
Commit
```

If processing fails before the transaction is successfully committed:

```text
ROLLBACK
```

can be used to prevent partial database changes.

This helps keep the target data and processing state consistent.

---

# Idempotency

An idempotent operation can be repeated without producing an incorrect final state.

The project uses:

- Primary keys
- Upsert operations
- Watermarks
- Transactions

to make repeated processing safer.

For example, if an existing order is processed again, the upsert updates the existing row instead of blindly inserting another copy.

---

# Configuration Management

Database credentials are loaded using environment variables rather than being hard-coded into source files.

Example `.env` configuration:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=employee_management
DB_USER=postgres
DB_PASSWORD=your_password
```

The `.env` file must not be committed to Git.

It should be included in `.gitignore`:

```text
.env
```

---

# Logging

The pipeline records important execution information.

Example:

```text
2026-10-04 08:31:24,162 | INFO | Pipeline started
2026-10-04 08:31:24,178 | INFO | Last processed timestamp: 2026-10-03 10:30:00
2026-10-04 08:31:24,179 | INFO | Last processed order ID: 1002
2026-10-04 08:31:24,181 | INFO | Orders extracted: 0
2026-10-04 08:31:24,181 | INFO | No new or changed orders found
```

Logging helps with:

- Debugging
- Monitoring
- Understanding pipeline behavior
- Investigating failures

---

# Running the Pipeline

From the Day 12 directory:

```bash
python3 pipeline.py
```

The pipeline will:

1. Connect to PostgreSQL.
2. Create the required tables if necessary.
3. Retrieve the composite watermark.
4. Read the CSV source.
5. Identify new or changed records.
6. Validate the records.
7. Upsert the records into PostgreSQL.
8. Determine the latest composite processing position.
9. Update the watermark.
10. Commit the transaction.
11. Log the result.

---

# Evolution of the Incremental Pipeline

The project evolved through several stages.

## Stage 1 — ID-Based Watermark

```text
order_id > last_processed_id
```

Good for:

```text
New sequential records
```

Problem:

```text
Updates to old IDs can be missed
```

---

## Stage 2 — Timestamp Watermark

```text
updated_at > last_processed_timestamp
```

Improvement:

```text
Detect new records
+
Detect updated records
```

Problem:

```text
Multiple records can share the same timestamp
```

---

## Stage 3 — Composite Watermark

```text
(updated_at, order_id)
```

Improvement:

```text
Timestamp ordering
+
Deterministic tie-breaking
```

---

## Stage 4 — Late-Arriving Data Awareness

Problem:

```text
Records may arrive after the watermark has already advanced
```

Possible solution:

```text
Lookback window
+
Idempotent upsert
```

---

## Stage 5 — Change Data Capture

Advanced approach:

```text
Capture INSERT
Capture UPDATE
Capture DELETE
```

This provides a more complete representation of changes occurring in the source system.

---

# Key Concepts Learned

## 1. Timestamp-Based Incremental Loading

Use modification timestamps to detect new and updated records.

## 2. Composite Watermarks

Use multiple columns to define a deterministic processing position.

## 3. Update Detection

Detect changes to previously processed records without requiring a new primary key.

## 4. Upsert

Insert new records and update existing records safely.

## 5. Late-Arriving Data

Understand that event time and ingestion time may differ.

## 6. Lookback Windows

Reprocess a controlled historical window to reduce the risk of missing late data.

## 7. Change Data Capture

Capture inserts, updates, and deletes from a source system.

## 8. Transactions

Keep data changes and processing state consistent.

## 9. Idempotency

Make repeated execution safe.

## 10. Pipeline State

Persist the point from which future pipeline executions should continue.

---

# Day 12 Learning Outcome

Day 12 moves the project beyond basic incremental loading.

The pipeline evolved from:

```text
order_id watermark
```

to:

```text
timestamp watermark
```

and finally to:

```text
timestamp + order_id composite watermark
```

The project demonstrates why production data pipelines must consider more than simply finding records with larger identifiers.

Important real-world problems such as updates, identical timestamps, late-arriving data, and deletes require more robust incremental-processing strategies.

---

# Project Status

| Component | Status |
|---|---|
| Source CSV | Complete |
| Configuration | Complete |
| Environment Variables | Complete |
| Logging | Complete |
| PostgreSQL Integration | Complete |
| Data Validation | Complete |
| Timestamp Watermark | Complete |
| Update Detection | Complete |
| Upsert | Complete |
| Composite Watermark | Complete |
| Transaction Handling | Complete |
| Idempotent Processing | Complete |
| Late-Arriving Data Concept | Complete |
| Lookback Window Concept | Complete |
| Change Data Capture Concept | Complete |
| Documentation | Complete |

---

# Future Improvements

Future versions of the pipeline could include:

- Implemented lookback windows
- Ingestion timestamps
- Batch identifiers
- Pipeline execution history
- Audit tables
- Retry mechanisms
- Exponential backoff
- Dead-letter handling
- Data quality metrics
- Schema evolution handling
- Automated unit tests
- Integration tests
- Change Data Capture implementation
- Debezium
- Event streaming
- Apache Kafka
- Cloud storage
- Pipeline orchestration
- Monitoring and alerting
- Continuous Integration and Continuous Delivery (CI/CD)

---

# Conclusion

Day 12 demonstrates how incremental data pipelines evolve as real-world requirements become more complex.

A simple identifier watermark can detect new records, but it cannot reliably detect changes to existing records.

A timestamp watermark improves update detection, while a composite watermark provides a more precise processing position when timestamps are shared.

The project also introduces late-arriving data and Change Data Capture (CDC), establishing the conceptual foundation for more advanced batch and streaming data pipelines.

The final pipeline provides a stronger foundation for future work involving data warehouses, distributed processing, cloud platforms, orchestration, event streaming, and production-scale data engineering.

---

