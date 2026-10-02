from config import PIPELINE_NAME
from database import (
    get_connection,
    create_tables,
    get_watermark,
    load_orders,
    update_watermark,
)
from extract import read_new_orders
from validate import validate_orders
from logger import logger


def run_pipeline():
    logger.info("Pipeline started")

    conn = None

    try:
        conn = get_connection()

        create_tables(conn)

        last_processed_id = get_watermark(
            conn,
            PIPELINE_NAME
        )

        logger.info(
            f"Last processed ID: {last_processed_id}"
        )

        orders = read_new_orders(
            last_processed_id
        )

        logger.info(
            f"Orders extracted: {len(orders)}"
        )

        if not orders:
            logger.info("No new orders found")
            return

        valid_orders = validate_orders(orders)

        logger.info(
            f"Orders validated: {len(valid_orders)}"
        )

        load_orders(
            conn,
            valid_orders
        )

        new_watermark = max(
            order["order_id"]
            for order in valid_orders
        )

        update_watermark(
            conn,
            PIPELINE_NAME,
            new_watermark
        )

        conn.commit()

        logger.info(
            f"Watermark updated to: {new_watermark}"
        )

        logger.info("Pipeline completed successfully")

    except Exception:
        if conn is not None:
            conn.rollback()

        logger.exception("Pipeline failed")

        raise

    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    run_pipeline()