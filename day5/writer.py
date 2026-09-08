import json


def write_orders(orders, file_path):

    with open(file_path, "w") as file:
        json.dump(orders, file, indent=4)