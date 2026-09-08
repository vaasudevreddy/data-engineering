def transform_orders(orders):

    for order in orders:
        order["amount"] = int(order["amount"])
        order["amount_with_tax"] = round(order["amount"] * 1.20, 2)

    return orders