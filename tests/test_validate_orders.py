
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



def test_process_orders_rejects_empty_input(tmp_path):
    import subprocess
    import sys
    from pathlib import Path

    project_dir = Path(__file__).resolve().parents[1]
    data_dir = project_dir / "day19" / "data"
    script = project_dir / "day19" / "process_orders.py"

    empty_file = data_dir / "orders_empty.csv"
    output_file = data_dir / "processed_orders.csv"
    original_output = output_file.read_bytes() if output_file.exists() else None

    empty_file.write_text("", encoding="utf-8")

    try:
        result = subprocess.run(
            [sys.executable, str(script), "orders_empty.csv"],
            capture_output=True,
            text=True,
        )

        assert result.returncode != 0
        assert "No orders found" in result.stderr

        if original_output is not None:
            assert output_file.read_bytes() == original_output
    finally:
        empty_file.unlink(missing_ok=True)





def test_existing_output_is_preserved_if_temp_write_fails(tmp_path):
    import subprocess
    import sys
    from pathlib import Path

    project_dir = Path(__file__).resolve().parents[1]
    data_dir = project_dir / "day19" / "data"
    script = project_dir / "day19" / "process_orders.py"

    output_file = data_dir / "processed_orders.csv"
    temp_file = output_file.with_suffix(".tmp")
    original_output = output_file.read_bytes() if output_file.exists() else None

    temp_file.mkdir(exist_ok=True)

    try:
        result = subprocess.run(
            [sys.executable, str(script), "orders.csv"],
            capture_output=True,
            text=True,
        )

        assert result.returncode != 0
        assert output_file.read_bytes() == original_output
        assert temp_file.is_dir()
    finally:
        temp_file.rmdir()
        if original_output is not None:
            output_file.write_bytes(original_output)




def test_calculate_total():
    import sys
    from pathlib import Path

    project_dir = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project_dir / "day19"))

    from process_orders import calculate_total

    assert calculate_total(3, 12.50) == 37.50
    assert calculate_total(2, 10.00) == 20.00
    assert calculate_total(1, 0.00) == 0.00

