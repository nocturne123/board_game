import tkinter as tk


class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")

        # display
        self.display = tk.Entry(master, width=20, font=("Arial", 16), justify="right")
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # button
        buttons = [
            "7",
            "8",
            "9",
            "/",
            "4",
            "5",
            "6",
            "*",
            "1",
            "2",
            "3",
            "-",
            "0",
            ".",
            "+",
            "=",
        ]

        # Add buttons
        row = 1
        col = 0
        for button_text in buttons:
            button = tk.Button(
                master,
                text=button_text,
                width=5,
                height=2,
                font=("Arial", 16),
                command=lambda value=button_text: self.click(value),
            )
            button.grid(row=row, column=col, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1

    def click(self, key):
        if key == "=":
            # Evaluate the expression and display the result
            try:
                result = str(eval(self.display.get()))
            except:
                result = "ERROR"
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, result)
        elif key == "C":
            # Clear the display
            self.display.delete(0, tk.END)
        else:
            # Append the key text to the display
            self.display.insert(tk.END, key)


root = tk.Tk()
app = Calculator(root)
root.mainloop()
