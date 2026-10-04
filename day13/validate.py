from schema import EXPECTED_SCHEMA


def validate_schema(source_columns):
    expected_columns = set(EXPECTED_SCHEMA.keys())
    actual_columns = set(source_columns)

    missing_columns = expected_columns - actual_columns
    unexpected_columns = actual_columns - expected_columns

    if missing_columns:
        raise ValueError(
            f"Missing columns: {sorted(missing_columns)}"
        )

    if unexpected_columns:
        raise ValueError(
            f"Unexpected columns: {sorted(unexpected_columns)}"
        )


def validate_records(records):
    primary_key = next(
        column
        for column in EXPECTED_SCHEMA
        if column.endswith("_id")
    )

    for record in records:
        if record[primary_key] <= 0:
            raise ValueError(
                f"Invalid primary key: {record[primary_key]}"
            )

        for column, data_type in EXPECTED_SCHEMA.items():
            if data_type == "string" and not record[column]:
                raise ValueError(
                    f"{column} is empty for "
                    f"{primary_key}: {record[primary_key]}"
                )

    return records