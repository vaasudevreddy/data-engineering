
import csv
import sys
from pathlib import Path

data_dir = Path(__file__).parent / "data"


def calculate_total(quantity, price):
    """Calculate an order total rounded to two decimal places."""
    return round(quantity * price, 2)


def load_orders(input_file):
    """Load orders from a CSV file."""
    with input_file.open("r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def validate_and_process_orders(orders, input_file):
    """Validate orders and calculate totals."""
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

        order["total"] = calculate_total(quantity, price)

    return orders


def write_orders(orders, output_file):
    """Write orders safely using a temporary file."""
    if not orders:
        raise ValueError("Cannot write an empty list of orders")

    temp_output_file = output_file.with_suffix(".tmp")

    try:
        with temp_output_file.open("w", newline="") as file:
            fieldnames = list(orders[0].keys())
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(orders)

        temp_output_file.replace(output_file)

    except Exception:
        if temp_output_file.is_file():
            temp_output_file.unlink()
        raise


def process_orders(input_name="orders.csv"):
    """Run the order-processing pipeline."""
    input_file = data_dir / input_name
    output_file = data_dir / "processed_orders.csv"

    orders = load_orders(input_file)
    orders = validate_and_process_orders(orders, input_file)
    write_orders(orders, output_file)

    print(f"Processed {len(orders)} orders from {input_file.name}.")
    print(f"Saved results to {output_file}")


if __name__ == "__main__":
    input_name = sys.argv[1] if len(sys.argv) > 1 else "orders.csv"
    process_orders(input_name)
