import tkinter as tk
import sqlite3
import math
from tkinter import messagebox

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("db/calculator_history.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expression TEXT,
            result TEXT
        )
        """
    )
    conn.commit()
    conn.close()

# Save calculation to the database
def save_to_db(expression, result):
    conn = sqlite3.connect("db/calculator_history.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (expression, result) VALUES (?, ?)", (expression, result))
    conn.commit()
    conn.close()

# Fetch calculation history
def fetch_history():
    conn = sqlite3.connect("db/calculator_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT expression, result FROM history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Create the calculator GUI
class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x600")
        self.history_window_open = False
        
        # Create a frame for centering the calculator
        self.main_frame = tk.Frame(root)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Entry widget for displaying the expression and result
        self.display = tk.Entry(self.main_frame, font=("Arial", 20), borderwidth=2, relief="solid", width=15, justify="right", bg="#f1f1f1")
        self.display.grid(row=0, column=0, columnspan=4)

        # Buttons for numbers and operations
        self.buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2),
        ]

        # Adding buttons to the grid with colors
        for (text, row, col) in self.buttons:
            button_color = "#4CAF50" if text != "=" else "#ff5722"  # Highlighting the "=" button
            button = tk.Button(self.main_frame, text=text, font=("Arial", 15), width=5, height=2, command=lambda t=text: self.on_button_click(t), bg=button_color, fg="white", activebackground="#45a049", relief="raised")
            button.grid(row=row, column=col, padx=5, pady=5)

        # History and Clear Entry (CLR) buttons
        self.history_button = tk.Button(self.main_frame, text="History", font=("Arial", 15), width=5, height=2, command=self.show_history, bg="#2196F3", fg="white", activebackground="#1976D2", relief="raised")
        self.history_button.grid(row=6, column=0, columnspan=2, pady=5)
        
        self.clear_entry_button = tk.Button(self.main_frame, text="CLR", font=("Arial", 15), width=5, height=2, command=self.clear_entry, bg="#f44336", fg="white", activebackground="#e53935", relief="raised")
        self.clear_entry_button.grid(row=6, column=2, columnspan=2, pady=5)
        
        # Initialize database
        init_db()

    def on_button_click(self, text):
        current = self.display.get()
        if text == "=":
            try:
                result = str(eval(current))
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, result)
                save_to_db(current, result)
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        elif text in ['sin', 'cos', 'tan']:
            try:
                # Applying trigonometric functions in radians
                result = str(eval(f"math.{text}({current})"))
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, result)
                save_to_db(current, result)
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        else:
            self.display.insert(tk.END, text)

    def clear_entry(self):
        current = self.display.get()
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, current[:-1])  # Remove the last character

    def show_history(self):
        if not self.history_window_open:
            history_window = tk.Toplevel(self.root)
            history_window.title("History")
            history_window.geometry("400x300")
            history_listbox = tk.Listbox(history_window, font=("Arial", 12))
            history_listbox.pack(fill=tk.BOTH, expand=True)

            history = fetch_history()
            for expr, result in history:
                history_listbox.insert(tk.END, f"{expr} = {result}")
            
            self.history_window_open = True
            history_window.protocol("WM_DELETE_WINDOW", lambda: self.on_history_window_close(history_window))
    
    def on_history_window_close(self, window):
        self.history_window_open = False
        window.destroy()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

