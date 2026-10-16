
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
VALIDATOR = PROJECT_DIR / "day19" / "validate_orders.py"


def test_valid_orders_pass_validation():
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "orders.csv"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Validation passed: 8 orders checked." in result.stderr


def test_empty_orders_file_fails_validation(tmp_path):
    empty_file = tmp_path / "orders_empty.csv"
    empty_file.write_text("", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(empty_file)],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "CSV file is empty" in result.stderr




def test_missing_required_column_fails_validation(tmp_path):
    invalid_file = tmp_path / "orders_missing_column.csv"
    invalid_file.write_text(
        "order_id,customer,product,quantity\n"
        "1001,Alex,Laptop,1\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(invalid_file)],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "Missing required columns: price" in result.stderr




def test_process_orders_calculates_correct_total():
    import csv
    import subprocess
    import sys
    from pathlib import Path

    project_dir = Path(__file__).resolve().parents[1]
    data_dir = project_dir / "day19" / "data"
    input_file = data_dir / "orders.csv"
    output_file = data_dir / "processed_orders.csv"
    script = project_dir / "day19" / "process_orders.py"

    with input_file.open("r", newline="") as file:
        original_orders = list(csv.DictReader(file))

    subprocess.run(
        [sys.executable, str(script), "orders.csv"],
        check=True,
        capture_output=True,
        text=True,
    )

    with output_file.open("r", newline="") as file:
        processed_orders = list(csv.DictReader(file))

    assert len(processed_orders) == len(original_orders)

    for original, processed in zip(original_orders, processed_orders):
        expected_total = round(
            int(original["quantity"]) * float(original["price"]),
            2,
        )
        assert float(processed["total"]) == expected_total




def test_process_orders_rejects_invalid_quantity(tmp_path):
    import subprocess
    import sys
    from pathlib import Path

    project_dir = Path(__file__).resolve().parents[1]
    data_dir = project_dir / "day19" / "data"
    script = project_dir / "day19" / "process_orders.py"

    invalid_file = tmp_path / "orders_invalid.csv"
    invalid_file.write_text(
        "order_id,customer,product,quantity,price\n"
        "9001,Alex,Laptop,abc,500\n",
        encoding="utf-8",
    )

    (data_dir / "orders_invalid.csv").write_text(
        invalid_file.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    try:
        result = subprocess.run(
            [sys.executable, str(script), "orders_invalid.csv"],
            capture_output=True,
            text=True,
        )

        assert result.returncode != 0
        assert "ValueError" in result.stderr
    finally:
        (data_dir / "orders_invalid.csv").unlink(missing_ok=True)

