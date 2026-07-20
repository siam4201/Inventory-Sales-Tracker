import os
import json
from models import Product

class InventoryManager:
    CATEGORIES = ("Electronics", "Clothing", "Groceries", "Home & Kitchen", "Books", "Other")

    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.products = {}
        self.product_ids_set = set()

    def get_categories(self):
        return self.CATEGORIES

    def get_product_ids(self):
        return self.product_ids_set

    def add_product(self, p_id, name, category, price, quantity, threshold):
                                                           
        print(f"DEBUG: Adding product {p_id}")
        new_prod = Product(p_id, name, category, price, quantity, threshold)
        self.products[p_id] = new_prod
        self.product_ids_set.add(p_id)
        return new_prod

    def update_product(self, p_id, name=None, category=None, price=None, quantity=None, threshold=None):
        p_id = p_id.strip().upper()
        if p_id not in self.products:
            raise KeyError(f"Product ID '{p_id}' not found.")
            
        product = self.products[p_id]
        
        if name is not None:
            if not name.strip(): raise ValueError("Product Name cannot be empty.")
            product.name = name.strip()
            
        if category is not None:
            if category not in self.CATEGORIES: raise ValueError("Invalid Product Type.")
            product.category = category
            
        if price is not None:
            if float(price) < 0: raise ValueError("Price cannot be negative.")
            product.price = float(price)
            
        if quantity is not None:
            if int(quantity) < 0: raise ValueError("Quantity cannot be negative.")
            product.quantity = int(quantity)
            
        if threshold is not None:
            if int(threshold) < 0: raise ValueError("Minimum stock cannot be negative.")
            product.low_stock_threshold = int(threshold)

        return product

    def delete_product(self, p_id):
        p_id = p_id.strip().upper()
        if p_id not in self.products:
            raise KeyError(f"Product ID '{p_id}' not found.")
            
        deleted_prod = self.products.pop(p_id)
        self.product_ids_set.discard(p_id)
        return deleted_prod
