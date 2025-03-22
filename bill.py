#bill.py
from datetime import datetime
import math

def generate_bill_text(restaurant_info, token_number, cart_items, total_price):
    restaurant_name, restaurant_address = restaurant_info

    bill_header = f"""
        {restaurant_name.upper()}
        {restaurant_address}
=========================================
token number: {token_number}
date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
_________________________________________
items:
"""
    bill_items = ""
    for item in cart_items:
        bill_items += f"{item['name']} x {item['quantity']}     : ₹{item['price']} * {item['quantity']: .2f}\n"

    # Calculate tax and service charge (1.5% each)
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    
    bill_footer = f"""
==================================================
total amount: ₹{math.ceil(total_price): .2f}
==================================================
thank you visit again 🙂
"""
    return bill_header + bill_items + bill_footer

if __name__ == "__main__":
    # Example usage:
    restaurant_details = ("Our Restaurant", "get your energy back")
    sample_cart_items = [
        {'name': 'Burger',  'price': 8.99, 'quantity': 2},
        {'name': 'Fries',   'price': 4.50, 'quantity': 1}
    ]
    total = sum(item['price'] * item['quantity'] for item in sample_cart_items)
    bill_text = generate_bill_text(restaurant_details, 123, sample_cart_items, total)
    print(bill_text)
