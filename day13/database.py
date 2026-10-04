import psycopg

from config import DB_CONFIG
from metadata import PIPELINE_METADATA


def get_connection():
    return psycopg.connect(**DB_CONFIG)


def get_sql_type(data_type):
    type_mapping = {
        "int": "INT",
        "string": "VARCHAR(255)"
    }

    if data_type not in type_mapping:
        raise ValueError(
            f"Unsupported data type: {data_type}"
        )

    return type_mapping[data_type]


def create_table(conn):
    table_name = PIPELINE_METADATA["target_table"]
    primary_key = PIPELINE_METADATA["primary_key"]
    schema = PIPELINE_METADATA["schema"]

    columns = []

    for column, data_type in schema.items():
        sql_type = get_sql_type(data_type)

        if column == primary_key:
            columns.append(
                f"{column} {sql_type} PRIMARY KEY"
            )
        else:
            columns.append(
                f"{column} {sql_type}"
            )

    columns_sql = ", ".join(columns)

    with conn.cursor() as cur:
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {columns_sql}
            )
        """)

        for column, data_type in schema.items():
            if column == primary_key:
                continue

            sql_type = get_sql_type(data_type)

            cur.execute(f"""
                ALTER TABLE {table_name}
                ADD COLUMN IF NOT EXISTS
                {column} {sql_type}
            """)

    conn.commit()


def load_records(conn, records):
    if not records:
        return

    table_name = PIPELINE_METADATA["target_table"]
    primary_key = PIPELINE_METADATA["primary_key"]
    schema = PIPELINE_METADATA["schema"]

    columns = list(schema.keys())

    column_sql = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))

    update_columns = [
        column
        for column in columns
        if column != primary_key
    ]

    update_sql = ", ".join(
        f"{column} = EXCLUDED.{column}"
        for column in update_columns
    )

    query = f"""
        INSERT INTO {table_name}
            ({column_sql})
        VALUES
            ({placeholders})
        ON CONFLICT ({primary_key})
        DO UPDATE SET
            {update_sql}
    """

    with conn.cursor() as cur:
        for record in records:
            values = [
                record[column]
                for column in columns
            ]

            cur.execute(query, values)