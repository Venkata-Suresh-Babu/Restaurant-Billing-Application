# cart file
class shoppingCart():
    def __init__(self):
        self.items = {}  # dictionary to hold items in the cart: {item_id: {'name': name, 'price': price, 'quantity': quantity}}

    def add_item(self, menu_card):
        item_id = menu_card.item_id
        item_name = menu_card.item_name
        item_price = menu_card.item_price
        quantity = menu_card.quantity

        if quantity > 0:
            self.items[item_id] = {'item_id': item_id, 'name': item_name, 'price': item_price, 'quantity': quantity}
        elif item_id in self.items and quantity == 0:  # remove if quantity becomes 0
            del self.items[item_id]

    def get_items(self):
        return list(self.items.values())  # return as a list of item dictionaries

    def get_total_price(self):
        total = 0.0
        for item in self.items.values():
            total += item['price'] * item['quantity']

        return round(total, 2)  # rounding to 2 decimal places

    def clear_cart(self):
        self.items = {}
