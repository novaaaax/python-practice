import mysql.connector
import os
from dotenv import load_dotenv
import simpy 
from simpy import Environment, Resource
import barcode
from barcode.writer import ImageWriter

# Load environment variables from .env file
load_dotenv()

# connect to MySQL Server
db_connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = db_connection.cursor()
# creating the schema
db_name = os.getenv("DB_NAME")
cursor.execute(f"CREATE DATABASE if NOT EXISTS {db_name}")
cursor.execute(f"USE {db_name}")

print("Schema 'order_tracker_db' created successfully.")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        fiber_qty INT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS production_tracking (
        tracking_id INT AUTO_INCREMENT PRIMARY KEY,
        batch_id INT,
        operator_id INT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')


main_page = (int(input("What would you like to do? \n1. Create new order \n2. View current orders \n3. Enter production Tracking Mode \n4. Exit \n")))
while main_page == 1 or main_page == 2 or main_page == 3 or main_page == 4:
    if main_page == 1:
        job_info = []
        job_number = int(input("Scan the job number: "))
        fiber_qty = int(input("Enter the fiber quantity: "))
        job_info.append((job_number, fiber_qty))
        cursor.execute("INSERT INTO orders (order_id, fiber_qty) VALUES (%s, %s)", job_info)
        db_connection.commit()
        print(f"{job_info} inserted successfully.")

    elif main_page == 2:
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        for order in orders:
            print(f"Order ID: {order[0]}, Fiber Quantity: {order[1]}")
        continue_input = int(input("Return to main menu? (1 for yes, 2 for no): "))
        if continue_input == 1:
            main_paint = (int(input("What would you like to do? \n1. Create new order \n2. View current orders \n3. Enter production Tracking Mode \n4. Exit \n")))
        else:
            print("Exiting the program.")
            break

    elif main_page == 3:
        # i want to make the text be entered automatically when the operator scans the job number and operator id.
        while True:
            operator_id = int(input("Scan your operator ID: "))
            batch_id = int(input("Scan the batch ID: "))
            cursor.execute("INSERT INTO production_tracking (batch_id, operator_id) VALUES (%s, %s)", (batch_id, operator_id))
            db_connection.commit()
            print(f"Batch {batch_id} entered successfully")


    elif main_page == 4:
        print("Exiting the program.")
        break
        
    else:
        print("Invalid option. Please select a valid option from the menu.")
    main_page = (int(input("What would you like to do? \n1. Create new order \n2. View current orders \n3. Enter production Tracking Mode \n4. Exit \n")))