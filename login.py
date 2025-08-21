import time
from random import choice
from colorama import Fore
from tabulate import tabulate
from animations import slow_print, glitch_line
from user_manager import UserManager
import base64
from journal import Journal
import sys
import random

class Login:
    def __init__(self):
        self.user_manager = UserManager()
        self.last_activity_time = time.time()  # Czas ostatniej aktywnosci

    def login_menu(self):
        username = input(Fore.YELLOW + "Username: ").strip()

        if self.user_manager.is_user_locked(username):
            slow_print(Fore.RED + "Account is locked. Try again later.")
            glitch_line("LOCKED: Unauthorized access detected.")
            return

        if username not in self.user_manager.users:
            slow_print(Fore.RED + "User not found!")
            glitch_line("ERROR: User does not exist in the database.")
            return

        attempts = 0
        while attempts < 3:
            password = input(Fore.YELLOW + "Password: ").strip()
            if self.user_manager.check_credentials(username, password):
                slow_print(Fore.GREEN + "Login successful!")
                glitch_line("SYSTEM ACCESS GRANTED.")
                self.show_user_menu(username)
                return
            else:
                slow_print(Fore.RED + "Incorrect password.")
                glitch_line("ERROR: Invalid password.")
                attempts += 1

        slow_print(Fore.RED + "Too many failed attempts. Locking account for 1 minute.")
        self.user_manager.lock_user(username)
        glitch_line("Account temporarily locked.")

    def show_user_menu(self, username):
        user_level = self.user_manager.users[username]['access_level']
        slow_print(Fore.GREEN + f"Welcome {username}, Access Level: {user_level}")

        # Opcje dostepne dla róznych poziomów dostepu
        options = {
            "ascii": "Zobacz ASCII art",
            "logs": "Otwórz Logi",
            "encrypt": "Zaszyfruj Wiadomosć",
            "decrypt": "Odszyfruj Wiadomosć",
            "edit_notes": "Edytuj Notatki",
            "help": "Display this help information",
            "exit": "Exit the menu",
            "db": "Baza Danych"
        }

        # Ograniczenia dostepu w zaleznosci od poziomu uzytkownika
        if user_level == 2:
            allowed_options = {"ascii", "logs", "exit"}
        elif user_level == 8:  # Admin
            allowed_options = set(options.keys())
        else:
            allowed_options = {"help", "exit"}  # Domyslne opcje dla innych poziomów

        while True:
            self.check_inactivity()  # Check if user has been inactive for 5 minutes

            # Wyswietl dostepne opcje
            slow_print(Fore.YELLOW + "Type 'help' to see available options.")
            # for option, description in options.items():
            #     if option in allowed_options:
            #         slow_print(Fore.CYAN + f"- {option}: {description}")

            choice = input(Fore.YELLOW + "Choose an option (or type 'exit' to logout): ").strip().lower()
            self.handle_option(choice, username)

    def xor_encrypt(self, message):
        key = 'secret_key'  # Mozesz zmienić klucz na dowolny ciag znaków
        encrypted_message = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(message))
        return encrypted_message

    def encrypt_message(self, username):
        message = input(Fore.YELLOW + "Enter the message to encrypt: ").strip()
        encrypted_message = self.xor_encrypt(message)
        encoded_message = base64.b64encode(encrypted_message.encode()).decode()  # Kodowanie Base64
        slow_print(Fore.GREEN + f"Encrypted Message: {encoded_message}")
        self.user_manager.log_operation(username, "Encryption", len(message))

    def decrypt_message(self, username):
        encoded_message = input(Fore.YELLOW + "Enter the encrypted message: ").strip()
        try:
            encrypted_message = base64.b64decode(encoded_message.encode()).decode()  # Dekodowanie Base64
            decrypted_message = self.xor_encrypt(encrypted_message)  # Uzyj tej samej metody do deszyfrowania
            slow_print(Fore.GREEN + f"Decrypted Message: {decrypted_message}")
            self.user_manager.log_operation(username, "Decryption", len(encoded_message))
        except Exception as e:
            slow_print(Fore.RED + f"ERROR: Decryption failed - {str(e)}")

    def edit_notes(self, username):
        slow_print(Fore.GREEN + f"Editing notes for {username}.")
        glitch_line("Notes opened for modification.")

    def access_logs(self, username):
        slow_print(Fore.GREEN + "Accessing logs...")
        glitch_line("Logs accessed.")

        # Lista losowych komunikatów do wyswietlenia
        random_logs = [
            "User authentication successful.",
            "System diagnostics completed.",
            "Unauthorized access attempt detected.",
            "File 'config.sys' modified.",
            "Backup completed successfully.",
            "Error: Connection to server lost.",
            "Log entry: User 'admin' logged in.",
            "Warning: Disk space running low.",
            "Process 'daemon.exe' terminated.",
            "New user 'guest' created.",
            "Firewall rules updated.",
            "Critical error: Memory overflow detected."
        ]

        # Wyswietl losowe komunikaty przez kilka sekund
        start_time = time.time()
        while time.time() - start_time < 5:  # Wyswietlaj przez 5 sekund
            log = random.choice(random_logs)
            slow_print(Fore.YELLOW + log)
            time.sleep(0.5)  # Odstep miedzy komunikatami

        # Odczyt logów z pliku crypto_logs.json
        try:
            file_path = "data/crypto_logs.json"
            with open(file_path, "r", encoding="utf-8") as file:
                logs = file.readlines()  # Wczytaj logi jako liste wierszy

            slow_print(Fore.CYAN + "\nCrypto Logs:")
            for log in logs[-10:]:  # Wyswietl ostatnie 10 logów
                slow_print(Fore.WHITE + log.strip())

        except FileNotFoundError:
            slow_print(Fore.RED + f"Error: The file '{file_path}' was not found.")
        except Exception as e:
            slow_print(Fore.RED + f"An unexpected error occurred: {e}")

    def handle_option(self, option, username):
        user_level = self.user_manager.users[username]['access_level']

        # Opcje dostepne dla wszystkich poziomów dostepu
        options = {
            "ascii": (self.show_ascii_art, 2),
            "logs": (self.access_logs, 2),
            "encrypt": (self.encrypt_message, 5),
            "decrypt": (self.decrypt_message, 5),
            "edit_notes": (self.edit_notes, 8),
            "help": (self.show_help, 1),
            "exit": (self.handle_exit, 1),
            "db": (self.journal_menu, 5)
        }

        if option in options:
            action, required_level = options[option]
            if user_level >= required_level:
                action(username)
            else:
                slow_print(Fore.RED + "You do not have permission to access this option.")
        else:
            slow_print(Fore.RED + "Invalid option. Please try again.")

    def show_help(self, username=None):
        user_level = self.user_manager.users[username]['access_level']

        # Opcje dostepne dla wszystkich poziomów dostepu
        options = {
            "ascii": ("Zobacz ASCII art", 2),
            "logs": ("Otwórz Logi", 2),
            "encrypt": ("Zaszyfruj Wiadomosć", 5),
            "decrypt": ("Odszyfruj Wiadomosć", 5),
            "edit_notes": ("Edytuj Notatki", 8),
            "db": ("Baza Danych", 5),
            "help": ("Display this help information", 1),
            "exit": ("Exit the menu", 1),
        }

        # Filtrowanie opcji na podstawie poziomu dostepu
        help_text = """
        +-------------------------------------------------------------+
        |                       Available Commands                    |
        +-------------------------------------------------------------+
"""
        for option, (description, required_level) in options.items():
            if user_level >= required_level:
                help_text += f"        | {option:<12}: {description:<45} |\n"

        help_text += "        +-------------------------------------------------------------+"
        slow_print(help_text)

    def show_ascii_art(self, username=None):
        try:
            # sciezka do pliku z grafikami
            file_path = "data/baby_art.txt"

            # Wczytaj zawartosć pliku i podziel na grafiki
            with open(file_path, "r", encoding="utf-8") as file:
                art_sections = file.read().split("--splitter--")

            # Wyswietl losowe grafiki
            while True:
                random_art = random.choice(art_sections)  # Wybierz losowa grafike
                slow_print(Fore.GREEN + random_art.strip())  # Wyswietl grafike
                user_input = input(Fore.YELLOW + "Press Enter to see another art or type 'exit' to return: ").strip().lower()
                if user_input == "exit":
                    break

        except FileNotFoundError:
            slow_print(Fore.RED + "Error: The file 'baby_art.txt' was not found.")
        except Exception as e:
            slow_print(Fore.RED + f"An unexpected error occurred: {e}")

    def journal_menu(self, username):
        # Access the journal menu.
        journal = Journal()
        journal.journal_menu(username)

    def check_inactivity(self):
        """Sprawdza, czy uzytkownik byl nieaktywny przez 5 minut."""
        current_time = time.time()
        inactivity_limit = 9999999999999999 # 5 minut w sekundach

        if current_time - self.last_activity_time > inactivity_limit:
            slow_print(Fore.RED + "Session timed out due to inactivity.")
            glitch_line("SYSTEM SHUTDOWN: User inactive for too long.")
            sys.exit(0)  # Zakończ program

    def handle_exit(self):
        slow_print(Fore.YELLOW + "Exiting...")
        self.last_activity_time = time.time()  # Resetuj licznik aktywnosci
        self.boot_sequence()

    def boot_sequence(self):
        # This method can represent the boot sequence or any intro animation
        slow_print(Fore.GREEN + "Booting up...")
        time.sleep(1)
        slow_print(Fore.YELLOW + "Loading system...")
        time.sleep(1)
        glitch_line("SYSTEM READY.")
