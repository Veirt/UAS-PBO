import os


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
    def enter_and_continue():
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
