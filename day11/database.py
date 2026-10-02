import psycopg

from config import DB_CONFIG


def get_connection():
    return psycopg.connect(**DB_CONFIG)


def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS day11_orders (
                order_id INT PRIMARY KEY,
                customer VARCHAR(100),
                amount INT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS day11_watermark (
                pipeline_name VARCHAR(100) PRIMARY KEY,
                last_processed_id INT
            )
        """)

        cur.execute("""
            INSERT INTO day11_watermark
                (pipeline_name, last_processed_id)
            VALUES
                ('day11_orders_pipeline', 0)
            ON CONFLICT (pipeline_name) DO NOTHING
        """)

    conn.commit()


def get_watermark(conn, pipeline_name):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT last_processed_id
            FROM day11_watermark
            WHERE pipeline_name = %s
        """, (pipeline_name,))

        row = cur.fetchone()

        if row is None:
            raise RuntimeError(
                f"Watermark not found for pipeline: {pipeline_name}"
            )

        return row[0]


def load_orders(conn, orders):
    if not orders:
        return

    with conn.cursor() as cur:
        for order in orders:
            cur.execute("""
                INSERT INTO day11_orders
                    (order_id, customer, amount)
                VALUES
                    (%s, %s, %s)
                ON CONFLICT (order_id)
                DO UPDATE SET
                    customer = EXCLUDED.customer,
                    amount = EXCLUDED.amount
            """, (
                order["order_id"],
                order["customer"],
                order["amount"]
            ))


def update_watermark(conn, pipeline_name, last_processed_id):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE day11_watermark
            SET last_processed_id = %s
            WHERE pipeline_name = %s
        """, (
            last_processed_id,
            pipeline_name
        ))