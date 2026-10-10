
# Day 17 - Apache Airflow Workflow Orchestration

## Overview

Today I learned how to use Apache Airflow to define, execute, and monitor data pipeline workflows. I ran Airflow locally using Docker Compose and created a workflow containing three dependent tasks.

## Learning Objectives

- Understand workflow orchestration.
- Understand Directed Acyclic Graphs (DAGs) and tasks.
- Define tasks using Python and the `@task` decorator.
- Set task dependencies using the `>>` operator.
- Trigger workflows manually through the Airflow web interface.
- Monitor task execution and inspect logs.
- Update a workflow and verify successful execution.

## Technologies Used

- Python
- Apache Airflow 3.3.2
- Docker
- Docker Compose
- PostgreSQL
- Redis

## Project Structure

```text
day17/
├── dags/
│   └── day17_hello.py
├── logs/
├── plugins/
├── docker-compose.yaml
└── README.md
```

## Workflow

The workflow is named `day17_hello` and contains three tasks:

```text
start → hello → finish
```

### Tasks

1. **start**: Prints a message indicating that the pipeline has started.
2. **hello**: Prints a greeting from Apache Airflow.
3. **finish**: Prints a message confirming that the pipeline has completed successfully.

Each task runs only after its upstream task succeeds.

## How It Works

The workflow is defined using Python:

```python
@task
def finish():
    print("Day 17 pipeline completed successfully!")

start() >> hello() >> finish()
```

The `@task` decorator defines an Airflow task. The `>>` operator establishes dependencies between tasks.

Because the workflow uses `schedule=None`, it is triggered manually rather than automatically on a schedule.

## Running the Workflow

1. Start Docker Desktop.
2. Navigate to the `day17` directory.
3. Start the Airflow services using Docker Compose.
4. Open `http://localhost:8080`.
5. Open the `day17_hello` workflow.
6. Trigger a run and monitor its progress.
7. Inspect task logs to verify the output.

## Validation

The updated workflow completed successfully.

- `start`: Success
- `hello`: Success
- `finish`: Success

All three tasks executed successfully in approximately 3 seconds or less.

## Key Takeaways

- Apache Airflow orchestrates data pipelines.
- A DAG represents a workflow and its task dependencies.
- Tasks represent individual units of work.
- Dependencies determine the execution order.
- Airflow provides a web interface for triggering workflows and monitoring execution.
- Task logs help verify outputs and troubleshoot failures.

## Next Steps

- Learn scheduled workflow execution.
- Practise retries and failure handling.
- Explore pipeline monitoring and logging.
- Integrate Airflow with a data extraction, transformation, and loading (ETL) pipeline.

