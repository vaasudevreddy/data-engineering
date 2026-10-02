import csv

from config import CSV_FILE


def read_new_orders(last_processed_id):
    orders = []

    with open(CSV_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            order_id = int(row["order_id"])

            if order_id > last_processed_id:
                orders.append({
                    "order_id": order_id,
                    "customer": row["customer"],
                    "amount": int(row["amount"])
                })

    return orders