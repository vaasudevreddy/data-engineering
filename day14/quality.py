def check_required_fields(records, fields):
    errors = []

    for index, record in enumerate(records, start=1):
        for field in fields:
            value = record.get(field)

            if value is None or (
                isinstance(value, str) and not value.strip()
            ):
                errors.append(
                    f"Row {index}: {field} is missing"
                )

    return errors


def check_unique(records, field):
    errors = []
    seen = set()

    for index, record in enumerate(records, start=1):
        value = record[field]

        if value in seen:
            errors.append(
                f"Row {index}: duplicate {field}: {value}"
            )

        seen.add(value)

    return errors


def check_positive(records, field):
    errors = []

    for index, record in enumerate(records, start=1):
        if record[field] <= 0:
            errors.append(
                f"Row {index}: {field} must be positive"
            )

    return errors


def check_range(records, field, minimum, maximum):
    errors = []

    for index, record in enumerate(records, start=1):
        value = record[field]

        if value < minimum or value > maximum:
            errors.append(
                f"Row {index}: {field} must be between "
                f"{minimum} and {maximum}"
            )

    return errors


def run_quality_checks(records):
    errors = []

    errors.extend(
        check_required_fields(
            records,
            ["customer_name", "country"]
        )
    )

    errors.extend(
        check_unique(
            records,
            "customer_id"
        )
    )

    errors.extend(
        check_positive(
            records,
            "customer_id"
        )
    )

    errors.extend(
        check_range(
            records,
            "age",
            18,
            100
        )
    )

    return errors


def check_referential_integrity(records, field, valid_values):
    errors = []

    for index, record in enumerate(records, start=1):
        value = record[field]

        if value not in valid_values:
            errors.append(
                f"Row {index}: {field} references "
                f"unknown value: {value}"
            )

    return errors