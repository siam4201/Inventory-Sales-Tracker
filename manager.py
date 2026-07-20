import os
import json
from models import Product

class InventoryManager:
    CATEGORIES = ("Electronics", "Clothing", "Groceries", "Home & Kitchen", "Books", "Other")

    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.products = {}
        self.product_ids_set = set()
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        self.inventory_file = os.path.join(self.data_dir, "inventory.json")
        self.load_data()

    def get_categories(self):
        return self.CATEGORIES

    def get_product_ids(self):
        return self.product_ids_set

    def load_data(self):
        need_sample_inventory = not os.path.exists(self.inventory_file) or os.path.getsize(self.inventory_file) == 0

        try:
            if need_sample_inventory:
                self._load_sample_products(save=False)
            else:
                with open(self.inventory_file, 'r') as f:
                    data = json.load(f)
                    for item_data in data:
                        product = Product(
                            item_data["product_id"],
                            item_data["name"],
                            item_data["category"],
                            item_data["price"],
                            item_data["quantity"],
                            item_data["low_stock_threshold"]
                        )
                        self.products[product.item_id] = product
                        self.product_ids_set.add(product.item_id)
        except json.JSONDecodeError:
            backup_file = self.inventory_file + ".corrupted"
            if os.path.exists(self.inventory_file):
                os.rename(self.inventory_file, backup_file)
            self._load_sample_products(save=False)
        except Exception as e:
            raise IOError(f"Error loading inventory: {str(e)}")

        if need_sample_inventory:
            self.save_data()

    def save_data(self):
        try:
            with open(self.inventory_file, 'w') as f:
                json.dump([p.to_dict() for p in self.products.values()], f, indent=4)
        except Exception as e:
            raise IOError(f"Failed to save data: {str(e)}")

    def _load_sample_products(self, save=True):
        samples = [
            ("P101", "Gaming Laptop", "Electronics", 1200.00, 15, 5),
            ("P102", "Wireless Mouse", "Electronics", 25.50, 40, 10),
            ("P103", "Cotton T-Shirt", "Clothing", 19.99, 100, 15),
            ("P104", "Running Shoes", "Clothing", 85.00, 30, 8),
            ("P105", "Organic Milk 1L", "Groceries", 3.49, 50, 12),
        ]
        self.products.clear()
        self.product_ids_set.clear()
        for p_id, name, cat, price, qty, threshold in samples:
            product = Product(p_id, name, cat, price, qty, threshold)
            self.products[p_id] = product
            self.product_ids_set.add(p_id)
        if save:
            self.save_data()

    def add_product(self, p_id, name, category, price, quantity, threshold):
                                 
        p_id = p_id.strip().upper()
        if p_id in self.product_ids_set:
            raise ValueError(f"Product ID '{p_id}' is already taken.")
            
        if category not in self.CATEGORIES:
            raise ValueError(f"Invalid Category. Allowed: {self.CATEGORIES}")
            
        try:
            price_val = float(price)
            qty_val = int(quantity)
            thresh_val = int(threshold)
        except ValueError:
            raise ValueError("Price must be a number, and Quantity/Min Stock must be whole numbers.")

        new_prod = Product(p_id, name.strip(), category, price_val, qty_val, thresh_val)
        self.products[p_id] = new_prod
        self.product_ids_set.add(p_id)
        self.save_data()
        return new_prod

    def update_product(self, p_id, name=None, category=None, price=None, quantity=None, threshold=None):
                            
        p_id = p_id.strip().upper()
        product = self.products[p_id]
        if name: product.name = name.strip()
        if category: product.category = category
        if price is not None: product.price = float(price)
        if quantity is not None: product.quantity = int(quantity)
        if threshold is not None: product.low_stock_threshold = int(threshold)

        self.save_data()
        return product

    def delete_product(self, p_id):
        p_id = p_id.strip().upper()
        deleted_prod = self.products.pop(p_id)
        self.product_ids_set.discard(p_id)
        self.save_data()
        return deleted_prod
