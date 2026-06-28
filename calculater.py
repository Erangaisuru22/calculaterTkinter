import tkinter as tk
import math

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("380x550")
        self.configure(bg="#201a1a")  # Dark background color
        
        # Track state for calculation
        self.current_value = "0"
        self.reset_on_next_keypress = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # --- Top Menu Area ---
        top_frame = tk.Frame(self, bg="#201a1a")
        top_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        menu_btn = tk.Label(top_frame, text="☰  Standard", fg="white", bg="#201a1a", font=("Segoe UI", 12, "bold"))
        menu_btn.pack(side="left")
        
        # --- Display Screen ---
        self.display = tk.Label(
            self, 
            text=self.current_value, 
            anchor="e", 
            fg="white", 
            bg="#201a1a", 
            font=("Segoe UI", 48), 
            padx=15, 
            pady=15
        )
        self.display.pack(fill="x")
        
        # --- Memory Buttons Row ---
        mem_frame = tk.Frame(self, bg="#201a1a")
        mem_frame.pack(fill="x", padx=10, pady=5)
        mem_buttons = ["MC", "MR", "M+", "M-", "MS"]
        for btn_text in mem_buttons:
            lbl = tk.Label(mem_frame, text=btn_text, fg="#a89f9f", bg="#201a1a", font=("Segoe UI", 9))
            lbl.pack(side="left", expand=True, fill="x")
            
        # --- Main Button Grid Layout ---
        grid_frame = tk.Frame(self, bg="#201a1a")
        grid_frame.pack(expand=True, fill="both", padx=4, pady=4)
        
        # Configure weights for uniform resizing
        for i in range(6):
            grid_frame.rowconfigure(i, weight=1)
        for j in range(4):
            grid_frame.columnconfigure(j, weight=1)
            
        # Defining the layout pattern match
        buttons = [
            ('%', 0, 0), ('CE', 0, 1), ('C', 0, 2), ('⌫', 0, 3),
            ('1/x', 1, 0), ('x²', 1, 1), ('²√x', 1, 2), ('÷', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('×', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('+/-', 5, 0), ('0', 5, 1), ('.', 5, 2), ('=', 5, 3)
        ]
        
        for text, row, col in buttons:
            # Color distinctions
            if text.isdigit() or text in ['.', '+/-']:
                bg_color = "#3b3434"      # Digit keys
                fg_color = "white"
            elif text == '=':
                bg_color = "#f28b70"      # Accent Action color (orange/coral)
                fg_color = "black"
            else:
                bg_color = "#302828"      # Operations / Control keys
                fg_color = "white"
                
            btn = tk.Button(
                grid_frame, 
                text=text, 
                bg=bg_color, 
                fg=fg_color, 
                font=("Segoe UI", 12),
                bd=0, 
                activebackground="#4a4242",
                activeforeground="white",
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

    def update_display(self, text):
        # Truncate or format safely if strings become too long
        if len(text) > 12:
            try:
                text = f"{float(text):.6g}"
            except ValueError:
                text = text[:12]
        self.display.config(text=text)

    def on_button_click(self, char):
        if char.isdigit():
            if self.current_value == "0" or self.reset_on_next_keypress:
                self.current_value = char
                self.reset_on_next_keypress = False
            else:
                self.current_value += char
            self.update_display(self.current_value)
            
        elif char == ".":
            if self.reset_on_next_keypress:
                self.current_value = "0."
                self.reset_on_next_keypress = False
            elif "." not in self.current_value:
                self.current_value += "."
            self.update_display(self.current_value)
            
        elif char == "C":
            self.current_value = "0"
            self.update_display(self.current_value)
            
        elif char == "CE":
            self.current_value = "0"
            self.update_display(self.current_value)
            
        elif char == "⌫":
            if len(self.current_value) > 1:
                self.current_value = self.current_value[:-1]
            else:
                self.current_value = "0"
            self.update_display(self.current_value)
            
        elif char == "+/-":
            if self.current_value != "0":
                if self.current_value.startswith("-"):
                    self.current_value = self.current_value[1:]
                else:
                    self.current_value = "-" + self.current_value
                self.update_display(self.current_value)
                
        elif char in ["+", "-", "×", "÷"]:
            # Basic expression assembly mapping
            op_map = {"×": "*", "÷": "/"}
            mapped_char = op_map.get(char, char)
            
            if self.reset_on_next_keypress:
                self.current_value = self.display.cget("text") + " " + mapped_char + " "
                self.reset_on_next_keypress = False
            else:
                if self.current_value == "0" and char == "-":
                    self.current_value = "-"
                else:
                    self.current_value += " " + mapped_char + " "
            self.update_display(char) # Briefly show operator symbol standard Windows UI style
            
        elif char in ["x²", "²√x", "1/x", "%"]:
            try:
                val = float(self.current_value.split()[-1]) # Use last entered number segment
                if char == "x²":
                    res = val ** 2
                elif char == "²√x":
                    res = math.sqrt(val)
                elif char == "1/x":
                    res = 1 / val
                elif char == "%":
                    res = val / 100
                
                # Replace the last element or whole expression
                self.current_value = str(int(res) if res.is_integer() else res)
                self.update_display(self.current_value)
            except Exception:
                self.update_display("Error")
                self.current_value = "0"
                
        elif char == "=":
            try:
                # Sanitize input and evaluate expression safely
                expr = self.current_value
                # Calculate evaluation safely
                result = eval(expr)
                
                # Format to strip unnecessary floating trailing zeroes
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                    
                self.current_value = str(result)
                self.update_display(self.current_value)
                self.reset_on_next_keypress = True
            except Exception:
                self.update_display("Error")
                self.current_value = "0"

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
