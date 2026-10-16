
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

