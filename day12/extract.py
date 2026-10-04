import csv
from datetime import datetime

from config import CSV_FILE


def read_changed_orders(
    last_processed_timestamp,
    last_processed_order_id
):
    orders = []

    with open(CSV_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            updated_at = datetime.strptime(
                row["updated_at"],
                "%Y-%m-%d %H:%M:%S"
            )

            order_id = int(row["order_id"])

            if (
                updated_at > last_processed_timestamp
                or (
                    updated_at == last_processed_timestamp
                    and order_id > last_processed_order_id
                )
            ):
                orders.append({
                    "order_id": order_id,
                    "customer": row["customer"],
                    "amount": int(row["amount"]),
                    "updated_at": updated_at
                })

    return orders