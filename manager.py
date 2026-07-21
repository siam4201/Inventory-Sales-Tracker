import os
import json
import statistics
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
        need_sample_inventory = not os.path.exists(self.inventory_file) or os.path.getsize(self.inventory_file) == 0
        need_sample_sales = not os.path.exists(self.sales_file) or os.path.getsize(self.sales_file) == 0

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

        try:
            if need_sample_sales:
                self._load_sample_sales(save=False)
            else:
                with open(self.sales_file, 'r') as f:
                    data = json.load(f)
                    for sale_data in data:
                        sale = Sale(
                            sale_data["sale_id"],
                            sale_data["product_id"],
                            sale_data["quantity_sold"],
                            sale_data["sale_price"],
                            sale_data["sale_date"]
                        )
                        self.sales.append(sale)
        except json.JSONDecodeError:
            backup_file = self.sales_file + ".corrupted"
            if os.path.exists(self.sales_file):
                os.rename(self.sales_file, backup_file)
            self._load_sample_sales(save=False)
        except Exception as e:
            raise IOError(f"Error loading sales data: {str(e)}")

        if need_sample_inventory or need_sample_sales:
            self.save_data()

    def save_data(self):
        try:
            with open(self.inventory_file, 'w') as f:
                json.dump([p.to_dict() for p in self.products.values()], f, indent=4)
                
            with open(self.sales_file, 'w') as f:
                json.dump([s.to_dict() for s in self.sales], f, indent=4)
        except Exception as e:
            raise IOError(f"Failed to save data: {str(e)}")

    def _load_sample_products(self, save=True):
        samples = [
            ("P101", "Gaming Laptop", "Electronics", 1200.00, 15, 5),
            ("P102", "Wireless Mouse", "Electronics", 25.50, 40, 10),
            ("P103", "Cotton T-Shirt", "Clothing", 19.99, 100, 15),
            ("P104", "Running Shoes", "Clothing", 85.00, 30, 8),
            ("P105", "Organic Milk 1L", "Groceries", 3.49, 50, 12),
            ("P106", "Wheat Bread", "Groceries", 2.29, 60, 15),
            ("P107", "Chef Knife 8-inch", "Home & Kitchen", 45.00, 20, 5),
            ("P108", "Non-Stick Frying Pan", "Home & Kitchen", 35.00, 3, 5),
            ("P109", "Python Programming", "Books", 49.99, 25, 6),
            ("P110", "Introduction to NumPy", "Books", 39.99, 8, 10),
        ]
        self.products.clear()
        self.product_ids_set.clear()
        for p_id, name, cat, price, qty, threshold in samples:
            product = Product(p_id, name, cat, price, qty, threshold)
            self.products[p_id] = product
            self.product_ids_set.add(p_id)
        if save:
            self.save_data()

    def _load_sample_sales(self, save=True):
        samples = [
            ("S1001", "P101", 2, 1200.00, "2026-07-01 10:15:30.000000"),
            ("S1002", "P102", 5, 25.50, "2026-07-02 14:20:00.000000"),
            ("S1003", "P105", 10, 3.49, "2026-07-03 09:05:15.000000"),
            ("S1004", "P109", 3, 49.99, "2026-07-04 16:45:00.000000"),
            ("S1005", "P103", 12, 19.99, "2026-07-05 11:30:00.000000"),
        ]
        self.sales.clear()
        for s_id, p_id, qty, price, date in samples:
            self.sales.append(Sale(s_id, p_id, qty, price, date))
        if save:
            self.save_data()

    def add_product(self, p_id, name, category, price, quantity, threshold):
        if not p_id or not name or not category:
            raise ValueError("Product ID, Name, and Type cannot be empty.")
            
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

        if price_val < 0 or qty_val < 0 or thresh_val < 0:
            raise ValueError("Values cannot be negative.")

        new_prod = Product(p_id, name.strip(), category, price_val, qty_val, thresh_val)
        self.products[p_id] = new_prod
        self.product_ids_set.add(p_id)
        self.save_data()
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

        self.save_data()
        return product

    def delete_product(self, p_id):
        p_id = p_id.strip().upper()
        if p_id not in self.products:
            raise KeyError(f"Product ID '{p_id}' not found.")
            
        deleted_prod = self.products.pop(p_id)
        self.product_ids_set.discard(p_id)
        self.save_data()
        return deleted_prod
    
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

    def get_total_inventory_value(self):
        return sum(p.price * p.quantity for p in self.products.values())

    def get_sales_statistics(self):
        if not self.sales:
            return {"total_revenue": 0.0, "mean": 0.0, "median": 0.0, "std_dev": 0.0, "min": 0.0, "max": 0.0, "count": 0}
            
        revenues = [s.total_amount for s in self.sales]
        return {
            "total_revenue": sum(revenues),
            "mean": statistics.mean(revenues),
            "median": statistics.median(revenues),
            "std_dev": statistics.stdev(revenues) if len(revenues) > 1 else 0.0,
            "min": min(revenues),
            "max": max(revenues),
            "count": len(revenues)
        }

    def get_category_distribution(self):
        cat_stats = {}
        for cat in self.CATEGORIES:
            cat_products = [p for p in self.products.values() if p.category == cat]
            if not cat_products:
                cat_stats[cat] = {"count": 0, "total_value": 0.0, "avg_price": 0.0}
            else:
                cat_stats[cat] = {
                    "count": sum(p.quantity for p in cat_products),
                    "total_value": sum(p.price * p.quantity for p in cat_products),
                    "avg_price": sum(p.price for p in cat_products) / len(cat_products)
                }
        return cat_stats

    def get_low_stock_items(self):
        return [p for p in self.products.values() if p.quantity <= p.low_stock_threshold]