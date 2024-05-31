from utils import Utils
from datetime import datetime
import shutil
import os
import tkinter as tk
from tkinter import filedialog

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

            if age == "0":
                print("Usia tidak boleh 0.")
                Utils.enter_and_continue()
                continue

            if not age.isdigit():
                print("Usia harus berupa angka.")
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

            if price == "0":
                print("Harga tidak boleh 0.")
                Utils.enter_and_continue()
                continue

            if not price.isdigit():
                print("Harga harus berupa angka.")
                Utils.enter_and_continue()
                continue

            break

        description = input("Deskripsi: ")

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
    def adoption_menu(current_user):
        if len(pets) == 0:
            print("Belum ada hewan peliharaan.")
            Utils.enter_and_continue()
            return

        for index, pet in enumerate(pets):
            print(f"[{index + 1}] {pet.name}")

        choice = input("Pilih hewan peliharaan: ")

        if not choice.isdigit():
            print("Pilihan harus berupa angka.")
            Utils.enter_and_continue()
            return

        choice = int(choice)

        if choice < 1 or choice > len(pets):
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

            if choice == "0":
                return
            elif choice == "1":
                pets.remove(pet)
                Pet.save_to_file()

                print("Hewan peliharaan berhasil diadopsi.")
                Utils.enter_and_continue()
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()
                continue

            break

    @staticmethod
    def save_to_file():
        with open("data/pets.tsv", "w") as file:
            file.write("nama\tusia\tspesies\tgambar\tharga\tdeskripsi\n")
            for pet in pets:
                file.write(
                    f"{pet.name}\t{pet.age}\t{pet.species}\t{pet.image}\t{pet.description}\n"
                )

    @staticmethod
    def load_from_file():
        if not os.path.exists("data/pets.tsv"):
            return

        with open("data/pets.tsv") as file:
            for line in file.readlines()[1:]:
                name, age, species, image, price, description = line.strip().split("\t")
                pet = Pet(name, age, species, image, price, description)
                pets.append(pet)
