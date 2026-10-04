from database import (
    get_connection,
    create_table,
    load_records,
)
from extract import read_records
from validate import (
    validate_records,
    validate_schema,
)
from metadata import PIPELINE_METADATA


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

        print(f"Records extracted: {len(records)}")

        valid_records = validate_records(records)

        print(
            f"Records validated: {len(valid_records)}"
        )

        load_records(conn, valid_records)

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