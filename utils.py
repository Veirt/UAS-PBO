from tkinter import Toplevel, Frame, Label
from PIL import Image, ImageTk
import os


# Utility class.
# Isinya method-method kayak clear screen, press enter to continue.
class Utils:
    @staticmethod
    def clear():
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    @staticmethod
    def enter_and_continue():
        input("Press Enter to continue...")
        Utils.clear()

    # Ubah format angka jadi format rupiah.
    @staticmethod
    def format_rupiah(amount):
        formatted_amount = f"{amount:,.2f}"
        formatted_amount = (
            formatted_amount.replace(",", "X").replace(".", ",").replace("X", ".")
        )

        return f"Rp. {formatted_amount}"

    # Tampilkan gambar hewan peliharaan di window baru
    @staticmethod
    def show_image(image_path):
        root = Toplevel()
        root.title("Foto Hewan")

        frame = Frame(root)
        frame.pack(pady=20)

        pet_image = Image.open(image_path)
        pet_photo = ImageTk.PhotoImage(pet_image)
        pet_label = Label(frame, image=pet_photo)  # type: ignore
        pet_label.pack()

        def on_closing():
            root.destroy()
            root.quit()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        root.mainloop()
