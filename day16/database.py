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