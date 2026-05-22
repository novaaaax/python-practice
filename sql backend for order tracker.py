import mysql.connector
import os
from dotenv import load_dotenv
import simpy 
from simpy import Environment, Resource
import barcode
from barcode.writer import ImageWriter
import pandas as ps
import openpyxl


# Load environment variables from .env file
load_dotenv()

# connect to MySQL Server
db_connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = db_connection.cursor()
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
        batch_id VARCHAR(255),
        operator_id INT,
        area_of_production VARCHAR(255),
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')



def smart_scheduling():
    env = Environment()
    prep_operators = Resource(env, capacity=int(input("How many operators are in the prep area? ")))
    term_operators = Resource(env, capacity=int(input("How many operators are in the term area? ")))
    cleave_operators = Resource(env, capacity=int(input("How many operators are in the cleave area? ")))
    polish_operators = Resource(env, capacity=int(input("How many operators are in the polish area? ")))
    scope_operators = Resource(env, capacity=int(input("How many operators are in the scope area? ")))
    test_operators = Resource(env, capacity=int(input("How many operators are in the test area? ")))
    packing_operators = Resource(env, capacity=int(input("How many operators are in the packing area? ")))





def export_to_excel():
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    df = ps.DataFrame(orders, columns=['Order ID', 'Fiber Qty'])
    df.to_excel('completed_orders.xlsx', index=False)
    openpyxl.load_workbook(f'completed_orders.xlsx')



main_page = (int(input("What would you like to do? \n1. Create new order \n2. View current orders \n3. Enter production Tracking Mode \n4. Export to Excel \n5. Exit \n")))
while main_page == 1 or main_page == 2 or main_page == 3 or main_page == 4 or main_page == 5:
    if main_page == 1:
        order_id = int(input("Scan the job number: "))
        fiber_qty = int(input("Enter the fiber quantity: "))
        print(f"Job info: {order_id, fiber_qty}")
        cursor.execute("INSERT INTO orders (order_id, fiber_qty) VALUES (%s, %s)", (order_id, fiber_qty))
        db_connection.commit()
        print(f"{order_id, fiber_qty} inserted successfully.")

    elif main_page == 2:
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        for order in orders:
            print(f"Order ID: {order[0]}, Fiber Quantity: {order[1]}")
        continue_input = int(input("Return to main menu? (1 for yes, 2 for no): "))
        if continue_input == 1:
            main_paint = (int(input("What would you like to do? \n1. Create new order \n2. View current orders \n3. Enter production Tracking Mode \n4. Export to Excel \n5. Exit \n")))
        else:
            print("Exiting the program.")
            break

    elif main_page == 3:
        # i want to make the text be entered automatically when the operator scans the job number and operator id.
        while True:
            area_of_production = int(input("What area of prouction are you currently in? \n1. Prep \n2. Term \n3. Cleave \n4. Polish \n5. Scope \n6. Test \n7. Packing"))
            prep = "Prep"
            term = "Term"
            cleave = "Cleave"
            polish = "Polish"
            scope = "Scope"
            test = "Test"
            packing = "Packing"
            tracking_id = 1
            if area_of_production == 1:
                operator_id = int(input("Scan your operator ID: "))
                batch_id = int(input("Scan the batch ID: "))
                cursor.execute("INSERT INTO production_tracking (tracking_id, batch_id, operator_id, area_of_production) VALUES (%s, %s, %s, %s)", (tracking_id, batch_id, operator_id, prep))
                db_connection.commit()
                print(f"Batch {batch_id} entered successfully")
                operator_id
                batch_id

            elif area_of_production == 2:
                operator_id = int(input("Scan your operator ID: "))
                batch_id = int(input("Scan the batch ID: "))
                cursor.execute("INSERT INTO production_tracking (tracking_id, batch_id, operator_id, area_of_production) VALUES (%s, %s, %s, %s)", (tracking_id, batch_id, operator_id, term))
                db_connection.commit()
                print(f"Batch {batch_id} entered successfully")

            operator_id = int(input("Scan your operator ID: "))
            batch_id = int(input("Scan the batch ID: "))
            cursor.execute("INSERT INTO production_tracking (tracking_id, batch_id, operator_id, area_of_production) VALUES (%s, %s, %s, %s)", (tracking_id, batch_id, operator_id, packing ))
            db_connection.commit()
            print(f"Batch {batch_id} entered successfully")

    elif main_page == 4:
        export_to_excel()
        print("Data exported to completed_orders.xlsx successfully.")
        main_page = (int(input("What would you like to do? \n1. Create new order \n2. View current orders \n3. Enter production Tracking Mode \n5. Exit \n")))



    elif main_page == 5:
        print("Exiting the program.")
        break
        
    else:
        print("Invalid option. Please select a valid option from the menu.")
    main_page = (int(input("What would you like to do? \n1. Create new order \n2. View current orders \n3. Enter production Tracking Mode \n4. Export to Excel \n5. Exit \n")))
    