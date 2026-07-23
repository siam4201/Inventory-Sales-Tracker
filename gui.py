import tkinter as tk
from tkinter import ttk, messagebox

class InventoryApp:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        
        self.root.title("My Inventory & Sales Tracker")
        self.root.geometry("1000x650")
        self.root.configure(bg="#18181b")
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.bg_dark = "#18181b"
        self.bg_card = "#27272a"
        self.fg_light = "#f4f4f5"
        self.accent = "#3b82f6"
        self.danger = "#ef4444"
        self.input_bg = "#3f3f46"
        self.font_main = ("Segoe UI", 10)
        self.font_bold = ("Segoe UI", 10, "bold")
        
        self.style.configure(".", background=self.bg_dark, foreground=self.fg_light, font=self.font_main)
        self.style.configure("TNotebook", background=self.bg_dark, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.bg_card, foreground=self.fg_light, font=self.font_bold, padding=[16, 6])
        self.style.map("TNotebook.Tab", background=[("selected", self.accent)], foreground=[("selected", "#ffffff")])
        
        self.style.configure("TEntry", fieldbackground=self.input_bg, foreground=self.fg_light, insertcolor=self.fg_light, borderwidth=0, padding=4)
        self.style.configure("TCombobox", fieldbackground=self.input_bg, foreground=self.fg_light, arrowcolor=self.fg_light, borderwidth=0, padding=4)
        self.style.map("TCombobox", fieldbackground=[("readonly", self.input_bg)], foreground=[("readonly", self.fg_light)])
        
        self.root.option_add("*TCombobox*Listbox.background", self.input_bg)
        self.root.option_add("*TCombobox*Listbox.foreground", self.fg_light)
        self.root.option_add("*TCombobox*Listbox.selectBackground", self.accent)
        self.root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")
        
        self.style.configure("Treeview", background=self.bg_card, fieldbackground=self.bg_card, foreground=self.fg_light, rowheight=28, font=self.font_main, borderwidth=0)
        self.style.configure("Treeview.Heading", background=self.input_bg, foreground=self.fg_light, font=self.font_bold, padding=4, borderwidth=0)
        self.style.map("Treeview", background=[("selected", self.accent)], foreground=[("selected", "#ffffff")])
        
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
        self.build_sales_manager()
        
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.refresh_views())
        self.refresh_views()

    def build_dashboard(self):
        card_frame = tk.Frame(self.tab_dash, bg=self.bg_dark)
        card_frame.pack(fill=tk.X, pady=10)
        
        self.card_inv = self.create_card(card_frame, "Total Stock Value", "$0.00", "#4cd137")
        self.card_rev = self.create_card(card_frame, "Total Sales Revenue", "$0.00", self.accent)
        self.card_warn = self.create_card(card_frame, "Low Stock Alerts", "0 Items", self.danger)
        
        lists_frame = tk.Frame(self.tab_dash, bg=self.bg_dark)
        lists_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        f_left = ttk.LabelFrame(lists_frame, text=" Recent Sales ")
        f_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.dash_sales = ttk.Treeview(f_left, columns=("id", "qty", "tot", "date"), show="headings")
        self.setup_cols(self.dash_sales, {"id": ("Product ID", 90), "qty": ("Qty", 50), "tot": ("Total", 90), "date": ("Date", 100)})
        
        f_right = ttk.LabelFrame(lists_frame, text=" Low Stock ")
        f_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        self.dash_warns = ttk.Treeview(f_right, columns=("id", "name", "qty"), show="headings")
        self.setup_cols(self.dash_warns, {"id": ("ID", 70), "name": ("Name", 150), "qty": ("In Stock", 70)})

    def create_card(self, parent, title, initial_val, color):
        card = tk.Frame(parent, bg=self.bg_card, bd=0)
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=5, ipady=12)
        
        tk.Frame(card, bg=color, height=4).pack(fill=tk.X, side=tk.TOP)
        tk.Label(card, text=title, font=("Segoe UI", 9, "bold"), fg="#a1a1aa", bg=self.bg_card).pack(anchor=tk.W, padx=12, pady=(10, 0))
        lbl_v = tk.Label(card, text=initial_val, font=("Segoe UI", 20, "bold"), fg=self.fg_light, bg=self.bg_card)
        lbl_v.pack(anchor=tk.W, padx=12, pady=(2, 2))
        return lbl_v

    def build_inventory_manager(self):
        search_f = tk.Frame(self.tab_inv, bg=self.bg_dark)
        search_f.pack(fill=tk.X, pady=5)
        
        tk.Label(search_f, text="Find a product:", fg=self.fg_light, bg=self.bg_dark).pack(side=tk.LEFT, padx=5)
        self.ent_search = ttk.Entry(search_f)
        self.ent_search.pack(side=tk.LEFT, padx=5)
        self.ent_search.bind("<KeyRelease>", lambda e: self.filter_inventory())
        
        tk.Label(search_f, text="Filter by type:", fg=self.fg_light, bg=self.bg_dark).pack(side=tk.LEFT, padx=(15, 5))
        
        self.cmb_filter = ttk.Combobox(search_f, values=["All"] + list(self.manager.get_categories()), state="readonly", width=12)
        self.cmb_filter.current(0)
        self.cmb_filter.pack(side=tk.LEFT, padx=5)
        self.cmb_filter.bind("<<ComboboxSelected>>", lambda e: self.filter_inventory())
        
        self.inv_tree = ttk.Treeview(self.tab_inv, columns=("id", "name", "cat", "price", "qty", "alert"), show="headings")
        self.setup_cols(self.inv_tree, {
            "id": ("ID", 70), "name": ("Name", 200), "cat": ("Type", 120),
            "price": ("Price", 90), "qty": ("In Stock", 70), "alert": ("Min Stock", 90)
        })
        self.inv_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        self.inv_tree.bind("<<TreeviewSelect>>", self.on_product_select)
        
        form = tk.Frame(self.tab_inv, bg=self.bg_dark)
        form.pack(fill=tk.X, pady=10)
        form.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        self.inputs = {}
        fields = [("Product ID", "id"), ("Name", "name"), ("Price ($)", "price"), ("Stock Qty", "qty"), ("Min Stock", "thresh")]
        
        for idx, (label, key) in enumerate(fields):
            f_frame = tk.Frame(form, bg=self.bg_dark)
            f_frame.grid(row=0, column=idx, padx=3, sticky="ew")
            tk.Label(f_frame, text=label, font=("Segoe UI", 9), fg="#8f9ca8", bg=self.bg_dark).pack(anchor=tk.W)
            self.inputs[key] = ttk.Entry(f_frame)
            self.inputs[key].pack(fill=tk.X, pady=2)
            
        cat_frame = tk.Frame(form, bg=self.bg_dark)
        cat_frame.grid(row=0, column=5, padx=3, sticky="ew")
        tk.Label(cat_frame, text="Type", font=("Segoe UI", 9), fg="#8f9ca8", bg=self.bg_dark).pack(anchor=tk.W)
        self.inputs["cat"] = ttk.Combobox(cat_frame, values=self.manager.get_categories(), state="readonly")
        self.inputs["cat"].pack(fill=tk.X, pady=2)
        
        btn_frame = tk.Frame(self.tab_inv, bg=self.bg_dark)
        btn_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Button(btn_frame, text=" Add New Product ", bg=self.accent, fg=self.bg_dark, font=("Segoe UI", 9, "bold"), bd=0, command=self.add_product).pack(side=tk.LEFT, padx=5, ipadx=10)
        tk.Button(btn_frame, text=" Save Changes ", bg="#fbc531", fg=self.bg_dark, font=("Segoe UI", 9, "bold"), bd=0, command=self.update_product).pack(side=tk.LEFT, padx=5, ipadx=10)
        tk.Button(btn_frame, text=" Remove Product ", bg=self.danger, fg=self.fg_light, font=("Segoe UI", 9, "bold"), bd=0, command=self.delete_product).pack(side=tk.LEFT, padx=5, ipadx=10)
        tk.Button(btn_frame, text=" Clear Form ", bg=self.bg_card, fg=self.fg_light, font=("Segoe UI", 9), bd=0, command=self.clear_form).pack(side=tk.LEFT, padx=5, ipadx=10)

    def build_sales_manager(self):
        record_f = tk.Frame(self.tab_sales, bg=self.bg_dark)
        record_f.pack(fill=tk.X, pady=10)
        
        tk.Label(record_f, text="Choose a product to sell:", fg=self.fg_light, bg=self.bg_dark).pack(side=tk.LEFT, padx=5)
        self.cmb_sales_prod = ttk.Combobox(record_f, state="readonly", width=30)
        self.cmb_sales_prod.pack(side=tk.LEFT, padx=5)
        self.cmb_sales_prod.bind("<<ComboboxSelected>>", lambda e: self.update_sales_preview())
        
        tk.Label(record_f, text="How many?", fg=self.fg_light, bg=self.bg_dark).pack(side=tk.LEFT, padx=(15, 5))
        self.ent_sales_qty = ttk.Entry(record_f, width=8)
        self.ent_sales_qty.pack(side=tk.LEFT, padx=5)
        self.ent_sales_qty.bind("<KeyRelease>", lambda e: self.update_sales_preview())
        
        self.lbl_sales_preview = tk.Label(record_f, text="Total: $0.00 (In Stock: -)", font=("Segoe UI", 10, "bold"), fg="#ffbc42", bg=self.bg_dark)
        self.lbl_sales_preview.pack(side=tk.LEFT, padx=15)
        
        tk.Button(record_f, text=" Confirm Sale ", bg=self.accent, fg=self.bg_dark, font=("Segoe UI", 9, "bold"), bd=0, command=self.submit_sale).pack(side=tk.LEFT, padx=5, ipadx=15)
        
        self.sales_tree = ttk.Treeview(self.tab_sales, columns=("id", "pid", "qty", "price", "total", "date"), show="headings")
        self.setup_cols(self.sales_tree, {
            "id": ("Sale ID", 80), "pid": ("Product ID", 90), "qty": ("Qty", 70),
            "price": ("Unit Price", 90), "total": ("Total Amount", 100), "date": ("Date/Time", 140)
        })
        self.sales_tree.pack(fill=tk.BOTH, expand=True, pady=5)

    def setup_cols(self, tree, col_dict):
        for col, (text, width) in col_dict.items():
            tree.heading(col, text=text)
            tree.column(col, width=width, anchor=tk.W if col in ("name", "cat") else tk.CENTER)
        tree.pack(fill=tk.BOTH, expand=True)

    def refresh_views(self):
        self.card_inv.config(text=f"${self.manager.get_total_inventory_value():,.2f}")
        self.card_rev.config(text=f"${self.manager.get_sales_statistics()['total_revenue']:,.2f}")
        
        warns = self.manager.get_low_stock_items()
        self.card_warn.config(text=f"{len(warns)} Items")
        
        self.dash_sales.delete(*self.dash_sales.get_children())
        sorted_sales = sorted(self.manager.sales, key=lambda s: s.sale_date, reverse=True)
        for s in sorted_sales[:5]:
            self.dash_sales.insert("", tk.END, values=(s.product_id, s.quantity_sold, f"${s.total_amount:.2f}", s.sale_date.split(" ")[0]))
            
        self.dash_warns.delete(*self.dash_warns.get_children())
        for p in warns[:5]:
            self.dash_warns.insert("", tk.END, values=(p.item_id, p.name, p.quantity))
            
        self.filter_inventory()
        
        sorted_prods = sorted(self.manager.products.values(), key=lambda p: p.item_id)
        self.cmb_sales_prod["values"] = [f"{p.item_id} | {p.name}" for p in sorted_prods]
        
        self.sales_tree.delete(*self.sales_tree.get_children())
        sorted_sales_by_id = sorted(self.manager.sales, key=lambda s: s.sale_id, reverse=True)
        for s in sorted_sales_by_id:
            self.sales_tree.insert("", tk.END, values=(s.sale_id, s.product_id, s.quantity_sold, f"${s.sale_price:.2f}", f"${s.total_amount:.2f}", s.sale_date.split(".")[0]))

    def filter_inventory(self):
        query = self.ent_search.get().lower().strip()
        cat_filter = self.cmb_filter.get()
        self.inv_tree.delete(*self.inv_tree.get_children())
        
        for p in self.manager.products.values():
            match_query = not query or query in p.item_id.lower() or query in p.name.lower()
            match_cat = cat_filter == "All" or p.category == cat_filter
            if match_query and match_cat:
                self.inv_tree.insert("", tk.END, values=(p.item_id, p.name, p.category, f"${p.price:.2f}", p.quantity, p.low_stock_threshold))

    def on_product_select(self, event):
        selected = self.inv_tree.selection()
        if not selected:
            return
            
        vals = self.inv_tree.item(selected[0], "values")
        self.clear_form()
        
        self.inputs["id"].insert(0, vals[0])
        self.inputs["id"].config(state="disabled")
        self.inputs["name"].insert(0, vals[1])
        self.inputs["cat"].set(vals[2])
        self.inputs["price"].insert(0, vals[3].replace("$", ""))
        self.inputs["qty"].insert(0, vals[4])
        self.inputs["thresh"].insert(0, vals[5])

    def clear_form(self):
        self.inputs["id"].config(state="normal")
        for ent in self.inputs.values():
            if isinstance(ent, ttk.Combobox):
                ent.set("")
            else:
                ent.delete(0, tk.END)

    def add_product(self):
        pass

    def __disabled_add_product(self):
        try:
            p = self.manager.add_product(
                self.inputs["id"].get().strip(),
                self.inputs["name"].get().strip(),
                self.inputs["cat"].get().strip(),
                self.inputs["price"].get().strip(),
                self.inputs["qty"].get().strip(),
                self.inputs["thresh"].get().strip()
            )
            messagebox.showinfo("Success", f"Product '{p.name}' added successfully.")
            self.clear_form()
            self.refresh_views()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_product(self):
        pass

    def __disabled_update_product(self):
        p_id = self.inputs["id"].get().strip()
        if not p_id: return
        
        try:
            self.manager.update_product(
                p_id,
                name=self.inputs["name"].get().strip(),
                category=self.inputs["cat"].get().strip(),
                price=self.inputs["price"].get().strip(),
                quantity=self.inputs["qty"].get().strip(),
                threshold=self.inputs["thresh"].get().strip()
            )
            messagebox.showinfo("Success", "Product details updated successfully.")
            self.clear_form()
            self.refresh_views()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_product(self):
        pass

    def __disabled_delete_product(self):
        p_id = self.inputs["id"].get().strip()
        if not p_id: return
        if messagebox.askyesno("Confirm Delete", f"Delete product {p_id}?"):
            try:
                self.manager.delete_product(p_id)
                self.clear_form()
                self.refresh_views()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def update_sales_preview(self):
        sel = self.cmb_sales_prod.get()
        qty_s = self.ent_sales_qty.get().strip()
        if not sel: return
            
        p_id = sel.split(" | ")[0]
        prod = self.manager.products.get(p_id)
        if not prod: return
        
        try:
            total = int(qty_s) * prod.price if qty_s else 0
            self.lbl_sales_preview.config(text=f"Total: ${total:.2f} (In Stock: {prod.quantity})")
        except ValueError:
            self.lbl_sales_preview.config(text=f"Total: $0.00 (In Stock: {prod.quantity})")

    def submit_sale(self):
        pass

    def __disabled_submit_sale(self):
        sel = self.cmb_sales_prod.get()
        qty_s = self.ent_sales_qty.get().strip()
        if not sel or not qty_s: return
            
        p_id = sel.split(" | ")[0]
        try:
            sale = self.manager.record_sale(p_id, int(qty_s))
            messagebox.showinfo("Success", f"Recorded sale {sale.sale_id}.")
            self.cmb_sales_prod.set("")
            self.ent_sales_qty.delete(0, tk.END)
            self.lbl_sales_preview.config(text="Total: $0.00 (In Stock: -)")
            self.refresh_views()
            
            p = self.manager.products.get(p_id)
            if p and p.is_low_stock():
                messagebox.showwarning("Low Stock", f"Product '{p.name}' is low on stock ({p.quantity} left).")
        except Exception as e:
            messagebox.showerror("Sale Error", str(e))
