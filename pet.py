from utils import Utils
from datetime import datetime
import shutil
import os
import tkinter as tk
from tkinter import filedialog
from payment import Payment

root = tk.Tk()
root.withdraw()


pets = []


class Pet:
    def __init__(self, name, age, species, image, price, description):
        self.name = name
        self.age = age
        self.species = species
        self.image = image
        self.price = price
        self.description = description

    @staticmethod
    def input_pet():
        while True:
            name = input("Nama: ")

            if name == "":
                print("Nama tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            break

        while True:
            age = input("Usia: ")

            if age == "":
                print("Usia tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            if not age.isdigit():
                print("Usia harus berupa angka.")
                Utils.enter_and_continue()
                continue

            age = int(age)

            if age == 0:
                print("Usia tidak boleh 0.")
                Utils.enter_and_continue()
                continue

            break

        while True:
            species = input("Spesies: ")

            if species == "":
                print("Spesies tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            break

        while True:
            print("Pilih gambar hewan peliharaan.")
            file_path = filedialog.askopenfilename(
                title="Pilih gambar hewan peliharaan",
                filetypes=[("Image files", "*.jpg *.jpeg *.png")],
            )

            if file_path == "":
                print("Gambar tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            break

        while True:
            price = input("Harga: ")

            if price == "":
                print("Harga tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            if not price.isdigit():
                print("Harga harus berupa angka.")
                Utils.enter_and_continue()
                continue

            price = int(price)

            if price == 0:
                print("Harga tidak boleh 0.")
                Utils.enter_and_continue()
                continue

            break

        while True:
            description = input("Deskripsi: ")

            if description == "":
                print("Deskripsi tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            break

        # Pindahin file nya.
        _, file_ext = os.path.splitext(os.path.basename(file_path))
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        image = f"{name}_{timestamp}{file_ext}"
        destination_path = os.path.join("images", image)
        shutil.copy2(file_path, destination_path)

        pet = Pet(name, age, species, image, price, description)

        return pet

    @staticmethod
    def create_pet():
        pet = Pet.input_pet()
        pets.append(pet)

        print("Hewan peliharaan berhasil ditambahkan.")

        Pet.save_to_file()
        Utils.enter_and_continue()

    @staticmethod
    def read_all():
        if len(pets) == 0:
            print("Tidak ada hewan peliharaan yang tersedia.")
            Utils.enter_and_continue()
            return

        for index, pet in enumerate(pets):
            print(f"[{index + 1}] {pet.name}")

        Utils.enter_and_continue()

    @staticmethod
    def adoption_menu():
        if len(pets) == 0:
            print("Belum ada hewan peliharaan.")
            Utils.enter_and_continue()
            return

        while True:
            print("[0] Kembali")
            for index, pet in enumerate(pets):
                print(f"[{index + 1}] {pet.name}")

            choice = input("Pilihan: ")
            Utils.clear()

            if not choice.isdigit():
                print("Pilihan harus berupa angka.")
                Utils.enter_and_continue()
                return

            if choice == "0":
                break

            choice = int(choice)

            if choice > len(pets):
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()
                return

            pet = pets[choice - 1]

            while True:
                print(f"Nama: {pet.name}")
                print(f"Usia: {pet.age}")
                print(f"Spesies: {pet.species}")
                print(f"Deskripsi: {pet.description}")
                print(f"Harga: {Utils.format_rupiah(pet.price)}")

                image_path = os.path.join("images", pet.image)
                Utils.show_image(image_path)

                print("[0] Kembali")
                print("[1] Adopsi")

                choice = input("Pilih menu: ")
                Utils.clear()

                if choice == "0":
                    break
                elif choice == "1":
                    Payment.select_method()

                    os.remove(image_path)
                    pets.remove(pet)

                    Pet.save_to_file()

                    print("Hewan peliharaan berhasil diadopsi.")
                    Utils.enter_and_continue()
                    return
                else:
                    print("Pilihan tidak valid.")
                    Utils.enter_and_continue()
                    continue

    @staticmethod
    def update_pet():
        if not pets:
            print("Tidak ada hewan peliharaan yang terdaftar.")
            Utils.enter_and_continue()
            return

        print("Daftar Hewan Peliharaan:")
        for i, pet in enumerate(pets):
            print(f"[{i + 1}] {pet.name} - {pet.species} - {pet.age} tahun")

        choice = input(
            "Pilih nomor hewan peliharaan yang ingin diubah (0 untuk kembali): "
        )

        if choice == "0":
            return

        try:
            index = int(choice) - 1
            pet = pets[index]
        except (ValueError, IndexError):
            print("Pilihan tidak valid.")
            Utils.enter_and_continue()
            return

        new_pet = Pet.input_pet()
        pets[index] = new_pet

        print("Hewan peliharaan berhasil diubah.")
        Utils.enter_and_continue()

        Pet.save_to_file()

    @staticmethod
    def delete_pet():
        if not pets:
            print("Tidak ada hewan peliharaan yang terdaftar.")
            Utils.enter_and_continue()
            return

        print("Daftar Hewan Peliharaan:")
        for i, pet in enumerate(pets):
            print(f"[{i + 1}] {pet.name} - {pet.species} - {pet.age} tahun")

        choice = input(
            "Pilih nomor hewan peliharaan yang ingin dihapus (0 untuk kembali): "
        )

        if choice == "0":
            return

        try:
            index = int(choice) - 1
            pet = pets.pop(index)
            os.remove(os.path.join("images", pet.image))

            print(f"Hewan peliharaan {pet.name} berhasil dihapus.")
        except (ValueError, IndexError):
            print("Pilihan tidak valid.")
            Utils.enter_and_continue()
            return

        Pet.save_to_file()
        Utils.enter_and_continue()

    @staticmethod
    def save_to_file():
        with open("data/pets.tsv", "w") as file:
            file.write("nama\tusia\tspesies\tgambar\tharga\tdeskripsi\n")
            for pet in pets:
                file.write(
                    f"{pet.name}\t{pet.age}\t{pet.species}\t{pet.image}\t{pet.price}\t{pet.description}\n"
                )

    @staticmethod
    def load_from_file():
        if not os.path.exists("data/pets.tsv"):
            return

        with open("data/pets.tsv") as file:
            for line in file.readlines()[1:]:
                name, age, species, image, price, description = line.strip().split("\t")
                pet = Pet(name, age, species, image, int(price), description)
                pets.append(pet)
