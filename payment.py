from tkinter import Tk, Label, Frame, Toplevel
from PIL import Image, ImageTk
from utils import Utils


class Payment:
    @staticmethod
    def select_method():
        while True:
            print("Pilih metode pembayaran:")
            print("[1] Transfer")
            print("[2] QRIS")
            choice = input("Pilihan: ")

            if choice == "":
                print("Pilihan tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            if choice not in ["1", "2"]:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()
                continue

            break

        if choice == "1":
            Payment.show_bank_account()
        elif choice == "2":
            Payment.show_qr_code()

    @staticmethod
    def show_bank_account():
        root = Tk()
        root.title("Nomor Rekening")

        bank_account = Label(
            root, text="Nomor Rekening: 1234567890", font=("Arial", 16)
        )
        bank_account.pack(pady=20)

        def on_closing():
            root.destroy()
            root.quit()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        root.mainloop()

    @staticmethod
    def show_qr_code():
        root = Toplevel()
        root.title("QRIS")

        frame = Frame(root)
        frame.pack(pady=20)

        pet_shop_name = Label(frame, text="Pet Shop", font=("Arial", 24))
        pet_shop_name.pack()

        qr_code_image = Image.open("assets/qr.png")
        qr_code_photo = ImageTk.PhotoImage(qr_code_image)
        qr_code_label = Label(frame, image=qr_code_photo)  # type: ignore
        qr_code_label.pack()

        def on_closing():
            root.destroy()
            root.quit()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        root.mainloop()
