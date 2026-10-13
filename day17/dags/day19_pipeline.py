import subprocess
import pendulum

from airflow.sdk import dag, task


@dag(
    dag_id="day19_orders_pipeline",
    schedule=None,
    start_date=pendulum.datetime(2026, 10, 13, tz="UTC"),
    catchup=False,
    tags=["day19", "data-pipeline"],
)
def day19_orders_pipeline():

    @task
    def process_orders():
        script_path = "/opt/airflow/day19/process_orders.py"

        subprocess.run(
            ["python", script_path],
            check=True,
        )

    process_orders()


day19_orders_pipeline()
