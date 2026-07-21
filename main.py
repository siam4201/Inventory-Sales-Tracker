import tkinter as tk
from tkinter import messagebox
from manager import InventoryManager
from gui import InventoryApp

def main():
    try:
        manager = InventoryManager(data_dir="data")
        root = tk.Tk()
        app = InventoryApp(root, manager)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
