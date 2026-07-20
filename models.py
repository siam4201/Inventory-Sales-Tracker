from datetime import datetime

class BaseItem:
    def __init__(self, item_id, name, category, price):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.price = price                                      

    def __str__(self):
        return f"[{self.item_id}] {self.name} - {self.category}"

class Product(BaseItem):
    def __init__(self, product_id, name, category, price, quantity, low_stock_threshold):
        super().__init__(product_id, name, category, price)
        self.quantity = int(quantity)
        self.low_stock_threshold = int(low_stock_threshold)

    def __str__(self):
        return (f"Product: [{self.item_id}] {self.name} - {self.category} @ ${self.price:.2f} | "
                f"Qty: {self.quantity} | "
                f"Threshold: {self.low_stock_threshold}")

    def to_dict(self):
        return {
            "product_id": self.item_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
            "low_stock_threshold": self.low_stock_threshold
        }
