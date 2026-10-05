from quality import (
    check_required_fields,
    check_unique,
    check_positive,
    check_range,
    check_referential_integrity,
)


def test_required_field_passes():
    records = [
        {
            "customer_name": "Alice",
            "country": "Denmark"
        }
    ]

    errors = check_required_fields(
        records,
        ["customer_name", "country"]
    )

    assert errors == []


def test_required_field_fails():
    records = [
        {
            "customer_name": "",
            "country": "Denmark"
        }
    ]

    errors = check_required_fields(
        records,
        ["customer_name", "country"]
    )

    assert len(errors) == 1
    assert "customer_name is missing" in errors[0]


def test_unique_passes():
    records = [
        {"customer_id": 1},
        {"customer_id": 2},
        {"customer_id": 3}
    ]

    errors = check_unique(
        records,
        "customer_id"
    )

    assert errors == []


def test_unique_fails():
    records = [
        {"customer_id": 1},
        {"customer_id": 2},
        {"customer_id": 1}
    ]

    errors = check_unique(
        records,
        "customer_id"
    )

    assert len(errors) == 1
    assert "duplicate customer_id: 1" in errors[0]


def test_positive_passes():
    records = [
        {"customer_id": 1},
        {"customer_id": 5}
    ]

    errors = check_positive(
        records,
        "customer_id"
    )

    assert errors == []


def test_positive_fails():
    records = [
        {"customer_id": 1},
        {"customer_id": -5}
    ]

    errors = check_positive(
        records,
        "customer_id"
    )

    assert len(errors) == 1
    assert "customer_id must be positive" in errors[0]


def test_range_passes():
    records = [
        {"age": 25},
        {"age": 50},
        {"age": 100}
    ]

    errors = check_range(
        records,
        "age",
        18,
        100
    )

    assert errors == []


def test_range_fails():
    records = [
        {"age": 25},
        {"age": 150}
    ]

    errors = check_range(
        records,
        "age",
        18,
        100
    )

    assert len(errors) == 1
    assert "age must be between 18 and 100" in errors[0]


def test_referential_integrity_passes():
    records = [
        {"customer_id": 1},
        {"customer_id": 2},
        {"customer_id": 3}
    ]

    valid_customer_ids = {1, 2, 3}

    errors = check_referential_integrity(
        records,
        "customer_id",
        valid_customer_ids
    )

    assert errors == []


def test_referential_integrity_fails():
    records = [
        {"customer_id": 1},
        {"customer_id": 99}
    ]

    valid_customer_ids = {1, 2, 3}

    errors = check_referential_integrity(
        records,
        "customer_id",
        valid_customer_ids
    )

    assert len(errors) == 1
    assert "unknown value: 99" in errors[0]