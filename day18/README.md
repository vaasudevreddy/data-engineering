# Day 18 – Apache Airflow Retries and Failure Handling

## Objective
Learn how Apache Airflow handles task failures and automatically retries unsuccessful tasks.

## What I Implemented
- Created a workflow named `day18_retries`.
- Created a task named `unreliable_task`.
- Simulated temporary failures using Python exceptions.
- Configured two retries with a 10-second delay between attempts.
- Verified that the task failed on its first attempt and succeeded on its second attempt.

## Key Concepts
- **Retries:** Automatically rerun a failed task.
- **Retry delay:** The waiting time before another attempt.
- **Exception handling:** An exception can mark a task attempt as failed.
- **Task monitoring:** Airflow logs and the user interface show task status and attempt history.

## Technologies
- Python
- Apache Airflow 3.3.2
- Docker Compose

## Result
The task failed on its first attempt and succeeded on its second attempt, demonstrating automatic retry functionality.

## Key Takeaway
Retries improve pipeline reliability when tasks experience temporary failures.

