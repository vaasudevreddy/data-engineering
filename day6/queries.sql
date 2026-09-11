-- Select all orders
SELECT *
FROM orders;


-- Orders greater than 100
SELECT *
FROM orders
WHERE amount > 100;


-- Highest amount first
SELECT *
FROM orders
ORDER BY amount DESC;


-- Total amount
SELECT SUM(amount) AS total_amount
FROM orders;


-- Average amount
SELECT AVG(amount) AS average_amount
FROM orders;


-- Number of orders
SELECT COUNT(*) AS order_count
FROM orders;


-- Total amount by customer
SELECT
    customer_id,
    SUM(amount) AS total_amount
FROM orders
GROUP BY customer_id;


-- Total amount by country
SELECT
    customers.country,
    SUM(orders.amount) AS total_amount
FROM orders
JOIN customers
    ON orders.customer_id = customers.customer_id
GROUP BY customers.country;


-- Customers with total orders greater than 200
SELECT
    customer_id,
    SUM(amount) AS total_amount
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 200;


-- Customer name and total amount
SELECT
    customers.customer_name,
    SUM(orders.amount) AS total_amount
FROM orders
JOIN customers
    ON orders.customer_id = customers.customer_id
GROUP BY customers.customer_name;