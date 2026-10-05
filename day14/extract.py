import csv

from metadata import PIPELINE_METADATA


def read_records():
    records = []

    source_file = PIPELINE_METADATA["source_file"]

    with open(source_file, "r", newline="") as file:
        reader = csv.DictReader(file)

        source_columns = reader.fieldnames

        for row in reader:
            record = {}

            for column, data_type in PIPELINE_METADATA["schema"].items():
                value = row[column]

                if data_type == "int":
                    value = int(value)

                elif data_type == "string":
                    value = value.strip()

                record[column] = value

            records.append(record)

    return records, source_columns