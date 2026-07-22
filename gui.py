import tkinter as tk
from tkinter import ttk, messagebox

class InventoryApp:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        
        self.root.title("My Inventory & Sales Tracker")
        self.root.geometry("1000x650")
        self.root.configure(bg="#18181b")
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tab_dash = ttk.Frame(self.notebook)
        self.tab_inv = ttk.Frame(self.notebook)
        self.tab_sales = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_dash, text=" My Dashboard ")
        self.notebook.add(self.tab_inv, text=" Manage Stock ")
        self.notebook.add(self.tab_sales, text=" Log a Sale ")
        
        self.build_dashboard()
        self.build_inventory_manager()
        
    def build_dashboard(self):
        pass                          

    def build_inventory_manager(self):
        search_f = tk.Frame(self.tab_inv, bg="#18181b")
        search_f.pack(fill=tk.X, pady=5)
        
        tk.Label(search_f, text="Find a product:", fg="white", bg="#18181b").pack(side=tk.LEFT, padx=5)
        self.ent_search = ttk.Entry(search_f)
        self.ent_search.pack(side=tk.LEFT, padx=5)
        
        tk.Label(search_f, text="Filter by type:", fg="white", bg="#18181b").pack(side=tk.LEFT, padx=(15, 5))
        self.cmb_filter = ttk.Combobox(search_f, values=["All"] + list(self.manager.get_categories()), state="readonly", width=12)
        self.cmb_filter.current(0)
        self.cmb_filter.pack(side=tk.LEFT, padx=5)
        
        self.inv_tree = ttk.Treeview(self.tab_inv, columns=("id", "name", "cat", "price", "qty", "alert"), show="headings")
        self.setup_cols(self.inv_tree, {
            "id": ("ID", 70), "name": ("Name", 200), "cat": ("Type", 120),
            "price": ("Price", 90), "qty": ("In Stock", 70), "alert": ("Min Stock", 90)
        })
        self.inv_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        form = tk.Frame(self.tab_inv, bg="#18181b")
        form.pack(fill=tk.X, pady=10)
        form.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        self.inputs = {}
        fields = [("Product ID", "id"), ("Name", "name"), ("Price ($)", "price"), ("Stock Qty", "qty"), ("Min Stock", "thresh")]
        
        for idx, (label, key) in enumerate(fields):
            f_frame = tk.Frame(form, bg="#18181b")
            f_frame.grid(row=0, column=idx, padx=3, sticky="ew")
            tk.Label(f_frame, text=label, font=("Segoe UI", 9), fg="#8f9ca8", bg="#18181b").pack(anchor=tk.W)
            self.inputs[key] = ttk.Entry(f_frame)
            self.inputs[key].pack(fill=tk.X, pady=2)
            
        cat_frame = tk.Frame(form, bg="#18181b")
        cat_frame.grid(row=0, column=5, padx=3, sticky="ew")
        tk.Label(cat_frame, text="Type", font=("Segoe UI", 9), fg="#8f9ca8", bg="#18181b").pack(anchor=tk.W)
        self.inputs["cat"] = ttk.Combobox(cat_frame, values=self.manager.get_categories(), state="readonly")
        self.inputs["cat"].pack(fill=tk.X, pady=2)
        
        btn_frame = tk.Frame(self.tab_inv, bg="#18181b")
        btn_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Button(btn_frame, text=" Add New Product ").pack(side=tk.LEFT, padx=5, ipadx=10)
        tk.Button(btn_frame, text=" Save Changes ").pack(side=tk.LEFT, padx=5, ipadx=10)
        tk.Button(btn_frame, text=" Remove Product ").pack(side=tk.LEFT, padx=5, ipadx=10)
        tk.Button(btn_frame, text=" Clear Form ").pack(side=tk.LEFT, padx=5, ipadx=10)

    def setup_cols(self, tree, col_dict):
        for col, (text, width) in col_dict.items():
            tree.heading(col, text=text)
            tree.column(col, width=width, anchor=tk.W if col in ("name", "cat") else tk.CENTER)
        tree.pack(fill=tk.BOTH, expand=True)
