
import pendulum

from airflow.sdk import dag, task


@dag(
    dag_id="day17_hello",
    schedule=None,
    start_date=pendulum.datetime(2026, 10, 7, tz="UTC"),
    catchup=False,
    tags=["day17", "learning"],
)
def day17_hello():

    @task
    def start():
        print("Starting Day 17 Airflow pipeline")

    @task
    def hello():
        print("Hello from Apache Airflow!")

    @task
    def finish():
        print("Day 17 pipeline completed successfully!")

    start() >> hello() >> finish()


day17_hello()
