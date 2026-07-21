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

    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold

    def update_stock(self, amount):
        if self.quantity + amount < 0:
            raise ValueError(f"Insufficient stock for {self.name}. Current: {self.quantity}, Requested: {abs(amount)}")
        self.quantity += amount

class Sale:
    def __init__(self, sale_id, product_id, quantity_sold, sale_price, sale_date=None):
        self.sale_id = sale_id
        self.product_id = product_id
        self.quantity_sold = int(quantity_sold)
        self.sale_price = float(sale_price)
        self.total_amount = self.quantity_sold * self.sale_price
        
        if sale_date is None:
            self.sale_date = str(datetime.now())
        else:
            self.sale_date = sale_date

    def __str__(self):
        return (f"Sale ID: {self.sale_id} | Product: {self.product_id} | "
                f"Qty: {self.quantity_sold} @ ${self.sale_price:.2f} = ${self.total_amount:.2f}")

    def to_dict(self):
        return {
            "sale_id": self.sale_id,
            "product_id": self.product_id,
            "quantity_sold": self.quantity_sold,
            "sale_price": self.sale_price,
            "sale_date": self.sale_date,
            "total_amount": self.total_amount
        }
