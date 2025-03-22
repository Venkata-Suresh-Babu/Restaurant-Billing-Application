#main.py
import customtkinter as ctk
import restaurant_database as database
from menu import menu_card
from cart import shoppingCart
from bill import generate_bill_text
from datetime import datetime
import random # For generating token numbers

class RestaurantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Restaurant Bill Generator")
        self.geometry("800x600")

        self.restaurant_info = database.get_restaurant_info() # Fetch restaurant details
        self.menu_items_data = database.get_menu_items()
        self.shopping_cart = shoppingCart()

        # --- UI Setup ---
        self.grid_columnconfigure(0, weight = 1) # Main window column expand
        self.grid_rowconfigure(1, weight = 1)    # Menu Frame row expand

        # Restaurant Info Frame (Top)
        self.info_frame = ctk.CTkFrame(self, corner_radius= 1)
        self.info_frame.grid(row=0, column=0, sticky="ew")
        self.restaurant_name_label = ctk.CTkLabel(self.info_frame, text=self.restaurant_info[0].upper() if self.restaurant_info else "RESTAURANT NAME", font=ctk.CTkFont(size=20, weight="bold"))
        self.restaurant_name_label.pack(pady=5)
        self.restaurant_address_label = ctk.CTkLabel(self.info_frame, text=self.restaurant_info[1] if self.restaurant_info else "Restaurant Address")
        self.restaurant_address_label.pack(pady=5)

        # Menu Frame (Scrollable)
        self.menu_scrollable_frame = ctk.CTkScrollableFrame(self)
        self.menu_scrollable_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.menu_cards = []
        self.display_menu()

        #Cart frame (Right side)
        self.cart_frame = ctk.CTkFrame(self, width = 250, corner_radius = 10)
        self.cart_frame.grid(row=0, column=1, rowspan=2, padx=20, pady=10, sticky="nesw")
        self.cart_frame.grid_rowconfigure(1, weight = 1) # Cart items frame expand
        ctk.CTkLabel(self.cart_frame, text="Your Cart", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.cart_items_frame = ctk.CTkScrollableFrame(self.cart_frame)
        self.cart_items_frame.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = "nsew")
        self.cart_total_label = ctk.CTkLabel(self.cart_frame, text="Total: ₹0.00", font=ctk.CTkFont(weight="bold", size=16))
        self.cart_total_label.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.checkout_button = ctk.CTkButton(self.cart_frame, text="Checkout", command=self.checkout_order, state=ctk.DISABLED)
        self.checkout_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.cart_item_display_labels = {} # To store labels for cart items for updating display

    def display_menu(self):
        for item_data in self.menu_items_data:
            menu_card_instance = menu_card(self.menu_scrollable_frame, item_data, self.update_cart_from_menu, corner_radius=5, fg_color="transparent")  # Make cards transparent to see scrollable frame color
            menu_card_instance.pack(pady=10, padx=10, fill="x", expand=True)  # Pack to arrange cards vertically in scrollable frame
            self.menu_cards.append(menu_card_instance)

    def update_cart_from_menu(self, menu_card):
        self.shopping_cart.add_item(menu_card)
        self.update_cart_display()
    
    def update_cart_display(self):
        cart_items = self.shopping_cart.get_items()
        total_amount = self.shopping_cart.get_total_price()

        # Clear previous cart items display
        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()
        self.cart_item_display_labels = {}

        if not cart_items:
            ctk.CTkLabel(self.cart_items_frame, text = "Your cart is empty", font = ctk.CTkFont(size = 14)).pack(pady = 20)
        else:
            self.checkout_button.configure(state = ctk.NORMAL) # Enable checkout button

            for index, item in enumerate(cart_items):
                item_label = ctk.CTkLabel(self.cart_items_frame, text = f"{item['name']} x {item['quantity']} - ₹{item['price'] * item['quantity']:.2f}")
                item_label.pack(anchor='w', padx= 10, pady=(0, 5))
                self.cart_item_display_labels[item['name']] = item_label
        
        self.cart_total_label.configure(text = f"Total: ₹{total_amount:.2f}")

    def checkout_order(self):
        cart_items = self.shopping_cart.get_items()
        total_amount = self.shopping_cart.get_total_price()
        if not cart_items:
            return
        token_number = random.randint(1000, 9999) # Generate a random token number
        order_date = datetime.now().isoformat() # Get current date and time

        #Save order to database
        database.save_order(token_number, order_date, total_amount, cart_items)

        #generate bill text
        #bill_text = generate_bill_text(self.restaurant_info, token_number, order_date, cart_items, total_amount)
        bill_text = generate_bill_text(self.restaurant_info, token_number, cart_items, total_amount)

        bill_window = ctk.CTkToplevel(self)
        bill_window.title("Bill")
        bill_window.geometry("400x600")
        
        bill_text_area = ctk.CTkTextbox(bill_window, wrap = "none") # warp = "none" fo=r horizontal scrolling if needed
        bill_text_area.insert("0.0", bill_text) # Insert bill text at the beginning
        bill_text_area.configure(state = "disabled") # Make it read only
        bill_text_area.pack(padx= 10, pady = 10, fill = "both", expand = True)

        #clear cart after checkout
        self.shopping_cart.clear_cart()
        self.update_cart_display()

        for card in self.menu_cards:
            card.quantity = 0
            card.quantity_display.configure(text = "0")

if __name__ == "__main__":
    database.initialize_database()
    app = RestaurantApp()
    app.mainloop()
