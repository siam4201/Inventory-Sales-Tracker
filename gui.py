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
        
    def build_dashboard(self):
                               
        card_frame = tk.Frame(self.tab_dash, bg="#18181b")
        card_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(card_frame, text="Dashboard under construction...", fg="white", bg="#18181b").pack()
