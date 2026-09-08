def validate_order(order):

    if not order.get("order_id"):
        return False

    try:
        amount = int(order["amount"])
    except (ValueError, TypeError):
        return False

    if amount < 0:
        return False

    return True