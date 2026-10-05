from database import (
    get_connection,
    create_table,
    load_records,
)
from extract import read_records
from metadata import PIPELINE_METADATA
from quality import run_quality_checks
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


def run_pipeline():
    conn = None

    try:
        conn = get_connection()

        create_table(conn)

        records, source_columns = read_records()

        print(
            f"Pipeline: "
            f"{PIPELINE_METADATA['pipeline_name']}"
        )

        print(
            f"Source: "
            f"{PIPELINE_METADATA['source_file']}"
        )

        print(
            f"Target: "
            f"{PIPELINE_METADATA['target_table']}"
        )

        validate_schema(source_columns)

        print("Schema validated successfully")

        print(
            f"Records extracted: {len(records)}"
        )

        quality_errors = run_quality_checks(records)

        if quality_errors:
            print("Data quality checks failed:")

            for error in quality_errors:
                print(f"- {error}")

            raise ValueError(
                "Pipeline stopped because data quality "
                "checks failed"
            )

        print("Data quality checks passed")

        load_records(conn, records)

        conn.commit()

        print("Pipeline completed successfully")

    except Exception:
        if conn is not None:
            conn.rollback()

        print("Pipeline failed")

        raise

    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    run_pipeline()