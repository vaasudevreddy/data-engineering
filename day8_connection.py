import psycopg

connection = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="employee_management",
    user="postgres",
    password="REMOVED_PASSWORD"
)

cursor = connection.cursor()

# Create output table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS employee_salary_updates (
        employee_id INT PRIMARY KEY,
        name VARCHAR(100),
        department VARCHAR(100),
        original_salary NUMERIC,
        new_salary NUMERIC
    );
""")

# Read employees
cursor.execute("""
    SELECT id, name, department, salary
    FROM employees
    WHERE salary > %s;
""", (50000,))

rows = cursor.fetchall()

# Transform and write the data
for row in rows:
    employee_id, name, department, salary = row

    new_salary = salary * 1.10

    cursor.execute("""
        INSERT INTO employee_salary_updates
            (employee_id, name, department, original_salary, new_salary)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (employee_id)
        DO UPDATE SET
            name = EXCLUDED.name,
            department = EXCLUDED.department,
            original_salary = EXCLUDED.original_salary,
            new_salary = EXCLUDED.new_salary;
    """, (
        employee_id,
        name,
        department,
        salary,
        new_salary
    ))

connection.commit()

print("Salary updates written successfully!")

cursor.close()
connection.close()
