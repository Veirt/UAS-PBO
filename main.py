"""
Tema: Hewan Peliharaan
Judul: Pet Shop

Penyimpanan eksternal: TSV (Tab Separated Values)
Mirip dengan CSV, tapi menggunakan tab sebagai pemisah. Memudahkan karena nama produk mungkin ada yang punya koma.
"""

from utils import Utils
from user import User, Admin, Doctor
from pet import Pet
from product import Product


current_user: User | None = None

from payment import Payment

Payment.payment_method()

Product.load_from_file()
User.load_from_file()
Pet.load_from_file()

while True:
    print("Selamat datang di Pet Shop!")
    print("[0] Keluar dari aplikasi")
    print("[1] Login")
    print("[2] Daftar")
    print("[3] Lupa Password")

    choice = input("Pilihan: ")
    Utils.clear()

    if choice == "0":
        break
    elif choice == "1":
        current_user = User.login()
        if current_user is None:
            continue

        if current_user.role == "admin":
            Admin.menu(current_user)
        elif current_user.role == "doctor":
            Doctor.menu(current_user)
        else:
            User.menu(current_user)

    elif choice == "2":
        User.create_user()

    elif choice == "3":
        User.forgot_password()
    else:
        print()
        print("Pilihan tidak valid.")
        Utils.enter_and_continue()
    Utils.clear()
