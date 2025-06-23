# main.py
import tkinter as tk
from src.gui import QuadraticFormulaApp

if __name__ == "__main__":
    root = tk.Tk()
    app = QuadraticFormulaApp(root)
    root.mainloop()