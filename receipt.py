import tkinter as tk
from tkinter import ttk

from utils import Utils


class Receipt:
    def create_receipt(self, shopping_cart):
        root = tk.Tk()
        root.title("Receipt")
        root.geometry("500x600")  # Set the initial window size
        root.resizable(False, False)  # Disable window resizing

        # Create a title label
        title_label = tk.Label(root, text="Receipt", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # Create a frame for the receipt text
        receipt_frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=2)
        receipt_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Create the monospace font
        monospace_font = ("Courier", 12)

        # Create the receipt text widget
        receipt_text = tk.Text(
            receipt_frame, font=monospace_font, width=40, height=20, state="disabled"
        )
        receipt_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Generate the receipt text
        receipt = ""
        total = 0
        for product, amount in shopping_cart:
            receipt += f"{product.name} x {amount} - {Utils.format_rupiah(product.price * amount)}\n"
            total += product.price * amount

        receipt += f"\nTotal: {Utils.format_rupiah(total)}"
        receipt_text.configure(state="normal")  # Enable text editing temporarily
        receipt_text.insert(tk.END, receipt)
        receipt_text.configure(state="disabled")  # Disable text editing again

        # Create a button frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        def on_closing():
            root.destroy()
            root.quit()

        close_button = ttk.Button(button_frame, text="Close", command=on_closing)
        close_button.pack(side=tk.RIGHT, padx=10)

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
