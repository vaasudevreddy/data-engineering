import csv
import json
import logging
from pathlib import Path


# -----------------------------
# Logging configuration
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# -----------------------------
# File paths
# -----------------------------

BASE_DIR = Path(__file__).parent

INPUT_FILE = BASE_DIR / "orders.csv"
OUTPUT_FILE = BASE_DIR / "processed_orders.json"


# -----------------------------
# Read CSV data
# -----------------------------

def read_orders(file_path):
    orders = []

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:

            # Convert amount to integer when possible
            try:
                row["amount"] = int(row["amount"])
            except ValueError:
                pass

            orders.append(row)

    return orders


# -----------------------------
# Validate order
# -----------------------------

def validate_order(order):

    # Rule 1: order_id must exist
    if not order.get("order_id"):
        return False

    # Rule 2: amount must be an integer
    if not isinstance(order["amount"], int):
        return False

    # Rule 3: amount cannot be negative
    if order["amount"] < 0:
        return False

    return True


# -----------------------------
# Transform valid orders
# -----------------------------

def transform_orders(orders):

    for order in orders:

        order["amount_with_tax"] = round(
            order["amount"] * 1.20,
            2
        )

    return orders


# -----------------------------
# Main pipeline
# -----------------------------

def main():

    logging.info("Pipeline started")

    # Step 1: Read
    orders = read_orders(INPUT_FILE)

    logging.info(
        "Read %d orders from CSV",
        len(orders)
    )

    # Step 2: Validate and separate
    valid_orders = []
    invalid_orders = []

    for order in orders:

        if validate_order(order):

            valid_orders.append(order)

            logging.info(
                "Valid order: %s",
                order["order_id"]
            )

        else:

            invalid_orders.append(order)

            logging.warning(
                "Invalid order: %s",
                order.get("order_id", "UNKNOWN")
            )

    # Step 3: Transform valid orders
    valid_orders = transform_orders(valid_orders)

    # Step 4: Write processed data
    with open(OUTPUT_FILE, "w") as file:

        json.dump(
            valid_orders,
            file,
            indent=4
        )

    logging.info(
        "Processed %d valid orders",
        len(valid_orders)
    )

    logging.info(
        "Rejected %d invalid orders",
        len(invalid_orders)
    )

    logging.info("Pipeline finished")


# -----------------------------
# Run pipeline
# -----------------------------

if __name__ == "__main__":
    main()