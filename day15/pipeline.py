import csv
import sys

from database import get_connection, create_table, load_order
from retry import retry


def read_orders():
    orders = []

    with open("source_orders.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            orders.append({
                "order_id": int(row["order_id"]),
                "customer": row["customer"].strip(),
                "amount": int(row["amount"]),
                "order_date": row["order_date"]
            })

    return orders


def load_orders(orders):
    conn = get_connection()

    try:
        create_table(conn)

        for order in orders:
            load_order(conn, order)

        conn.commit()
        print("Transaction committed successfully")

    except Exception:
        conn.rollback()
        print("Transaction rolled back")
        raise

    finally:
        conn.close()


def backfill(orders, target_date):
    historical_orders = [
        order for order in orders
        if order["order_date"] == target_date
    ]

    print(f"Backfill date: {target_date}")
    print(f"Orders selected for backfill: {len(historical_orders)}")

    if not historical_orders:
        print("No orders found for backfill")
        return

    retry(
        lambda: load_orders(historical_orders),
        max_attempts=3,
        delay_seconds=2
    )

    print("Backfill completed successfully")


def run_pipeline():
    orders = read_orders()

    print(f"Orders extracted: {len(orders)}")

    retry(
        lambda: load_orders(orders),
        max_attempts=3,
        delay_seconds=2
    )

    print("Pipeline completed successfully")


if __name__ == "__main__":
    orders = read_orders()

    if len(sys.argv) == 3 and sys.argv[1] == "backfill":
        backfill(orders, sys.argv[2])
    else:
        run_pipeline()