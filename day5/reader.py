import csv


def read_orders(file_path):

    orders = []

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            orders.append(row)

    return orders