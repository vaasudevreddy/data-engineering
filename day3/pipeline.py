import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

file_path = Path("day3/orders.json")


def load_orders(path: Path) -> list:
    with open(path, "r") as file:
        return json.load(file)


def calculate_total(orders: list) -> int:
    total = 0

    for order in orders:
        amount = order["amount"]

        if amount is None:
            logging.warning(
                f"{order['order_id']} has a missing amount"
            )
            continue

        total = total + amount

    return total


logging.info("Pipeline started")

orders = load_orders(file_path)

total_amount = calculate_total(orders)

logging.info(f"Total amount: {total_amount}")

logging.info("Pipeline finished")