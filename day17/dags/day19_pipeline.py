
import os
import subprocess
import pendulum

from airflow.sdk import dag, task


@dag(
    dag_id="day19_orders_pipeline",
    schedule=None,
    start_date=pendulum.datetime(2026, 10, 13, tz="UTC"),
    catchup=False,
    tags=["day19", "data-quality", "configuration"],
)
def day19_orders_pipeline():

    selected_file = os.getenv("ORDERS_INPUT_FILE", "orders.csv")

    @task
    def validate_orders(input_file):
        script_path = "/opt/airflow/day19/validate_orders.py"

        subprocess.run(
            ["python", script_path, input_file],
            check=True,
        )

    @task
    def process_orders(input_file):
        script_path = "/opt/airflow/day19/process_orders.py"

        subprocess.run(
            ["python", script_path, input_file],
            check=True,
        )

    validate_orders(selected_file) >> process_orders(selected_file)


day19_orders_pipeline()
