import psycopg

from config import DB_CONFIG


def get_connection():
    return psycopg.connect(**DB_CONFIG)


def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS day12_orders (
                order_id INT PRIMARY KEY,
                customer VARCHAR(100),
                amount INT,
                updated_at TIMESTAMP NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS day12_watermark (
                pipeline_name VARCHAR(100) PRIMARY KEY,
                last_processed_timestamp TIMESTAMP,
                last_processed_order_id INT
            )
        """)

        cur.execute("""
            INSERT INTO day12_watermark
                (
                    pipeline_name,
                    last_processed_timestamp,
                    last_processed_order_id
                )
            VALUES
                (
                    'day12_orders_pipeline',
                    '1900-01-01 00:00:00',
                    0
                )
            ON CONFLICT (pipeline_name) DO NOTHING
        """)

    conn.commit()


def get_watermark(conn, pipeline_name):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                last_processed_timestamp,
                last_processed_order_id
            FROM day12_watermark
            WHERE pipeline_name = %s
        """, (pipeline_name,))

        row = cur.fetchone()

        if row is None:
            raise RuntimeError(
                f"Watermark not found for pipeline: {pipeline_name}"
            )

        return row[0], row[1]


def load_orders(conn, orders):
    if not orders:
        return

    with conn.cursor() as cur:
        for order in orders:
            cur.execute("""
                INSERT INTO day12_orders
                    (order_id, customer, amount, updated_at)
                VALUES
                    (%s, %s, %s, %s)
                ON CONFLICT (order_id)
                DO UPDATE SET
                    customer = EXCLUDED.customer,
                    amount = EXCLUDED.amount,
                    updated_at = EXCLUDED.updated_at
            """, (
                order["order_id"],
                order["customer"],
                order["amount"],
                order["updated_at"]
            ))


def update_watermark(
    conn,
    pipeline_name,
    last_processed_timestamp,
    last_processed_order_id
):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE day12_watermark
            SET
                last_processed_timestamp = %s,
                last_processed_order_id = %s
            WHERE pipeline_name = %s
        """, (
            last_processed_timestamp,
            last_processed_order_id,
            pipeline_name
        ))