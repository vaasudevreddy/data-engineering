import csv
import psycopg

DB_CONFIG = {
    "host": "localhost",
    "dbname": "employee_management",
    "user": "postgres",
    "password": "REMOVED_PASSWORD",
    "port": 5432
}

CSV_FILE = "source_orders.csv"


def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS incremental_orders (
                order_id INT PRIMARY KEY,
                customer VARCHAR(100),
                amount INT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_watermark (
                pipeline_name VARCHAR(100) PRIMARY KEY,
                last_processed_id INT
            )
        """)

        cur.execute("""
            INSERT INTO pipeline_watermark
                (pipeline_name, last_processed_id)
            VALUES
                ('orders_pipeline', 0)
            ON CONFLICT (pipeline_name) DO NOTHING
        """)

    conn.commit()


def get_watermark(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT last_processed_id
            FROM pipeline_watermark
            WHERE pipeline_name = 'orders_pipeline'
        """)

        return cur.fetchone()[0]


def read_new_orders(last_processed_id):
    new_orders = []

    with open(CSV_FILE, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            order_id = int(row["order_id"])

            if order_id > last_processed_id:
                new_orders.append({
                    "order_id": order_id,
                    "customer": row["customer"],
                    "amount": int(row["amount"])
                })

    return new_orders


def load_orders(conn, orders):
    if not orders:
        return

    with conn.cursor() as cur:
        for order in orders:
            cur.execute("""
                INSERT INTO incremental_orders
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


def update_watermark(conn, last_processed_id):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE pipeline_watermark
            SET last_processed_id = %s
            WHERE pipeline_name = 'orders_pipeline'
        """, (last_processed_id,))


def main():
    try:
        with psycopg.connect(**DB_CONFIG) as conn:

            create_tables(conn)

            last_processed_id = get_watermark(conn)

            print(f"Last processed ID: {last_processed_id}")

            orders = read_new_orders(last_processed_id)

            print(f"New orders found: {len(orders)}")

            if orders:
                load_orders(conn, orders)

                new_watermark = max(
                    order["order_id"]
                    for order in orders
                )

                update_watermark(conn, new_watermark)

                conn.commit()

                print(f"Watermark updated to: {new_watermark}")

            else:
                print("No new orders found.")

    except Exception as e:
        print(f"Pipeline failed: {e}")


if __name__ == "__main__":
    main()