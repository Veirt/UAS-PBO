"""
Tema: Hewan Peliharaan
Judul: Pet Shop

Penyimpanan eksternal: TSV (Tab Separated Values)
Mirip dengan CSV, tapi menggunakan tab sebagai pemisah. Memudahkan karena nama produk mungkin ada yang punya koma.
"""

import os
from typing import List


user_list = []


class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    # Buat user. Hanya input-input beserta validasinya.
    @staticmethod
    def input_user(admin=False):
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

        return User(username, password, role)

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
            print(f"{i + 1}. {user.username} - {user.role}")

        Utils.clear_and_continue()

    # Simpan user ke tsv.
    @staticmethod
    def save_to_file():
        with open("users.tsv", "w") as file:
            file.write("username\tpassword\trole\n")
            for user in user_list:
                file.write(f"{user.username}\t{user.password}\t{user.role}\n")

    # Ambil user dari tsv.
    @staticmethod
    def load_from_file():
        with open("users.tsv", "r") as file:
            lines = file.readlines()
            for line in lines[1:]:
                username, password, role = line.strip().split("\t")
                user_list.append(User(username, password, role))


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


product_list: List[Product] = []
