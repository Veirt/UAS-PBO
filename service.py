import os
from payment import Payment
from utils import Utils
from receipt import Receipt


class HealthCheck:
    def __init__(self, user):
        self.user = user
        # Status: bisa Waiting, Done, Paid
        # Waiting: sedang menunggu dokter memproses
        # Done: sudah selesai diproses dokter
        # Paid: sudah dibayar oleh user
        self.status = "Waiting"
        self.pet_type = None
        self.disease = None
        self.medicine = None
        self.price = 0

    def __str__(self):
        result = f"Pemilik: {self.user.username} / {self.user.name}"

        if self.pet_type:
            result += f", Jenis Hewan: {self.pet_type}"
        if self.disease:
            result += f", Penyakit: {self.disease}"
        if self.medicine:
            result += f", Obat: {self.medicine}"
        if self.price:
            result += f", Harga: {Utils.format_rupiah(self.price)}"

        result += f", Status: {self.status}"

        return result

    @staticmethod
    def get_queue_num(health_check):
        waiting_list = [item for item in health_check_list if item.status == "Waiting"]
        return waiting_list.index(health_check) + 1

    @staticmethod
    def save_to_file():
        with open("data/health_check.tsv", "w") as file:
            file.write("Pemilik\tJenis Hewan\tPenyakit\tObat\tHarga\tStatus\n")
            for item in health_check_list:
                file.write(
                    f"{item.user.username}\t{item.pet_type}\t{item.disease}\t{item.medicine}\t{item.price}\t{item.status}\n"
                )

    @staticmethod
    def load_from_file():
        if not os.path.exists("data/health_check.tsv"):
            return

        with open("data/health_check.tsv", "r") as file:
            from user import user_list

            for line in file.readlines()[1:]:
                data = line.strip().split("\t")
                item = HealthCheck(None)
                item.user = Utils.find_user(user_list, data[0])
                item.pet_type = data[1] if data[1] != "None" else None
                item.disease = data[2] if data[2] != "None" else None
                item.medicine = data[3] if data[3] != "None" else None
                item.price = int(data[4])
                item.status = data[5]
                health_check_list.append(item)


health_check_list = []


# Antrean layanan perawatan hewan.
class PetCare:
    def __init__(self, user, pet_type, package, price):
        self.user = user
        self.pet_type = pet_type
        self.package = package
        self.status = "Waiting"
        self.price = price

    def __str__(self):
        return f"Pemilik: {self.user.username} / {self.user.name}, Jenis Hewan: {self.pet_type}, Paket: {self.package}, Status: {self.status}, Harga: {Utils.format_rupiah(self.price)}"

    @staticmethod
    def get_queue_num(pet_care):
        waiting_list = [item for item in pet_care_queue if item.status == "Waiting"]
        return waiting_list.index(pet_care) + 1

    @staticmethod
    def save_to_file():
        with open("data/pet_care.tsv", "w") as file:
            file.write("Pemilik\tJenis Hewan\tPaket\tHarga\tStatus\n")
            for item in pet_care_queue:
                file.write(
                    f"{item.user.username}\t{item.pet_type}\t{item.package}\t{item.price}\t{item.status}\n"
                )

    @staticmethod
    def load_from_file():
        if not os.path.exists("data/pet_care.tsv"):
            return

        with open("data/pet_care.tsv", "r") as file:
            from user import user_list

            for line in file.readlines()[1:]:
                data = line.strip().split("\t")
                item = PetCare(None, None, None, 0)
                item.user = Utils.find_user(user_list, data[0])
                item.pet_type = data[1]
                item.package = data[2]
                item.price = int(data[3])
                item.status = data[4]
                pet_care_queue.append(item)


pet_care_queue = []


