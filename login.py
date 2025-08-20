import time
from random import choice
from colorama import Fore
from tabulate import tabulate
from animations import slow_print, glitch_line
from user_manager import UserManager
import base64
from journal import Journal

class Login:
    def __init__(self):
        self.user_manager = UserManager()
        self.last_activity_time = time.time()  # Czas ostatniej aktywności

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

        # Opcje dostępne dla różnych poziomów dostępu
        options = {
            "ascii": "Zobacz ASCII art",
            "logs": "Otwórz Logi",
            "encrypt": "Zaszyfruj Wiadomość",
            "decrypt": "Odszyfruj Wiadomość",
            "edit_notes": "Edytuj Notatki",
            "help": "Display this help information",
            "exit": "Exit the menu",
            "db": "Baza Danych"
        }

        # Ograniczenia dostępu w zależności od poziomu użytkownika
        if user_level == 2:
            allowed_options = {"ascii", "logs", "exit"}
        elif user_level == 8:  # Admin
            allowed_options = set(options.keys())
        else:
            allowed_options = {"help", "exit"}  # Domyślne opcje dla innych poziomów

        while True:
            self.check_inactivity()  # Check if user has been inactive for 5 minutes

            # Wyświetl dostępne opcje
            slow_print(Fore.YELLOW + "Available options:")
            for option, description in options.items():
                if option in allowed_options:
                    slow_print(Fore.CYAN + f"- {option}: {description}")

            choice = input(Fore.YELLOW + "Choose an option (or type 'exit' to logout): ").strip().lower()
            self.handle_option(choice, username)

    def xor_encrypt(self, message):
        key = 'secret_key'  # Możesz zmienić klucz na dowolny ciąg znaków
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
            decrypted_message = self.xor_encrypt(encrypted_message)  # Użyj tej samej metody do deszyfrowania
            slow_print(Fore.GREEN + f"Decrypted Message: {decrypted_message}")
            self.user_manager.log_operation(username, "Decryption", len(encoded_message))
        except Exception as e:
            slow_print(Fore.RED + f"ERROR: Decryption failed - {str(e)}")

    def edit_notes(self, username):
        slow_print(Fore.GREEN + f"Editing notes for {username}.")
        glitch_line("Notes opened for modification.")

    def access_logs(self, username):
        slow_print(Fore.GREEN + "Accessing logs.")
        glitch_line("Logs accessed.")


    def handle_option(self, option, username):
        user_level = self.user_manager.users[username]['access_level']

        # Opcje dostępne dla różnych poziomów dostępu
        options = {
            "ascii": self.show_ascii_art,
            "logs": self.access_logs,
            "encrypt": self.encrypt_message,
            "decrypt": self.decrypt_message,
            "edit_notes": self.edit_notes,
            "help": self.show_help,
            "exit": self.handle_exit,
            "db": self.journal_menu
        }

        # Ograniczenia dostępu w zależności od poziomu użytkownika
        if user_level == 2:
            allowed_options = {"ascii", "logs"}
        elif user_level == 8:  # Admin
            allowed_options = set(options.keys())
        else:
            allowed_options = {"help", "exit"}  # Domyślne opcje dla innych poziomów

        if option in allowed_options:
            options[option](username)
        else:
            slow_print(Fore.RED + "You do not have permission to access this option.")

    def show_help(self, username=None):
        help_text = """
        +-------------------------------------------------------------+
        |                       Available Commands                    |
        +-------------------------------------------------------------+
        | ascii          : Zobacz ASCII art                           |
        | logs           : Otwórz Logi                                |
        | db             : Baza Danych                                |
        | encrypt        : Zaszyfruj Wiadomość                        |
        | decrypt        : Odszyfruj Wiadomość                        |
        | edit_notes     : Edytuj Notatki                             |
        | help           : Display this help information              |
        | exit           : Exit the menu                              |
        +-------------------------------------------------------------+
        """
        slow_print(help_text)

    def show_ascii_art(self, username=None):
        slow_print(Fore.GREEN + "Zobacz ASCII art")

    def journal_menu(self, username):
        # Access the journal menu.
        journal = Journal()
        journal.journal_menu(username)

    def check_inactivity(self):
        if time.time() - self.last_activity_time > 300:  # 5 minut w sekundach
            slow_print(Fore.YELLOW + "You have been inactive for 5 minutes.")
            self.last_activity_time = time.time()  # Resetuj licznik aktywności
            self.boot_sequence()

    def handle_exit(self):
        slow_print(Fore.YELLOW + "Exiting...")
        self.last_activity_time = time.time()  # Resetuj licznik aktywności
        self.boot_sequence()

    def boot_sequence(self):
        # This method can represent the boot sequence or any intro animation
        slow_print(Fore.GREEN + "Booting up...")
        time.sleep(1)
        slow_print(Fore.YELLOW + "Loading system...")
        time.sleep(1)
        glitch_line("SYSTEM READY.")
