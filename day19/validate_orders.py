import csv
import sys
from pathlib import Path

data_dir = Path(__file__).parent / "data"
input_file = data_dir / (sys.argv[1] if len(sys.argv) > 1 else "orders.csv")

required_fields = ["order_id", "customer", "product", "quantity", "price"]

with input_file.open("r", newline="") as file:
    reader = csv.DictReader(file)
    orders = list(reader)

errors = []
seen_order_ids = set()

for row_number, order in enumerate(orders, start=2):
    if any(
        not order.get(field) or not order[field].strip()
        for field in required_fields
    ):
        errors.append(f"Row {row_number}: Missing required value")
        continue

    order_id = order["order_id"].strip()

    if order_id in seen_order_ids:
        errors.append(f"Row {row_number}: Duplicate order ID {order_id}")

    seen_order_ids.add(order_id)

    try:
        quantity = int(order["quantity"])
        price = float(order["price"])

        if quantity <= 0:
            errors.append(f"Row {row_number}: Quantity must be positive")

        if price < 0:
            errors.append(f"Row {row_number}: Price cannot be negative")

    except ValueError:
        errors.append(f"Row {row_number}: Quantity or price is not numeric")

if errors:
    print(f"Validation failed with {len(errors)} error(s):")
    for error in errors:
        print(error)
    sys.exit(1)

print(f"Validation passed: {len(orders)} orders checked.")