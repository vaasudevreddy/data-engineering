import psycopg
from config import DB_CONFIG


def get_connection():
    return psycopg.connect(**DB_CONFIG)


def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS day15_orders (
                order_id INT PRIMARY KEY,
                customer VARCHAR(255) NOT NULL,
                amount INT NOT NULL,
                order_date DATE NOT NULL
            )
        """)

        cur.execute("""
            ALTER TABLE day15_orders
            ADD COLUMN IF NOT EXISTS order_date DATE
        """)

    conn.commit()


def load_order(conn, order):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO day15_orders (
                order_id,
                customer,
                amount,
                order_date
            )
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (order_id)
            DO UPDATE SET
                customer = EXCLUDED.customer,
                amount = EXCLUDED.amount,
                order_date = EXCLUDED.order_date
        """, (
            order["order_id"],
            order["customer"],
            order["amount"],
            order["order_date"]
        ))