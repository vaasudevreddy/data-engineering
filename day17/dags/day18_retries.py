
import pendulum

from airflow.sdk import dag, task


@dag(
    dag_id="day18_retries",
    schedule=None,
    start_date=pendulum.datetime(2026, 10, 12, tz="UTC"),
    catchup=False,
    tags=["day18", "retries"],
)
def day18_retries():

    @task(retries=2, retry_delay=pendulum.duration(seconds=10))
    def unreliable_task():
        import random

        if random.random() < 0.7:
            raise ValueError("Simulated temporary failure")

        print("Task completed successfully!")

    unreliable_task()


day18_retries()

