import csv

import psycopg

from config import DB_CONFIG
from logger import get_logger


logger = get_logger()


def get_connection():
    logger.info("Connecting to PostgreSQL")
    return psycopg.connect(**DB_CONFIG)


def create_table(conn):
    logger.info("Creating target table if it does not exist")

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS day16_orders (
                order_id INT PRIMARY KEY,
                customer VARCHAR(255) NOT NULL,
                amount INT NOT NULL
            )
        """)

    conn.commit()
    logger.info("Target table is ready")


def read_orders():
    logger.info("Reading source_orders.csv")

    orders = []

    with open("source_orders.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            orders.append({
                "order_id": int(row["order_id"]),
                "customer": row["customer"].strip(),
                "amount": int(row["amount"])
            })

    logger.info("Orders extracted: %d", len(orders))

    return orders


def load_orders(conn, orders):
    logger.info("Loading %d orders into PostgreSQL", len(orders))

    with conn.cursor() as cur:
        for order in orders:
            cur.execute("""
                INSERT INTO day16_orders (
                    order_id,
                    customer,
                    amount
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (order_id)
                DO UPDATE SET
                    customer = EXCLUDED.customer,
                    amount = EXCLUDED.amount
            """, (
                order["order_id"],
                order["customer"],
                order["amount"]
            ))

    conn.commit()
    logger.info("Orders loaded successfully")


def run_pipeline():
    logger.info("Pipeline started")

    conn = None

    try:
        orders = read_orders()

        conn = get_connection()

        create_table(conn)

        load_orders(conn, orders)

        logger.info("Pipeline completed successfully")

    except Exception:
        if conn is not None:
            conn.rollback()

        logger.exception("Pipeline failed")
        raise

    finally:
        if conn is not None:
            conn.close()
            logger.info("Database connection closed")


if __name__ == "__main__":
    run_pipeline()