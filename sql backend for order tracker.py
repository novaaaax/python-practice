import mysql.connector
import os
from dotenv import load_dotenv
import simpy 
from simpy import Environment, Resource
import barcode
from barcode.writer import ImageWriter
import pandas as pd
import openpyxl
import tkinter as tk
from tkinter import filedialog


load_dotenv()

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
    root = tk.Tk()
    root.withdraw()
    env = Environment()
    prep_operators = Resource(env, capacity=int(input("How many operators are in the prep area? ")))
    term_operators = Resource(env, capacity=int(input("How many operators are in the term area? ")))
    cleave_operators = Resource(env, capacity=int(input("How many operators are in the cleave area? ")))
    polish_operators = Resource(env, capacity=int(input("How many operators are in the polish area? ")))
    scope_operators = Resource(env, capacity=int(input("How many operators are in the scope area? ")))
    test_operators = Resource(env, capacity=int(input("How many operators are in the test area? ")))
    packing_operators = Resource(env, capacity=int(input("How many operators are in the packing area? ")))
    
    output_goal = filedialog.askopenfilename(title="Insert Excel file with orders that need to be completed today", 
                                             filestypes=[("Excel files", "*.xlsx *.xls")])
    
    if output_goal:
        df = pd.read_excel(output_goal)
        print(df)
    else:
        print("No file selected. Exiting the program.")
        return
    


def export_to_excel():
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    df = pd.DataFrame(orders, columns=['Order ID', 'Fiber Qty'])
    df.to_excel('completed_orders.xlsx', index=False)
    openpyxl.load_workbook(f'completed_orders.xlsx')



current_area_of_production = None
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
            main_page = (int(input("What would you like to do? \n1. Create new order \n2. View current orders \n3. Enter production Tracking Mode \n4. Export to Excel \n5. Exit \n")))
        else:
            print("Exiting the program.")
            break

    elif main_page == 3:
        # i want to make the text be entered automatically when the operator scans the job number and operator id.
        track_or_enter = int(input("Would you like to track an order or enter production tracking mode? \n1. Track an order \n2. Enter production tracking mode \n"))
        if track_or_enter == 1:
            batch_id = int(input("Enter job number: "))
            cursor.execute("SELECT * FROM production_tracking WHERE batch_id = %s", (batch_id,))
            order = cursor.fetchall()
            for entry in order:
                print(f"Tracking ID: {entry[0]}, Batch ID: {entry[1]}, Operator ID: {entry[2]}, Area of Production: {entry[3]}, Timestamp: {entry[4]}")
            if entry[3] == "Packing":
                print("Order is completed.")
            elif entry[3] == "Test":
                print("Order is in the test area.")
            elif entry[3] == "Scope":
                print("Order is in the scope area.")
            elif entry[3] == "Polish":
                print("Order is in the polish area.")
            elif entry[3] == "Cleave":
                print("Order is in the cleave area.")
            elif entry[3] == "Term":
                print("Order is in the term area.")
            elif entry[3] == "Prep":
                print("Order is in the prep area.")
            else:
                print("Has not been scanned by production yet.")

        elif track_or_enter == 2:
            while True:
                area_of_production = int(input("What area of prouction are you currently in? \n1. Prep \n2. Term \n3. Cleave \n4. Polish \n5. Scope \n6. Test \n7. Packing"))
                prep = "Prep"
                term = "Term"
                cleave = "Cleave"
                polish = "Polish"
                scope = "Scope"
                test = "Test"
                packing = "Packing"
                tracking_id = 0
                if area_of_production == 1:
                    operator_id = int(input("Scan your operator ID: "))
                    batch_id = int(input("Scan the batch ID: "))
                    tracking_id += 1
                    print(f"Tracking ID: {tracking_id}")
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
        main_page = (int(input("What would you like to do? \n1. Create new order \n2. View current orders \n3. Enter production Tracking Mode \n4. Export to Excel \n5. Exit \n")))


    elif main_page == 5:
        print("Exiting the program.")
        break
        
    else:
        print("Invalid option. Please select a valid option from the menu.")
    main_page = (int(input("What would you like to do? \n1. Create new order \n2. View current orders \n3. Enter production Tracking Mode \n4. Export to Excel \n5. Exit \n")))
    