import csv
from pathlib import Path

data_dir = Path(__file__).parent / "data"
input_file = data_dir / "orders.csv"
output_file = data_dir / "processed_orders.csv"

with input_file.open("r", newline="") as file:
    reader = csv.DictReader(file)
    orders = list(reader)

for order in orders:
    quantity = int(order["quantity"])
    price = float(order["price"])
    order["total"] = round(quantity * price, 2)

with output_file.open("w", newline="") as file:
    fieldnames = list(orders[0].keys())
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(orders)

print(f"Processed {len(orders)} orders.")
print(f"Saved results to {output_file}")
