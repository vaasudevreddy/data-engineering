
import csv
import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

data_dir = Path(__file__).parent / "data"
input_name = sys.argv[1] if len(sys.argv) > 1 else "orders.csv"
input_path = Path(input_name)
input_file = input_path if input_path.is_absolute() else data_dir / input_path

required_fields = [
    "order_id",
    "customer",
    "product",
    "quantity",
    "price",
]

logger.info("Starting order validation")
logger.info("Input file: %s", input_file.name)

try:
    with input_file.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            logger.error("Validation failed: CSV file is empty")
            sys.exit(1)

        headers = [header.strip() for header in reader.fieldnames]

        missing_fields = [
            field for field in required_fields
            if field not in headers
        ]

        if missing_fields:
            logger.error(
                "Validation failed: Missing required columns: %s",
                ", ".join(missing_fields)
            )
            sys.exit(1)

        reader.fieldnames = headers
        orders = list(reader)

except OSError as error:
    logger.error("Could not read input file: %s", error)
    sys.exit(1)

if not orders:
    logger.error("Validation failed: CSV contains no orders")
    sys.exit(1)

errors = []
seen_order_ids = set()

for row_number, order in enumerate(orders, start=2):
    if any(
        not order.get(field) or not order[field].strip()
        for field in required_fields
    ):
        errors.append(
            f"Row {row_number}: Missing required value"
        )
        continue

    order_id = order["order_id"].strip()

    if order_id in seen_order_ids:
        errors.append(
            f"Row {row_number}: Duplicate order ID {order_id}"
        )

    seen_order_ids.add(order_id)

    try:
        quantity = int(order["quantity"])
        price = float(order["price"])

        if quantity <= 0:
            errors.append(
                f"Row {row_number}: Quantity must be positive"
            )

        if price < 0:
            errors.append(
                f"Row {row_number}: Price cannot be negative"
            )

    except ValueError:
        errors.append(
            f"Row {row_number}: Quantity or price is not numeric"
        )

if errors:
    logger.error(
        "Validation failed with %s error(s):",
        len(errors)
    )

    for error in errors:
        logger.error(error)

    sys.exit(1)

logger.info(
    "Validation passed: %s orders checked.",
    len(orders)
)
