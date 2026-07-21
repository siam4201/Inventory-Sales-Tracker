import tkinter as tk
from tkinter import ttk, messagebox

class InventoryApp:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        
        self.root.title("Basic Inventory Tool")
        self.root.geometry("800x600")
        
        self.lbl_welcome = tk.Label(self.root, text="Welcome to Inventory App (WIP)", font=("Arial", 16))
        self.lbl_welcome.pack(pady=30)
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tab_dash = ttk.Frame(self.notebook)
        self.tab_inv = ttk.Frame(self.notebook)
        self.tab_sales = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_dash, text=" My Dashboard ")
        self.notebook.add(self.tab_inv, text=" Manage Stock ")
        self.notebook.add(self.tab_sales, text=" Log a Sale ")
