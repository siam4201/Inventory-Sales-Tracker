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
    except IOError as e:
        print(f"Uh oh, there was an issue loading your files: {str(e)}")
        
        error_root = tk.Tk()
        error_root.withdraw()
        messagebox.showerror("Data Load Warning", f"We couldn't load your data files:\n{str(e)}")
        error_root.destroy()
    except Exception as e:
        print(f"Uh oh, something went wrong starting the app: {str(e)}")

if __name__ == "__main__":
    main()
