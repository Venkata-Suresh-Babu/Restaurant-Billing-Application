#menu.py
import customtkinter as ctk

class menu_card(ctk.CTkFrame):
    def __init__(self, master, item_data, add_to_cart_command, **kwargs):
        super().__init__(master, **kwargs)
        self.item_id, item_name, item_price = item_data
        self.item_name = item_name
        self.item_price = item_price
        self.quantity = 0
        self.add_to_cart_command = add_to_cart_command
        self.grid_columnconfigure(1, weight=1)

        self.item_name_label = ctk.CTkLabel(self, text=self.item_name, font=ctk.CTkFont(size=16, weight="bold"), anchor='w')
        self.item_name_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky='ew')
        
        self.price_label = ctk.CTkLabel(self, text=f"₹{self.item_price:.2f}", anchor='w')
        self.price_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='ew')

        self.quantity_frame = ctk.CTkFrame(self)
        self.quantity_frame.grid(row=2, column=0, padx=10, pady=(5, 10), sticky='ew')

        self.quantity_frame.grid_columnconfigure(0, weight=1)
        self.quantity_frame.grid_columnconfigure(2, weight=1)

        self.decrement_button = ctk.CTkButton(self.quantity_frame, text="-", width=30, height=30, command=self.decrement_quantity) # Corrected command
        self.decrement_button.grid(row=0, column=0, padx=5, pady=5)

        self.quantity_display = ctk.CTkLabel(self.quantity_frame, text=str(self.quantity), width=30)
        self.quantity_display.grid(row=0, column=1, padx=5, pady=5)

        self.increment_button = ctk.CTkButton(self.quantity_frame, text="+", width=30, height=30, command=self.increment_quantity) # Corrected command
        self.increment_button.grid(row=0, column=2, padx=5, pady=5) #corrected column to 2

    def increment_quantity(self): # Corrected method name
        self.quantity += 1
        self.quantity_display.configure(text=str(self.quantity))
        self.add_to_cart_command(self)  # Pass the MenuCard instance itself
    
    def decrement_quantity(self): # Corrected method name
        if self.quantity > 0:
            self.quantity -= 1
            self.quantity_display.configure(text=str(self.quantity))
            self.add_to_cart_command(self)  # Pass the MenuCard instance itself (even on decrement, to update cart)
