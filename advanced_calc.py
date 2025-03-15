import tkinter as tk
from tkinter import font, messagebox
import math

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("500x700")
        self.current_theme = "dark"
        self.memory = 0
        self.history = []

        # Custom font
        self.custom_font = font.Font(family="Helvetica", size=18, weight="bold")

        # Entry widget for input and results
        self.entry = tk.Entry(root, font=self.custom_font, justify="right", bd=10, relief=tk.RIDGE)
        self.entry.grid(row=0, column=0, columnspan=5, pady=20, padx=10, sticky="nsew")

        # History display
        self.history_label = tk.Label(root, text="History", font=self.custom_font)
        self.history_label.grid(row=1, column=0, columnspan=5, sticky="nsew")
        self.history_text = tk.Text(root, height=5, font=("Helvetica", 12), state="disabled")
        self.history_text.grid(row=2, column=0, columnspan=5, padx=10, pady=5, sticky="nsew")

        # Buttons layout
        buttons = [
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('/', 3, 3), ('C', 3, 4),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('*', 4, 3), ('√', 4, 4),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('-', 5, 3), ('^', 5, 4),
            ('0', 6, 0), ('.', 6, 1), ('%', 6, 2), ('+', 6, 3), ('=', 6, 4),
            ('sin', 7, 0), ('cos', 7, 1), ('tan', 7, 2), ('log', 7, 3), ('ln', 7, 4),
            ('M+', 8, 0), ('M-', 8, 1), ('MR', 8, 2), ('MC', 8, 3), ('Theme', 8, 4),
            (')', 9, 0)  # Closing braces button
        ]

        # Create buttons
        for button in buttons:
            text, row, col = button
            btn = tk.Button(root, text=text, font=self.custom_font, bd=5, relief=tk.RAISED,
                            command=lambda t=text: self.on_button_click(t))
            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

        # Configure grid weights
        for i in range(10):
            root.grid_rowconfigure(i, weight=1)
        for i in range(5):
            root.grid_columnconfigure(i, weight=1)

        # Apply initial theme
        self.configure_theme()

        # Bind keyboard events
        self.bind_keyboard_events()

    def configure_theme(self):
        if self.current_theme == "dark":
            self.root.configure(bg="#2E3440")
            self.entry.configure(bg="#4C566A", fg="#ECEFF4")
            self.history_label.configure(bg="#2E3440", fg="#ECEFF4")
            self.history_text.configure(bg="#3B4252", fg="#ECEFF4")
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.configure(bg="#5E81AC", fg="#ECEFF4")
        else:
            self.root.configure(bg="#FFFFFF")
            self.entry.configure(bg="#E0E0E0", fg="#000000")
            self.history_label.configure(bg="#FFFFFF", fg="#000000")
            self.history_text.configure(bg="#F0F0F0", fg="#000000")
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.configure(bg="#D3D3D3", fg="#000000")

    def on_button_click(self, text):
        if text == '=':
            self.calculate_result()
        elif text == 'C':
            self.entry.delete(0, tk.END)
        elif text == '√':
            self.entry.insert(tk.END, 'sqrt(')
        elif text == '^':
            self.entry.insert(tk.END, '**')
        elif text == '%':
            self.handle_percentage()
        elif text in ['sin', 'cos', 'tan', 'log', 'ln']:
            self.entry.insert(tk.END, f"{text}(")
        elif text in ['M+', 'M-', 'MR', 'MC']:
            self.handle_memory(text)
        elif text == 'Theme':
            self.switch_theme()
        elif text == ')':
            self.entry.insert(tk.END, ')')
        else:
            self.entry.insert(tk.END, text)

    def calculate_result(self):
        try:
            expression = self.entry.get()
            result = str(eval(expression))
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, result)
            self.add_to_history(f"{expression} = {result}")
        except Exception as e:
            messagebox.showerror("Error", "Invalid Expression")

    def handle_percentage(self):
        try:
            expression = self.entry.get()
            result = str(eval(expression) / 100)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", "Invalid Percentage Calculation")

    def handle_memory(self, operation):
        if operation == 'M+':
            self.memory += float(self.entry.get())
        elif operation == 'M-':
            self.memory -= float(self.entry.get())
        elif operation == 'MR':
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(self.memory))
        elif operation == 'MC':
            self.memory = 0

    def add_to_history(self, calculation):
        self.history.append(calculation)
        self.history_text.config(state="normal")
        self.history_text.insert(tk.END, calculation + "\n")
        self.history_text.config(state="disabled")

    def switch_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.configure_theme()

    def bind_keyboard_events(self):
        # Override default key handling to prevent duplicates
        self.root.bind("<Key>", self.on_key_press)

    def on_key_press(self, event):
        # Prevent Tkinter's default key handling
        if event.char in '0123456789+-*/.()':
            self.entry.insert(tk.END, event.char)
            return "break"  # Stop Tkinter from processing the key again
        elif event.keysym == 'Return':
            self.calculate_result()
            return "break"
        elif event.keysym == 'BackSpace':
            self.entry.delete(len(self.entry.get()) - 1, tk.END)
            return "break"
        elif event.keysym == 'Escape':
            self.entry.delete(0, tk.END)
            return "break"

if __name__ == "__main__":
    root = tk.Tk()
    calculator = AdvancedCalculator(root)
    root.mainloop()