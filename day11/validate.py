def validate_orders(orders):
    valid_orders = []

    for order in orders:
        if order["order_id"] <= 0:
            raise ValueError(
                f"Invalid order ID: {order['order_id']}"
            )

        if not order["customer"].strip():
            raise ValueError(
                f"Customer is empty for order: {order['order_id']}"
            )

        if order["amount"] < 0:
            raise ValueError(
                f"Negative amount for order: {order['order_id']}"
            )

        valid_orders.append(order)

    return valid_orders