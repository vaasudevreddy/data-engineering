CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    country VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    amount INT,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


-- Practice data

INSERT INTO customers (customer_id, customer_name, country)
VALUES
    (1, 'Alice', 'Denmark'),
    (2, 'Bob', 'Sweden'),
    (3, 'Charlie', 'Norway'),
    (4, 'David', 'Denmark');

INSERT INTO orders (order_id, customer_id, amount)
VALUES
    (1001, 1, 50),
    (1002, 2, 80),
    (1003, 1, 120),
    (1004, 3, 30),
    (1005, 4, 200),
    (1006, 2, 150);