class Service:
    @staticmethod
    def check_pet_health(current_user):
        item = HealthCheck(current_user)
        print("Anda telah ditambahkan ke antrean untuk pengecekan kesehatan.")
        print(f"Nomor antrean: {len(health_check_list) + 1}")
        health_check_list.append(item)

        HealthCheck.save_to_file()
        Utils.enter_and_continue()

    @staticmethod
    def pet_care(current_user):
        while True:
            Utils.clear()
            print("Menu Perawatan")
            print("[0] Kembali")
            print("[1] Anjing")
            print("[2] Kucing")

            choice = input("Pilihan: ")

            if choice == "0":
                break
            elif choice == "1":
                Service.care_package(
                    current_user,
                    "Anjing",
                )
            elif choice == "2":
                Service.care_package(current_user, "Kucing")
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()
                continue

            break

    @staticmethod
    def care_package(current_user, pet_type):
        price_dict = {
            "Anjing": {
                "Paket A (Lengkap)": 500000,
                "Paket B (Treatment)": 300000,
                "Paket C (Mandi)": 150000,
            },
            "Kucing": {
                "Paket A (Lengkap)": 400000,
                "Paket B (Treatment)": 250000,
                "Paket C (Mandi)": 100000,
            },
        }

        while True:
            Utils.clear()
            print(f"Paket Perawatan untuk {pet_type}")
            print("[0] Kembali")

            # Daftar harga berdasarkan jenis hewan
            for package, price in price_dict[pet_type].items():
                print(
                    f"[{list(price_dict[pet_type].keys()).index(package) + 1}] {package} - {Utils.format_rupiah(price)}"
                )

            choice = input("Pilihan: ")

            if choice == "0":
                break
            elif choice in [str(i) for i in range(1, len(price_dict[pet_type]) + 1)]:
                package = list(price_dict[pet_type].keys())[int(choice) - 1]
                price = price_dict[pet_type][package]

                item = PetCare(current_user, pet_type, package, price)
                pet_care_queue.append(item)
                print(
                    f"Anda telah ditambahkan ke antrean untuk {package} perawatan {pet_type} dengan harga {Utils.format_rupiah(price)}."
                )
                PetCare.save_to_file()

                Payment.select_method()
                receipt = Receipt()
                receipt.create_pet_care_receipt(item)
                break
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()

    @staticmethod
    def view_health_check_status(current_user):
        Utils.clear()
        print("Antrean Pengecekan Kesehatan Hewan:")
        user_pet_health_check_items = [
            item
            for item in health_check_list
            if item.user == current_user and item.status == "Waiting"
        ]
        if not user_pet_health_check_items:
            print("Tidak ada pengecekan kesehatan hewan yang aktif.")
        else:
            for item in user_pet_health_check_items:
                num = HealthCheck.get_queue_num(item)
                print(f"- No. Antrean {num}: {item.status}")

        print()
        Utils.enter_and_continue()

    @staticmethod
    def view_pet_care_status(current_user):
        Utils.clear()
        print("Antrean Perawatan Hewan:")
        user_pet_care_items = [
            item
            for item in pet_care_queue
            if item.user == current_user and item.status == "Waiting"
        ]
        if not user_pet_care_items:
            print("Tidak ada layanan perawatan hewan yang aktif.")
        else:
            for item in user_pet_care_items:
                num = PetCare.get_queue_num(item)
                print(f"- No. Antrean {num}: {str(item)}")

        print()
        Utils.enter_and_continue()

    @staticmethod
    def view_health_check_history(current_user):
        Utils.clear()
        completed_items = [
            item
            for item in health_check_list
            if item.user == current_user and item.status == "Done"
        ]

        if not completed_items:
            print("Tidak ada pengecekan kesehatan hewan yang telah selesai.")
            Utils.enter_and_continue()
            return

        for i, item in enumerate(completed_items, start=1):
            print(f"[{i}] {str(item)}")

        choice = input("Pilih nomor untuk melakukan pembayaran (0 untuk kembali): ")
        Utils.clear()
        if choice == "0":
            return

        try:
            index = int(choice) - 1
            selected_item = completed_items[index]
        except (ValueError, IndexError):
            print("Pilihan tidak valid.")
            Utils.enter_and_continue()
            return

        print(f"Pembayaran untuk {str(selected_item)}")
        Payment.select_method()
        selected_item.status = "Paid"

        receipt = Receipt()
        receipt.create_health_check_receipt(selected_item)

        HealthCheck.save_to_file()
        print("Pembayaran berhasil.")
        Utils.enter_and_continue()

    @staticmethod
    def health_check_menu(current_user):
        while True:
            Utils.clear()
            print("Menu Pengecekan Kesehatan Hewan")
            print("[0] Kembali")
            print("[1] Tambah Antrean Pengecekan Kesehatan")
            print("[2] Lihat Status Antrean Pengecekan Kesehatan")
            print("[3] Pembayaran Pengecekan Kesehatan")

            choice = input("Pilihan: ")
            Utils.clear()

            if choice == "0":
                break
            elif choice == "1":
                Service.check_pet_health(current_user)
            elif choice == "2":
                Service.view_health_check_status(current_user)
            elif choice == "3":
                Service.view_health_check_history(current_user)
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()

    @staticmethod
    def pet_care_menu(current_user):
        while True:
            Utils.clear()
            print("Menu Perawatan Hewan")
            print("[0] Kembali")
            print("[1] Perawatan Hewan")
            print("[2] Lihat Status Antrean Perawatan")

            choice = input("Pilihan: ")
            Utils.clear()

            if choice == "0":
                break
            elif choice == "1":
                Service.pet_care(current_user)
            elif choice == "2":
                Service.view_pet_care_status(current_user)
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()

    @staticmethod
    def menu(current_user):
        while True:
            Utils.clear()
            print("Menu Layanan")
            print("[0] Kembali")
            print("[1] Pengecekan Kesehatan Hewan")
            print("[2] Perawatan Hewan")

            choice = input("Pilihan: ")
            Utils.clear()

            if choice == "0":
                break
            elif choice == "1":
                Service.health_check_menu(current_user)
            elif choice == "2":
                Service.pet_care_menu(current_user)
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()
