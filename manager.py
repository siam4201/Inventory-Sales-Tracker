import os
import json
from models import Product, Sale

class InventoryManager:
    CATEGORIES = ("Electronics", "Clothing", "Groceries", "Home & Kitchen", "Books", "Other")

    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.products = {}
        self.sales = []
        self.product_ids_set = set()
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        self.inventory_file = os.path.join(self.data_dir, "inventory.json")
        self.sales_file = os.path.join(self.data_dir, "sales.json")
        self.load_data()

    def get_categories(self): return self.CATEGORIES
    def get_product_ids(self): return self.product_ids_set

    def load_data(self):
                                                                                     
        pass

    def record_sale(self, p_id, quantity_sold):
        p_id = p_id.strip().upper()
        if p_id not in self.products:
            raise KeyError(f"Product ID '{p_id}' not found.")
            
        qty_sold = int(quantity_sold)
        product = self.products[p_id]
        product.update_stock(-qty_sold)
        
        ids = [int(s.sale_id[1:]) for s in self.sales if s.sale_id.startswith("S") and s.sale_id[1:].isdigit()]
        next_id_num = max(ids) + 1 if ids else 1001
        
        new_sale = Sale(f"S{next_id_num}", p_id, qty_sold, product.price)
        self.sales.append(new_sale)
        return new_sale
