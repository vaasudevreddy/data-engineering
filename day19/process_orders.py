
import csv
import sys
from pathlib import Path

data_dir = Path(__file__).parent / "data"

input_name = sys.argv[1] if len(sys.argv) > 1 else "orders.csv"
input_file = data_dir / input_name
output_file = data_dir / "processed_orders.csv"

with input_file.open("r", newline="") as file:
    reader = csv.DictReader(file)
    orders = list(reader)

if not orders:
    raise ValueError(f"No orders found in {input_file.name}")

for order in orders:
    try:
        quantity = int(order["quantity"])
        price = float(order["price"])
    except (ValueError, TypeError) as error:
        raise ValueError(
            f"Invalid quantity or price for order "
            f"{order.get('order_id', 'unknown')}"
        ) from error

    if quantity <= 0:
        raise ValueError(
            f"Quantity must be positive for order "
            f"{order.get('order_id', 'unknown')}"
        )

    if price < 0:
        raise ValueError(
            f"Price cannot be negative for order "
            f"{order.get('order_id', 'unknown')}"
        )

    order["total"] = round(quantity * price, 2)

with output_file.open("w", newline="") as file:
    fieldnames = list(orders[0].keys())
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(orders)

print(f"Processed {len(orders)} orders from {input_file.name}.")
print(f"Saved results to {output_file}")
