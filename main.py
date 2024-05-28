"""
Tema: Hewan Peliharaan
Judul: Pet Shop

Penyimpanan eksternal: TSV (Tab Separated Values)
Mirip dengan CSV, tapi menggunakan tab sebagai pemisah. Memudahkan karena nama produk mungkin ada yang punya koma.
"""

import os
from typing import List


class User:
    def __init__(self, name, username, password, role):
        self.name = name
        self.username = username
        self.password = password
        self.role = role

    # Buat user. Hanya input-input beserta validasinya.
    @staticmethod
    def input_user(admin=False):
        while True:
            nama = input("Nama: ")
            # Validasi nama ga boleh kosong.
            if nama == "":
                print("Nama tidak boleh kosong.")
                Utils.clear_and_continue()
                continue

            break

        while True:
            username = input("Username: ")
            # Validasi username ga boleh kosong.
            if username == "":
                print("Username tidak boleh kosong.")
                Utils.clear_and_continue()
                continue

            # Validasi username harus unik.
            if any(user.username == username for user in user_list):
                print("Username sudah ada.")
                Utils.clear_and_continue()
                continue

            break

        while True:
            password = input("Password: ")
            # Validasi password ga boleh kosong.
            if password == "":
                print("Password tidak boleh kosong.")
                Utils.clear_and_continue()
                continue

            break

        # Default role adalah user.
        role = "user"

        # Jika admin, maka bisa pilih role.
        if admin:
            while True:
                role_dict = {"1": "user", "2": "admin", "3": "doctor"}
                print("Role: ")
                print("[1] User")
                print("[2] Admin")
                print("[3] Doctor")
                role = input("Role: ")

                # Validasi role ga boleh kosong.
                if role == "":
                    print("Role tidak boleh kosong.")
                    Utils.clear_and_continue()
                    continue

                if role not in role_dict.keys():
                    print("Role tidak valid.")
                    Utils.clear_and_continue()
                    continue

                role = role_dict[role]

                break

        return User(nama, username, password, role)

    @staticmethod
    def create_user():
        user = User.input_user()
        user_list.append(user)

        print("User berhasil ditambahkan.")

        User.save_to_file()
        Utils.clear_and_continue()

    @staticmethod
    def list_user():
        print("Daftar User: ")
        for i, user in enumerate(user_list):
            print(f"{i + 1}. {user.name} - {user.username} - {user.role}")

        Utils.clear_and_continue()

    # Simpan user ke tsv.
    @staticmethod
    def save_to_file():
        with open("users.tsv", "w") as file:
            file.write("nama\tusername\tpassword\trole\n")
            for user in user_list:
                file.write(
                    f"{user.name}\t{user.username}\t{user.password}\t{user.role}\n"
                )

    # Ambil user dari tsv.
    @staticmethod
    def load_from_file():
        with open("users.tsv", "r") as file:
            lines = file.readlines()
            for line in lines[1:]:
                name, username, password, role = line.strip().split("\t")
                user = User(name, username, password, role)
                user_list.append(user)

    @staticmethod
    def login():
        username = input("Username: ")
        password = input("Password: ")

        # Cek apakah username dan password ada di user_list.
        user = next((user for user in user_list if user.username == username), None)

        if user is not None and user.password == password:
            print("Login berhasil.")
            Utils.clear_and_continue()

            return user

        print("Username atau password salah.")
        Utils.clear_and_continue()

        return None

    @staticmethod
    def menu():
        while True:
            Utils.clear()
            print("Menu User")
            print("[0] Kembali")
            print("[1] Katalog Produk")

            choice = input("Pilihan: ")

            if choice == "0":
                break
            elif choice == "1":
                pass

    @staticmethod
    def forgot_password():
        username = input("Username: ")
        name = input("Nama: ")
        # Cari user berdasarkan username dan name.
        user = next(
            (
                user
                for user in user_list
                if user.username == username and user.name == name
            ),
            None,
        )

        if user is None:
            print("Username atau nama salah.")
            Utils.clear_and_continue()
            return

        new_password = input("Password baru: ")
        user.password = new_password

        print("Password berhasil diubah.")
        Utils.clear_and_continue()

        User.save_to_file()


class Admin(User):
    def __init__(self, name, username, password, role):
        super().__init__(name, username, password, role)

    @staticmethod
    def menu():
        while True:
            Utils.clear()
            print("Menu Admin")
            print("[0] Kembali")
            print("[1] Tambah User")
            print("[2] Lihat User")
            print("[3] Tambah Produk")
            print("[4] Lihat Produk")

            choice = input("Pilihan: ")

            if choice == "0":
                break
            elif choice == "1":
                User.create_user()
            elif choice == "2":
                User.list_user()
            elif choice == "3":
                Product.create_product()
            elif choice == "4":
                Product.list_product()


