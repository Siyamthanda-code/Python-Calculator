import tkinter as tk
from tkinter import ttk
# pylint: disable=E0401
import numexpr as ne
import numpy as np
import math #Import the math module for trigonometric functions

#Define trigFunction FIRST
def trigFunction(func):
    result = None
    radians = None
    
    try:
        value = float(result_var.get()) #Get the current input
        
        if func in ["sin", "cos", "tan"]:
            radians = math.radians(value)
        if func == 'sin':
            result = math.sin(radians)
        elif func == 'cos':
            result = math.cos(radians)
        elif func == 'tan':
            result = math.tan(radians)
            
        elif func in ["asin", "acos", "atan"]:
            if func == 'asin' and -1 <= value <= 1:
                radians = math.asin(value)
                result = math.degrees(math.asin(value)) 
        elif func == 'acos' and -1 <= value <= 1:
            radians = math.acos(value)
            result = math.degrees(math.acos(value)) 
        elif func == 'atan':
            radians = math.atan(value)
            result = math.degrees(radians) #Convert back to degrees
            
            if result is not None:
                result_var.set(result)
            else:
                result_var.set("Error")
                
    except ValueError:
        result_var.set("Error")

def handle_button_click(clicked_button_text):
    current_text = result_var.get()
    
    if clicked_button_text in ["sin", "cos", "tan", "asin", "acos", "atan"]:
        if current_text and current_text not in ["Error", "Domain Error"]:
            try:
                value = float(current_text)
                if clicked_button_text == "sin":
                    result =math.sin(math.radians(value))
                elif clicked_button_text == "cos":
                    result =math.cos(math.radians(value))
                elif clicked_button_text == "tan":
                    result =math.tan(math.radians(value))
                elif clicked_button_text == "asin":
                    if -1 <= value <= 1:
                        result = math.degrees(math.asin(value))
                    else:
                        result = "Domain Error"
                elif clicked_button_text == "acos":
                    if -1 <= value <= 1:
                        result = math.degrees(math.acos(value))
                    else:
                        result = "Domain Error"  
                elif clicked_button_text == "atan":
                    result = math.degrees(math.atan(value))  
                    
                    
                if isinstance(result, float): 
                    result = round(result, 10)  
                    result_var.set(result)
            except ValueError:
                result_var.set("Error")
        else:
            result_var.set("Error")
        return

    if clicked_button_text == "=":
        try:
            # Replace custom symbols with Python operators
            expression = current_text.replace("÷", "/").replace("×", "*")
            expression = expression.replace("√", "math.sqrt").replace("^", "**")
            
            # Evaluate the expression using numexpr
            result = ne.evaluate(expression)

            # Check if the result is a whole number
            if np.issubdtype(type(result), np.integer):
                result = int(result)

            result_var.set(result)
        except ZeroDivisionError:
            result_var.set("Div/0 Error")
        except (ValueError, SyntaxError):
            result_var.set("Input Error")
            
    elif clicked_button_text == "C":
        result_var.set("")
        
    elif clicked_button_text == "%":
        try:
            current_number = float(current_text)
            result_var.set(current_number / 100)
        except ValueError:
            result_var.set("Error")
            
    elif clicked_button_text == "±":
        try:
            current_number = float(current_text)
            result_var.set(-current_number)
        except ValueError:
            result_var.set("Error")
            
    elif clicked_button_text in ["sin", "cos", "tan", "asin", "acos", "atan", "√"]:
        if clicked_button_text == "√":
            try:
                value = float(current_text)
                if value >= 0:
                    result_var.set(math.sqrt(value))
                else:
                    result_var.set("Error")
            except ValueError:
                result_var.set("Error")
        else:
            trigFunction(clicked_button_text)
    else:
        if current_text == "0" or current_text == "Error":
            result_var.set(clicked_button_text)
        else:
            result_var.set(current_text + clicked_button_text)

# Create the main window
root = tk.Tk()
root.title("Scientific Calculator")

# Entry widget to display the result with larger font size
result_var = tk.StringVar()
result_entry = ttk.Entry(root, textvariable=result_var, font=("Helvetica", 24), justify="right")
result_entry.grid(row=0, column=0, columnspan=4, sticky="nsew")

# Button layout
buttons = [
    ("C", 1, 0), ("±", 1, 1), ("%", 1, 2), ("÷", 1, 3),
    ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("×", 2, 3),
    ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
    ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
    ("0", 5, 0, 2), (".", 5, 2), ("=", 5, 3),
    ("√", 6, 0), ("^", 6, 1), ("sin", 6, 2), ("cos", 6, 3),
    ("tan", 7, 0), ("asin", 7, 1), ("acos", 7, 2), ("atan", 7, 3)
]

# Configure style for theme
style = ttk.Style()
style.theme_use('default')
style.configure("TButton", font=("Helvetica", 16), width=10, height=4)

# Create buttons and add them to the grid
for button_info in buttons:
    button_text, row, col = button_info[:3]
    colspan = button_info[3] if len(button_info) > 3 else 1
    button = ttk.Button(root, text=button_text, command=lambda text=button_text: handle_button_click(text), style="TButton")
    button.grid(row=row, column=col, columnspan=colspan, sticky="nsew", ipadx=10, ipady=4, padx=5, pady=5)

# Configure row and column weights so that they expand proportionally
for i in range(8):
    root.grid_rowconfigure(i, weight=1)

for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# Set the window size to a 9:16 ratio
width = 500
height = 800
root.geometry(f"{width}x{height}")

# Make the window non-resizable
root.resizable(False, False)

# Keyboard control
root.bind("<Return>", lambda event: handle_button_click("="))
root.bind("<BackSpace>", lambda event: handle_button_click("C"))

# Run the main loop
root.mainloop()
