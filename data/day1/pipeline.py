import csv

missing_amounts = 0

with open("orders.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if row["amount"] == "":
            print("Warning:", row["order_id"], "has a missing amount")
            missing_amounts = missing_amounts + 1

print("Number of orders with missing amount:", missing_amounts)