class Doctor(User):
    def __init__(self, name, username, password, role):
        super().__init__(name, username, password, role)

    @staticmethod
    def menu():
        while True:
            Utils.clear()
            print("Menu Dokter")
            print("[0] Kembali")
            print("[1] Lihat User")
            print("[2] Lihat Produk")

            choice = input("Pilihan: ")

            if choice == "0":
                break
            elif choice == "1":
                User.list_user()
            elif choice == "2":
                Product.list_product()


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
    def clear_and_continue():
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


class Product:
    def __init__(self, name, price, stock, category):
        self.name = name
        self.price = price
        self._stock = stock
        self.category = category

    def get_price_formatted(self):
        return Utils.format_rupiah(self.price)

    # Enkapsulasi pada stock
    def get_stock(self):
        return self._stock

    def decrease_stock(self, amount):
        if self._stock < amount:
            print("Stok tidak cukup.")
            Utils.clear_and_continue()
            return False

        self._stock -= amount

    def increase_stock(self, amount):
        self._stock += amount

    def set_stock(self, amount):
        if amount < 0:
            print("Stok tidak boleh negatif.")
            Utils.clear_and_continue()
            return False

        self._stock = amount

    # Buat produknya. Hanya input-input beserta validasinya.
    @staticmethod
    def input_product():
        while True:
            name = input("Nama produk: ")
            # Validasi nama produk ga boleh kosong.
            if name == "":
                print("Nama produk tidak boleh kosong.")
                Utils.clear_and_continue()
                continue

            # Validasi nama produk harus unik.
            if any(product.name == name for product in product_list):
                print("Nama produk sudah ada.")
                Utils.clear_and_continue()
                continue

            break

        while True:
            price = input("Harga produk: ")
            # Validasi harga produk harus angka valid.
            if not price.isdigit():
                print("Harga produk harus angka yang valid.")
                Utils.clear_and_continue()
                continue

            price = int(price)

            break

        while True:
            stock = input("Stok produk: ")
            # Validasi stok produk harus angka.
            if not stock.isdigit():
                print("Stok produk harus angka yang valid.")
                Utils.clear_and_continue()
                continue

            stock = int(stock)

            break

        while True:
            category_dict = {
                "1": "hewan",
                "2": "makanan",
                "3": "mainan",
                "4": "aksesoris",
                "5": "lainnya",
            }
            print("Kategori Produk: ")
            print("[1] Hewan")
            print("[2] Makanan")
            print("[3] Mainan")
            print("[4] Aksesoris (Kalung, Pakaian, dll.)")
            print("[5] Lainnya")
            category = input("Kategori produk: ")
            # Validasi kategori produk ga boleh kosong.
            if category == "":
                print("Kategori produk tidak boleh kosong.")
                Utils.clear_and_continue()
                continue

            if category not in category_dict.keys():
                print("Kategori produk tidak valid.")
                Utils.clear_and_continue()
                continue

            category = category_dict[category]

            break

        return Product(name, price, stock, category)

    @staticmethod
    def create_product():
        product = Product.input_product()
        product_list.append(product)

        print("Produk berhasil ditambahkan.")

        Product.save_to_file()
        Utils.clear_and_continue()

    @staticmethod
    def list_product():
        print("Daftar Produk: ")
        for i, product in enumerate(product_list):
            print(
                f"{i + 1}. {product.name} - {product.get_price_formatted()} - {product.get_stock()} - {product.category}"
            )

        Utils.clear_and_continue()

    # Simpan produk dari tsv.
    @staticmethod
    def save_to_file():
        with open("products.tsv", "w") as file:
            file.write("nama\tharga\tstok\tkategori\n")
            for product in product_list:
                file.write(
                    f"{product.name}\t{product.price}\t{product.get_stock()}\t{product.category}\n"
                )

    # Ambil produk dari tsv.
    @staticmethod
    def load_from_file():
        with open("products.tsv", "r") as file:
            lines = file.readlines()
            for line in lines[1:]:
                name, price, stock, category = line.strip().split("\t")
                product_list.append(
                    Product(name, int(price), int(stock), category.title())
                )


user_list: List[User] = []
product_list: List[Product] = []

Product.load_from_file()
User.load_from_file()

while True:
    print("Selamat datang di Pet Shop!")
    print("[0] Keluar dari aplikasi")
    print("[1] Login")
    print("[2] Daftar")
    print("[3] Lupa Password")

    choice = input("Pilihan: ")

    if choice == "0":
        break
    elif choice == "1":
        current_user = User.login()
        if current_user is None:
            continue

        if current_user.role == "admin":
            Admin.menu()
        elif current_user.role == "doctor":
            Doctor.menu()
        else:
            User.menu()

    elif choice == "2":
        User.create_user()

    elif choice == "3":
        User.forgot_password()

    Utils.clear()
