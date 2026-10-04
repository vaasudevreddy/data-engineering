from config import PIPELINE_NAME
from database import (
    get_connection,
    create_tables,
    get_watermark,
    load_orders,
    update_watermark,
)
from extract import read_changed_orders
from validate import validate_orders
from logger import logger


def run_pipeline():
    logger.info("Pipeline started")

    conn = None

    try:
        conn = get_connection()

        create_tables(conn)

        last_processed_timestamp, last_processed_order_id = get_watermark(
            conn,
            PIPELINE_NAME
        )

        logger.info(
            f"Last processed timestamp: {last_processed_timestamp}"
        )

        logger.info(
            f"Last processed order ID: {last_processed_order_id}"
        )

        orders = read_changed_orders(
            last_processed_timestamp,
            last_processed_order_id
        )

        logger.info(
            f"Orders extracted: {len(orders)}"
        )

        if not orders:
            logger.info("No new or changed orders found")
            return

        valid_orders = validate_orders(orders)

        logger.info(
            f"Orders validated: {len(valid_orders)}"
        )

        load_orders(
            conn,
            valid_orders
        )

        latest_order = max(
            valid_orders,
            key=lambda order: (
                order["updated_at"],
                order["order_id"]
            )
        )

        update_watermark(
            conn,
            PIPELINE_NAME,
            latest_order["updated_at"],
            latest_order["order_id"]
        )

        conn.commit()

        logger.info(
            f"Watermark updated to: "
            f"{latest_order['updated_at']} | "
            f"Order ID: {latest_order['order_id']}"
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