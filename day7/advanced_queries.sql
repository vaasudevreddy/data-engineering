-- ============================================
-- DAY 7: ADVANCED SQL
-- ============================================


-- 1. Customer totals using a CTE

WITH customer_totals AS (
    SELECT
        customer_id,
        SUM(amount) AS total_amount
    FROM orders
    GROUP BY customer_id
)

SELECT *
FROM customer_totals
WHERE total_amount > 200;


-- 2. Total amount by customer using JOIN

SELECT
    customers.customer_name,
    SUM(orders.amount) AS total_amount
FROM orders
JOIN customers
    ON orders.customer_id = customers.customer_id
GROUP BY customers.customer_name;


-- 3. Customer order numbering

SELECT
    order_id,
    customer_id,
    amount,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY amount DESC
    ) AS row_num
FROM orders;


-- 4. Customer order ranking

SELECT
    order_id,
    customer_id,
    amount,
    RANK() OVER (
        PARTITION BY customer_id
        ORDER BY amount DESC
    ) AS order_rank
FROM orders;


-- 5. Dense ranking

SELECT
    order_id,
    customer_id,
    amount,
    DENSE_RANK() OVER (
        PARTITION BY customer_id
        ORDER BY amount DESC
    ) AS dense_rank
FROM orders;


-- 6. Running total for each customer

SELECT
    order_id,
    customer_id,
    order_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
    ) AS running_total
FROM orders;


-- 7. Previous order amount using LAG

SELECT
    order_id,
    customer_id,
    order_date,
    amount,
    LAG(amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
    ) AS previous_amount
FROM orders;


-- 8. Latest record for each customer

WITH ranked_orders AS (
    SELECT
        order_id,
        customer_id,
        amount,
        order_date,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY order_date DESC
        ) AS row_num
    FROM orders
)

SELECT
    order_id,
    customer_id,
    amount,
    order_date
FROM ranked_orders
WHERE row_num = 1;


-- 9. Deduplicate customers and keep the latest record

WITH ranked_customers AS (
    SELECT
        customer_id,
        customer_name,
        country,
        updated_at,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY updated_at DESC
        ) AS row_num
    FROM customers
)

SELECT
    customer_id,
    customer_name,
    country,
    updated_at
FROM ranked_customers
WHERE row_num = 1;