from utils import Utils


# Antrean layanan yang menunggu.
class ServiceQueue:
    def __init__(self, user, service_type, pet_type=None, package=None, price=0):
        self.user = user
        self.service_type = service_type
        self.pet_type = pet_type
        self.package = package
        self.status = "Waiting"
        self.result = None
        self.price = price


queue = []


class Service:
    @staticmethod
    def check_health(current_user):
        item = ServiceQueue(current_user, "Check Health")
        queue.append(item)
        print("Anda telah ditambahkan ke antrean untuk pengecekan kesehatan.")
        print(f"Nomor antrean: {len(queue) + 1}")
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

                item = ServiceQueue(current_user, "Pet Care", pet_type, package, price)
                queue.append(item)
                print(
                    f"Anda telah ditambahkan ke antrean untuk {package} perawatan {pet_type} dengan harga {Utils.format_rupiah(price)}."
                )
                Utils.enter_and_continue()
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()

    @staticmethod
    def view_service_status(current_user):
        user_queue_items = [item for item in queue if item.user == current_user]

        if not user_queue_items:
            print("Anda tidak memiliki layanan yang sedang diproses.")
            Utils.enter_and_continue()
            return

        print("Status Layanan Anda:")
        for item in user_queue_items:
            print(str(item))

        Utils.enter_and_continue()

    @staticmethod
    def menu(current_user):
        while True:
            Utils.clear()
            print("Menu Layanan")
            print("[0] Kembali")
            print("[1] Kesehatan")
            print("[2] Perawatan")
            print("[3] Lihat Status Layanan Anda")

            choice = input("Pilihan: ")

            if choice == "0":
                break
            elif choice == "1":
                Service.check_health(current_user)
            elif choice == "2":
                Service.pet_care(current_user)
            elif choice == "3":
                Service.view_service_status(current_user)
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()
