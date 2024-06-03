import tkinter as tk
from tkinter import ttk
from utils import Utils

monospace_font = ("Courier", 12)


class Receipt:
    def create_receipt(self, title, content):
        root = tk.Tk()
        root.title(title)
        root.geometry("500x400")
        root.resizable(False, False)

        title_label = tk.Label(root, text=title, font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        receipt_frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=2)
        receipt_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        receipt_text = tk.Text(receipt_frame, font=monospace_font, width=40, height=10)
        receipt_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        receipt_text.insert(tk.END, content)
        receipt_text.configure(state="disabled")

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        def on_closing():
            root.destroy()
            root.quit()

        close_button = ttk.Button(button_frame, text="Close", command=on_closing)
        close_button.pack(side=tk.RIGHT, padx=10)

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()

    def create_shop_receipt(self, shopping_cart):
        receipt = ""
        total = 0
        for product, amount in shopping_cart:
            receipt += f"{product.name} x {amount} - {Utils.format_rupiah(product.price * amount)}\n"
            total += product.price * amount
        receipt += f"\nTotal: {Utils.format_rupiah(total)}"
        self.create_receipt("Receipt", receipt)

    def create_adoption_receipt(self, item):
        receipt = ""
        receipt += f"Nama Hewan: {item.name}\n"
        receipt += f"Jenis Hewan: {item.species}\n"
        receipt += f"Umur Hewan: {item.age}\n"
        receipt += f"Deskripsi: {item.description}\n"
        receipt += f"Biaya Adopsi: {Utils.format_rupiah(item.price)}\n"
        self.create_receipt("Adoption Receipt", receipt)

    def create_health_check_receipt(self, item):
        receipt = f"Pemilik: {item.user.name}\n"
        receipt += f"Jenis Hewan: {item.pet_type}\n"
        receipt += f"Penyakit: {item.disease}\n"
        receipt += f"Obat: {item.medicine}\n"
        receipt += f"Harga: {Utils.format_rupiah(item.price)}\n"
        self.create_receipt("Health Check Receipt", receipt)

    def create_pet_care_receipt(self, item):
        receipt = f"Pemilik: {item.user.name}\n"
        receipt += f"Jenis Hewan: {item.pet_type}\n"
        receipt += f"Jenis Paket: {item.package}\n"
        receipt += f"Harga: {Utils.format_rupiah(item.price)}"
        self.create_receipt("Pet Care Receipt", receipt)
