#orders_details
import sqlite3
import csv
import os
from datetime import datetime

database_name = "restaurant.db"
save_file_path = r"enter the loaction to save the file"

def fetch_order_data():
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                Orders.token_number,
                Menu.Dish_Name,
                order_items.quantity,
                Orders.total_amount,
                Orders.order_date
            FROM Orders
            JOIN order_items ON Orders.order_id = order_items.order_id
            JOIN Menu ON order_items.item_id = Menu.item_id
            ORDER BY Orders.order_date;
        """)
        orders = cursor.fetchall()
        conn.close()
        return orders
    except sqlite3.Error as e:
        print(f"Error fetching order details: {e}")
        return None

def save_as_csv(orders):
    if not orders:
        print("No orders found to save.")
        return
    
    year_data = {}
    for order in orders:
        token_number, dish_name, quantity, total_amount, order_date = order
        try:
            year = datetime.strptime(order_date, "%Y-%m-%dT%H:%M:%S.%f").year
        except ValueError:
            year = datetime.strptime(order_date, "%Y-%m-%d").year
        
        if year not in year_data:
            year_data[year] = []
        year_data[year].append([token_number, dish_name, quantity, total_amount, order_date])
    
    for year, data in year_data.items():
        filename = os.path.join(save_file_path, f"orders in {year}.csv")
        try:
            with open(filename, mode = "w", newline = '', encoding = 'utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["token_number, dish_name, quantity, total_amount, order_date"])
                #writer.writerow(["Token Number", "Dish Name", "Quantity", "Total Amount", "Order date"])
                writer.writerows(data)
            print(f"saved order details for {year} to {filename}")
        except IOError as e:
            print(f"Error writing to file {filename}: {e}")

if __name__ == "__main__":
    orders = fetch_order_data()
    if orders:
        save_as_csv(orders)
    else:
        print("No orders found to save.")
