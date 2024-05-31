from typing import List
from utils import Utils


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
            Utils.enter_and_continue()
            return False

        self._stock -= amount

    def increase_stock(self, amount):
        self._stock += amount

    def set_stock(self, amount):
        if amount < 0:
            print("Stok tidak boleh negatif.")
            Utils.enter_and_continue()
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
                Utils.enter_and_continue()
                continue

            # Validasi nama produk harus unik.
            if any(product.name == name for product in product_list):
                print("Nama produk sudah ada.")
                Utils.enter_and_continue()
                continue

            break

        while True:
            price = input("Harga produk: ")
            # Validasi harga produk harus angka valid.
            if not price.isdigit():
                print("Harga produk harus angka yang valid.")
                Utils.enter_and_continue()
                continue

            price = int(price)

            break

        while True:
            stock = input("Stok produk: ")
            # Validasi stok produk harus angka.
            if not stock.isdigit():
                print("Stok produk harus angka yang valid.")
                Utils.enter_and_continue()
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
                Utils.enter_and_continue()
                continue

            if category not in category_dict.keys():
                print("Kategori produk tidak valid.")
                Utils.enter_and_continue()
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
        Utils.enter_and_continue()

    @staticmethod
    def list_product():
        print("Daftar Produk: ")
        for i, product in enumerate(product_list):
            print(
                f"{i + 1}. {product.name} - {product.get_price_formatted()} - {product.get_stock()} - {product.category}"
            )

        Utils.enter_and_continue()

    # Simpan produk dari tsv.
    @staticmethod
    def save_to_file():
        with open("data/products.tsv", "w") as file:
            file.write("nama\tharga\tstok\tkategori\n")
            for product in product_list:
                file.write(
                    f"{product.name}\t{product.price}\t{product.get_stock()}\t{product.category}\n"
                )

    # Ambil produk dari tsv.
    @staticmethod
    def load_from_file():
        with open("data/products.tsv", "r") as file:
            lines = file.readlines()
            for line in lines[1:]:
                name, price, stock, category = line.strip().split("\t")
                product_list.append(
                    Product(name, int(price), int(stock), category.title())
                )


product_list: List[Product] = []
