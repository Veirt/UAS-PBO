"""
File yang berisi class-class yang berhubungan dengan user.
Termasuk, User, Admin, dan Doctor.

User: user biasa
Admin: admin (Manajemen)
Doctor: dokter (mengecek pelayanan)
"""

from typing import List
from payment import Payment
from utils import Utils
from product import Product
from shop import Shop
from service import PetCare, Service, HealthCheck, pet_care_queue, health_check_list
from pet import Pet
from receipt import Receipt

import pwinput


class User:
    def __init__(self, name, username, password, role):
        self.name = name
        self.username = username
        self.password = password
        self.role = role
        self._shopping_cart = []

    def get_shopping_cart_total(self):
        total = 0
        for product, amount in self._shopping_cart:
            total += product.price * amount

        return total

    # Lihat isi keranjang belanja.
    def get_shopping_cart_items(self, interactive=False):
        if len(self._shopping_cart) == 0:
            if interactive:
                print("Keranjang belanja kosong.")
                Utils.enter_and_continue()

            return

        print("Keranjang Belanja: ")
        for product, amount in self._shopping_cart:
            print(
                f"* {product.name} - {product.get_price_formatted()} - Jumlah: {amount}"
            )

        print()
        print(f"Total: {Utils.format_rupiah(self.get_shopping_cart_total())}")

        print()

        if interactive:
            Utils.enter_and_continue()

    def add_to_shopping_cart(self, product, amount):
        # Cek apakah produk sudah ada di keranjang.
        for i, (p, a) in enumerate(self._shopping_cart):
            if p is product:
                self._shopping_cart[i] = (p, amount)
                print("Jumlah produk berhasil diubah.")
                break
        else:
            self._shopping_cart.append((product, amount))
            print("Produk berhasil ditambahkan ke keranjang.")

    def remove_from_shopping_cart(self):
        if len(self._shopping_cart) == 0:
            print("Keranjang belanja kosong.")
            Utils.enter_and_continue()
            return

        print("[0] Kembali")
        for i, (p, a) in enumerate(self._shopping_cart):
            print(f"[{i + 1}] {p.name} - {p.get_price_formatted()} - Jumlah: {a}")

        choice = input("Pilihan: ")

        if choice == "0":
            return

        try:
            index = int(choice) - 1
            self._shopping_cart.pop(index)
            print("Produk berhasil dihapus dari keranjang.")
        except (ValueError, IndexError):
            print("Pilihan tidak valid.")

        Utils.enter_and_continue()

    def checkout(self):
        Payment.select_method()

        for product, amount in self._shopping_cart:
            product.decrease_stock(amount)

        Product.save_to_file()
        print("Pembelian berhasil!")
        receipt = Receipt()
        receipt.create_shop_receipt(self._shopping_cart)
        self._shopping_cart = []

    # Buat user. Hanya input-input beserta validasinya.
    @staticmethod
    def input_user(admin=False):
        while True:
            nama = input("Nama: ")
            # Validasi nama ga boleh kosong.
            if nama == "":
                print("Nama tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            break

        while True:
            username = input("Username: ")
            # Validasi username ga boleh kosong.
            if username == "":
                print("Username tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            # Validasi username harus unik.
            if any(user.username == username for user in user_list):
                print("Username sudah ada.")
                Utils.enter_and_continue()
                continue

            break

        while True:
            password = pwinput.pwinput(prompt="Password: ")
            # Validasi password ga boleh kosong.
            if password == "":
                print("Password tidak boleh kosong.")
                Utils.enter_and_continue()
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
                    Utils.enter_and_continue()
                    continue

                if role not in role_dict.keys():
                    print("Role tidak valid.")
                    Utils.enter_and_continue()
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
        Utils.enter_and_continue()

    @staticmethod
    def list_user():
        print("Daftar User: ")
        for i, user in enumerate(user_list):
            print(f"{i + 1}. {user.name} - {user.username} - {user.role}")

        Utils.enter_and_continue()

    @staticmethod
    def update_user():
        if not user_list:
            print("Tidak ada user yang terdaftar.")
            Utils.enter_and_continue()
            return

        print("Daftar User:")
        for i, user in enumerate(user_list):
            print(f"[{i + 1}] {user.name} - {user.username} - {user.role}")

        choice = input("Pilih nomor user yang ingin diubah (0 untuk kembali): ")

        if choice == "0":
            return

        try:
            index = int(choice) - 1
            user = user_list[index]
        except (ValueError, IndexError):
            print("Pilihan tidak valid.")
            Utils.enter_and_continue()
            return

        new_user = User.input_user(admin=True)
        user_list[index] = new_user

        print("User berhasil diubah.")
        Utils.enter_and_continue()

        User.save_to_file()

    @staticmethod
    def delete_user():
        if not user_list:
            print("Tidak ada user yang terdaftar.")
            Utils.enter_and_continue()
            return

        print("Daftar User:")
        for i, user in enumerate(user_list):
            print(f"[{i + 1}] {user.name} - {user.username} - {user.role}")

        choice = input("Pilih nomor user yang ingin dihapus (0 untuk kembali): ")

        if choice == "0":
            return

        try:
            index = int(choice) - 1
            user = user_list.pop(index)
            print(f"User {user.name} ({user.username}) berhasil dihapus.")
        except (ValueError, IndexError):
            print("Pilihan tidak valid.")
            Utils.enter_and_continue()
            return

        User.save_to_file()
        Utils.enter_and_continue()

    # Simpan user ke tsv.
    @staticmethod
    def save_to_file():
        with open("data/users.tsv", "w") as file:
            file.write("nama\tusername\tpassword\trole\n")
            for user in user_list:
                file.write(
                    f"{user.name}\t{user.username}\t{user.password}\t{user.role}\n"
                )

    # Ambil user dari tsv.
    @staticmethod
    def load_from_file():
        with open("data/users.tsv", "r") as file:
            lines = file.readlines()
            for line in lines[1:]:
                name, username, password, role = line.strip().split("\t")
                user = User(name, username, password, role)
                user_list.append(user)

    @staticmethod
    def login():
        username = input("Username: ")
        password = pwinput.pwinput(prompt="Password: ")

        # Cek apakah username dan password ada di user_list.
        user = next((user for user in user_list if user.username == username), None)

        if user is not None and user.password == password:
            print("Login berhasil.")
            Utils.enter_and_continue()

            return user

        print("Username atau password salah.")
        Utils.enter_and_continue()

        return None

    @staticmethod
    def menu(current_user):
        while True:
            Utils.clear()
            print("Menu User")
            print("[0] Kembali")
            print("[1] Toko / Belanja")
            print("[2] Layanan")
            print("[3] Adopsi")

            choice = input("Pilihan: ")
            Utils.clear()

            if choice == "0":
                break
            elif choice == "1":
                Shop.menu(current_user)
            elif choice == "2":
                Service.menu(current_user)
            elif choice == "3":
                Pet.adoption_menu()
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()

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
            Utils.enter_and_continue()
            return

        if user.role == "admin":
            print("Tidak bisa reset password admin.")
            Utils.enter_and_continue()
            return

        while True:
            new_password = pwinput.pwinput(prompt="Password baru: ")
            if new_password == "":
                print("Password tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            break

        user.password = new_password

        print("Password berhasil diubah.")
        Utils.enter_and_continue()

        User.save_to_file()


class Admin(User):
    def __init__(self, name, username, password, role):
        super().__init__(name, username, password, role)

    @staticmethod
    def menu(current_user):
        while True:
            Utils.clear()
            print("Menu Admin")
            print("[0] Kembali")
            print("[1] Manajemen User")
            print("[2] Manajemen Produk")
            print("[3] Manajemen Hewan Adopsi")
            print("[4] Riwayat Layanan")

            choice = input("Pilihan: ")
            Utils.clear()

            if choice == "0":
                break
            elif choice == "1":
                Admin.user_management_submenu()
            elif choice == "2":
                Admin.product_management_submenu()
            elif choice == "3":
                Admin.pet_management_submenu()
            elif choice == "4":
                Admin.service_history_submenu()
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()

    @staticmethod
    def user_management_submenu():
        while True:
            Utils.clear()
            print("Manajemen User")
            print("[0] Kembali")
            print("[1] Tambah User")
            print("[2] Lihat User")
            print("[3] Ubah User")
            print("[4] Hapus User")
            choice = input("Pilihan: ")
            Utils.clear()
            if choice == "0":
                break
            elif choice == "1":
                User.create_user()
            elif choice == "2":
                User.list_user()
            elif choice == "3":
                User.update_user()
            elif choice == "4":
                User.delete_user()
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()

    @staticmethod
    def product_management_submenu():
        while True:
            Utils.clear()
            print("Manajemen Produk")
            print("[0] Kembali")
            print("[1] Tambah Produk")
            print("[2] Lihat Produk")
            print("[3] Ubah Produk")
            print("[4] Hapus Produk")
            print("[5] Ubah Stok Produk")
            choice = input("Pilihan: ")
            Utils.clear()
            if choice == "0":
                break
            elif choice == "1":
                Product.create_product()
            elif choice == "2":
                Product.list_product()
            elif choice == "3":
                Product.update_product()
            elif choice == "4":
                Product.delete_product()
            elif choice == "5":
                Product.change_stock()
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()

    @staticmethod
    def pet_management_submenu():
        while True:
            Utils.clear()
            print("Manajemen Hewan Adopsi")
            print("[0] Kembali")
            print("[1] Tambah Hewan Adopsi")
            print("[2] Lihat Hewan yang Tersedia")
            print("[3] Ubah Hewan Adopsi")
            print("[4] Hapus Hewan Adopsi")
            choice = input("Pilihan: ")
            Utils.clear()
            if choice == "0":
                break
            elif choice == "1":
                Pet.create_pet()
            elif choice == "2":
                Pet.read_all()
            elif choice == "3":
                Pet.update_pet()
            elif choice == "4":
                Pet.delete_pet()
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()

    @staticmethod
    def service_history_submenu():
        while True:
            Utils.clear()
            print("Riwayat Layanan")
            print("[0] Kembali")
            print("[1] Riwayat Pengecekan Kesehatan Hewan")
            print("[2] Riwayat Perawatan Hewan")

            choice = input("Pilihan: ")
            Utils.clear()

            if choice == "0":
                break
            elif choice == "1":
                Service.view_all_health_check_history()
            elif choice == "2":
                Service.view_all_pet_care_history()
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()


class Doctor(User):
    def __init__(self, name, username, password, role):
        super().__init__(name, username, password, role)

    @staticmethod
    def menu(current_user):
        while True:
            Utils.clear()
            print("Menu Dokter")
            print("[0] Kembali")
            print("[1] Lihat Antrean Kesehatan")
            print("[2] Lihat Antrean Perawatan")
            print("[3] Proses Antrean Kesehatan")
            print("[4] Proses Antrean Perawatan")

            choice = input("Pilihan: ")
            Utils.clear()

            if choice == "0":
                break
            elif choice == "1":
                Doctor.view_health_check_queue()
            elif choice == "2":
                Doctor.view_pet_care_queue()
            elif choice == "3":
                Doctor.process_health_check_queue()
            elif choice == "4":
                Doctor.process_pet_care_queue()
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()

    @staticmethod
    def view_health_check_queue():
        current_queue = [item for item in health_check_list if item.status == "Waiting"]
        if not current_queue:
            print("Antrean kesehatan kosong.")
            Utils.enter_and_continue()
            return

        print("Antrean Pengecekan Kesehatan:")
        for item in current_queue:
            print(f"* {str(item)}")

        print()
        Utils.enter_and_continue()

    @staticmethod
    def view_pet_care_queue():
        current_queue = [item for item in pet_care_queue if item.status == "Waiting"]
        if not current_queue:
            print("Antrean perawatan kosong.")
            Utils.enter_and_continue()
            return

        print("Antrean Perawatan Hewan:")
        for item in current_queue:
            print(f"* {str(item)}")

        print()
        Utils.enter_and_continue()

    @staticmethod
    def process_health_check_queue():
        current_queue = [item for item in health_check_list if item.status == "Waiting"]
        if not current_queue:
            print("Tidak ada antrean pengecekan kesehatan hewan yang menunggu.")
            Utils.enter_and_continue()
            return

        print("Antrean Pengecekan Kesehatan Hewan:")
        for i, item in enumerate(current_queue, start=1):
            print(f"[{i}] {str(item)}")

        print()
        choice = input("Pilih nomor antrean untuk diproses (0 untuk kembali): ")
        Utils.clear()
        if choice == "0":
            return

        try:
            index = int(choice) - 1
            item = health_check_list[index]
        except (ValueError, IndexError):
            print("Pilihan tidak valid.")
            Utils.enter_and_continue()
            return

        while True:
            pet_type = input(f"Masukkan jenis hewan: ")

            if pet_type == "":
                print("Jenis hewan tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            break

        while True:
            disease = input("Masukkan penyakit: ")

            if disease == "":
                print("Penyakit tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            break

        while True:
            medicine = input("Masukkan obat yang dibutuhkan: ")

            if medicine == "":
                print("Obat tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            break

        while True:
            price = input("Masukkan harga: ")

            if price == "":
                print("Harga tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            if not price.isdigit():
                print("Harga harus berupa angka.")
                Utils.enter_and_continue()
                continue

            price = int(price)

            break

        item.pet_type = pet_type
        item.disease = disease
        item.medicine = medicine
        item.price = price
        item.status = "Done"

        HealthCheck.save_to_file()

        print("Pengecekan kesehatan selesai.")
        Utils.enter_and_continue()

    @staticmethod
    def process_pet_care_queue():
        current_queue = [item for item in pet_care_queue if item.status == "Waiting"]
        if not current_queue:
            print("Antrean perawatan kosong.")
            Utils.enter_and_continue()
            return

        print("Antrean Perawatan Hewan:")
        for i, item in enumerate(current_queue, start=1):
            print(f"[{i}] {str(item)}")

        choice = input("Pilih nomor antrean untuk diproses (0 untuk kembali): ")
        if choice == "0":
            return

        try:
            index = int(choice) - 1
            item = pet_care_queue[index]
        except (ValueError, IndexError):
            print("Pilihan tidak valid.")
            Utils.enter_and_continue()
            return

        item.status = "Done"
        print(f"Perawatan {item.package} untuk {item.pet_type} selesai.")

        PetCare.save_to_file()
        Utils.enter_and_continue()


user_list: List[User] = []
