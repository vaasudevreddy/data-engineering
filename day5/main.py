from pathlib import Path
import logging

from reader import read_orders
from validator import validate_order
from transformer import transform_orders
from writer import write_orders


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR.parent / "day4" / "orders.csv"
OUTPUT_FILE = BASE_DIR / "processed_orders.json"


def main():

    logging.info("Pipeline started")

    try:
        orders = read_orders(INPUT_FILE)
        logging.info("Read %d orders", len(orders))

        valid_orders = []
        invalid_orders = []

        for order in orders:

            if validate_order(order):
                valid_orders.append(order)
                logging.info("Valid order: %s", order["order_id"])

            else:
                invalid_orders.append(order)
                logging.warning(
                    "Invalid order: %s",
                    order.get("order_id", "UNKNOWN")
                )

        valid_orders = transform_orders(valid_orders)

        write_orders(valid_orders, OUTPUT_FILE)

        logging.info(
            "Processed %d valid orders",
            len(valid_orders)
        )

        logging.info(
            "Rejected %d invalid orders",
            len(invalid_orders)
        )

        logging.info(
            "Output written to %s",
            OUTPUT_FILE
        )

    except Exception:
        logging.exception("Pipeline failed")
        raise

    logging.info("Pipeline finished")


if __name__ == "__main__":
    main()