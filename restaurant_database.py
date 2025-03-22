#restaurant_database
import sqlite3
database_name = "restaurant.db"

def create_tables():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

# create a table for restaurant info
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS RestaurantInfo(
        name TEXT NOT NULL,
        address TEXT NOT NULL
    )
    """)
# create a table for resturant menu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Menu(
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Dish_Name TEXT NOT NULL,
        price REAL NOT NULL
    )
    """)
# create a table for orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Orders(
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        token_number INTEGER UNIQUE NOT NULL,
        order_date TEXT NOT NULL,
        total_amount REAL NOT NULL
    )
    """)

#create a table for order items
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items(
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL, 
        FOREIGN KEY (order_id) REFERENCES Orders(order_id),
        FOREIGN KEY (item_id) REFERENCES Menu(item_id)
    )
    """)
    
    conn.commit()
    conn.close()

def initialize_database():
    create_tables()
    # Let's add some initial data if the tables are empty
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Check if RestaurantInfo is empty
    cursor.execute("SELECT COUNT(*) FROM RestaurantInfo")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO RestaurantInfo (name, address) VALUES (?, ?)",
                       ("Restaurant", "123 Main Street, City"))
    
    # Check if Menu is empty and add the dishes
    cursor.execute("SELECT COUNT(*) FROM Menu")
    if cursor.fetchone()[0] == 0:
        menu_items = [
            ("Dosa", 50.00),
            ("Idli", 30.00),
            ("Vada", 40.00),
            ("Sambar Rice", 60.00),
            ("Curd Rice", 50.00),
            ("Biryani", 120.00),
            ("Paneer Butter Masala", 150.00),
            ("Chicken Curry", 200.00),
            ("Fish Fry", 250.00),
            ("Prawn Masala", 300.00),
            ("Vegetable Biryani", 130.00),
            ("Egg Curry", 180.00),
        ]
        cursor.executemany("INSERT INTO Menu (Dish_Name, price) VALUES (?, ?)", menu_items)
    conn.commit()
    conn.close()

def get_restaurant_info():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM RestaurantInfo")
    restaurant_info = cursor.fetchone()
    conn.close()
    return restaurant_info

def get_menu_items():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Menu")
    menu_itmes = cursor.fetchall()
    conn.close()
    return menu_itmes

def save_order(token_number, order_date, total_amount, cart_items):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Orders(token_number, order_date, total_amount) VALUES (?, ?, ?)",
                   (token_number, order_date, total_amount))
    order_id = cursor.lastrowid #fetech the ID of the last order

    order_items = []
    for item in cart_items:
        order_items.append((order_id, item['item_id'], item['quantity']))
    cursor.executemany("INSERT INTO order_items(order_id, item_id, quantity) VALUES (?, ?, ?)", order_items)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    print("Database initialized")
