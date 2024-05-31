from utils import Utils
from product import product_list


class Shop:
    categories = ["Hewan", "Makanan", "Mainan", "Aksesoris", "Lainnya"]

    @staticmethod
    def print_categories():
        print("[0] Kembali")
        for i, category in enumerate(Shop.categories):
            print(f"[{i + 1}] {category}")

        return Shop.categories

    @staticmethod
    def list_product_by_category(category):
        Utils.clear()
        print("[0] Kembali")

        # Print produk sesuai kategori.
        result = [product for product in product_list if product.category == category]

        for i, product in enumerate(result):
            print(
                f"[{i + 1}] {product.name} - {product.get_price_formatted()} - Stok: {product.get_stock()}"
            )

        return result

    @staticmethod
    def catalogue(current_user):
        while True:
            try:
                Utils.clear()
                current_user.get_shopping_cart_items()
                categories = Shop.print_categories()
                choice = input("Pilihan: ")

                if choice == "0":
                    break

                category = categories[int(choice) - 1]
            except (ValueError, IndexError):
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()
                continue

            while True:
                Utils.clear()
                products = Shop.list_product_by_category(category)

                choice = input("Pilihan: ")

                if choice == "0":
                    break

                Utils.clear()
                try:
                    product = products[int(choice) - 1]
                    while True:
                        print("Produk yang dipilih: ")
                        print(f"Nama: {product.name}")
                        print(f"Harga: {product.get_price_formatted()}")
                        print(f"Stok: {product.get_stock()}")
                        print()

                        amount = input("Jumlah: ")

                        if not amount.isdigit():
                            print("Jumlah harus angka.")
                            Utils.enter_and_continue()
                            continue

                        if product.get_stock() < int(amount):
                            print("Stok tidak cukup.")
                            Utils.enter_and_continue()
                            continue

                        if int(amount) <= 0:
                            print("Jumlah harus lebih dari 0.")
                            Utils.enter_and_continue()
                            continue

                        amount = int(amount)
                        break

                    current_user.add_to_shopping_cart(product, amount)

                    Utils.enter_and_continue()

                except (ValueError, IndexError):
                    print("Pilihan tidak valid.")
                    Utils.enter_and_continue()
                    continue

    @staticmethod
    def menu(current_user):
        while True:
            Utils.clear()
            print("Menu Toko")
            print("[0] Kembali")
            print("[1] Lihat Keranjang Belanja")
            print("[2] Hapus Item dari Keranjang Belanja")
            print("[3] Katalog Toko")
            if current_user.get_shopping_cart_total() > 0:
                print("[4] Checkout")

            choice = input("Pilihan: ")
            Utils.clear()

            if choice == "0":
                break
            elif choice == "1":
                current_user.get_shopping_cart_items(interactive=True)
            elif choice == "2":
                current_user.remove_from_shopping_cart()
            elif choice == "3":
                Shop.catalogue(current_user)
            elif choice == "4":
                # Validasi belanjaan harus lebih dari 0.
                if current_user.get_shopping_cart_total() == 0:
                    print("Keranjang belanja kosong.")
                    Utils.enter_and_continue()
                    continue

                current_user.checkout()
                print("Terima kasih telah berbelanja!")
                Utils.enter_and_continue()
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()
