import json
import time
from random import choice
from animations import *
from colorama import Fore
from tabulate import tabulate  # Do formatowania tabel logów
import msvcrt  # Do wykrywania naciśnięcia klawisza

class Login:
    def __init__(self):
        self.users = self.load_users()
        self.failed_attempts = {}
        self.locked_users = {}
        self.last_activity_time = time.time()  # Czas ostatniej aktywności

    def load_users(self):
        try:
            with open('data/users.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            slow_print(Fore.RED + "ERROR: users.json not found!")
            return {}
        except json.JSONDecodeError:
            slow_print(Fore.RED + "ERROR: Error parsing users.json!")
            return {}
        except Exception as e:
            slow_print(Fore.RED + f"ERROR: {str(e)}")
            return {}

    def save_users(self):
        try:
            with open('data/users.json', 'w') as f:
                json.dump(self.users, f)
        except Exception as e:
            slow_print(Fore.RED + f"ERROR: Failed to save users data - {str(e)}")

    def log_operation(self, username, operation_type, message_length):
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "username": username,
            "operation": operation_type,
            "length": message_length
        }
        try:
            with open('data/crypto_logs.json', 'a') as log_file:
                log_file.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            slow_print(Fore.RED + f"ERROR: Failed to write log - {str(e)}")

    def view_crypto_logs(self):
        try:
            with open('data/crypto_logs.json', 'r') as log_file:
                logs = [json.loads(log) for log in log_file.readlines()]
                if logs:
                    table = [
                        [log["timestamp"], log["username"], log["operation"], log["length"]]
                        for log in logs
                    ]
                    slow_print(Fore.GREEN + tabulate(
                        table, headers=["Timestamp", "Username", "Operation", "Message Length"], tablefmt="grid"
                    ))
                else:
                    slow_print(Fore.YELLOW + "No logs available.")
        except FileNotFoundError:
            slow_print(Fore.RED + "No logs file found.")
        except json.JSONDecodeError:
            slow_print(Fore.RED + "Error reading logs file.")

    def xor_encrypt(self, message):
        key = len(message)
        encrypted = ''.join(chr(ord(char) ^ key) for char in message)
        return encrypted

    def xor_decrypt(self, message):
        key = len(message)
        decrypted = ''.join(chr(ord(char) ^ key) for char in message)
        return decrypted

    def login_menu(self):
        username = input(Fore.YELLOW + "Username: ").strip()

        if username in self.locked_users:
            if time.time() < self.locked_users[username]:
                slow_print(Fore.RED + "Account is locked. Try again later.")
                glitch_line("LOCKED: Unauthorized access detected.")
                return
            else:
                del self.locked_users[username]

        if username not in self.users:
            slow_print(Fore.RED + "User not found!")
            glitch_line("ERROR: User does not exist in the database.")
            return

        attempts = 0
        while attempts < 3:
            password = input(Fore.YELLOW + "Password: ").strip()
            if self.check_credentials(username, password):
                slow_print(Fore.GREEN + "Login successful!")
                glitch_line("SYSTEM ACCESS GRANTED.")
                self.show_user_menu(username)
                return
            else:
                slow_print(Fore.RED + "Incorrect password.")
                glitch_line("ERROR: Invalid password.")
                attempts += 1

        slow_print(Fore.RED + "Too many failed attempts. Locking account for 1 minute.")
        self.locked_users[username] = time.time() + 60
        glitch_line("Account temporarily locked.")

    def check_credentials(self, username, password):
        return username in self.users and self.users[username]['password'] == password

    def show_user_menu(self, username):
        user_level = self.users[username]['access_level']
        slow_print(Fore.GREEN + f"Welcome {username}, Access Level: {user_level}")

        menu_options = self.get_menu_options(user_level)
        while True:
            self.check_inactivity()  # Check if user has been inactive for 5 minutes

            slow_print(Fore.YELLOW + "Available options:")
            for idx, option in enumerate(menu_options, 1):
                slow_print(Fore.GREEN + f"{idx}. {option}")
            choice = input(Fore.YELLOW + "Choose an option (or type 'exit' to logout): ").strip().lower()
            if choice == 'exit':
                self.handle_exit()
                break

            if choice.isdigit() and 1 <= int(choice) <= len(menu_options):
                self.handle_option(int(choice), username)
            else:
                slow_print(Fore.RED + "Invalid choice. Please try again.")
                glitch_line("ERROR: Invalid menu option.")

    def get_menu_options(self, access_level):
        all_options = [
            "Zobacz gołe baby (ASCII art)",
            "Otwórz Logi",
            "Zaszyfruj Wiadomość",
            "Odszyfruj Wiadomość",
            "Zobacz logi enkrypcji",
            "Uzbrój rakietę",
            "Edytuj Notatki",
        ]
        return all_options[:access_level]

    def handle_option(self, option, username):
        if option == 1:
            self.view_baby_ascii()
        elif option == 2:
            self.access_logs()
        elif option == 3:
            self.encrypt_message(username)
        elif option == 4:
            self.decrypt_message(username)
        elif option == 5:
            self.view_crypto_logs()
        elif option == 6:
            self.arm_rocket()
        elif option == 7:
            self.edit_notes(username)
        else:
            slow_print(Fore.RED + "Wybrano nieznaną opcję.")
            glitch_line("ERROR: Niepoprawna opcja.")

    def view_baby_ascii(self):
        try:
            with open('data/baby_art.txt', 'r', encoding='utf-8') as f:  # Określenie kodowania
                ascii_art = f.read().split('--splitter--')
                selected_art = choice(ascii_art).strip()
                slow_print(Fore.GREEN + selected_art)
        except FileNotFoundError:
            slow_print(Fore.RED + "ERROR: baby_art.txt not found!")
        except UnicodeDecodeError as e:
            slow_print(Fore.RED + f"ERROR: Could not decode the file - {str(e)}")

    def encrypt_message(self, username):
        message = input(Fore.YELLOW + "Enter the message to encrypt: ").strip()
        encrypted_message = self.xor_encrypt(message)
        slow_print(Fore.GREEN + f"Encrypted Message: {encrypted_message}")
        self.log_operation(username, "Encryption", len(message))

    def decrypt_message(self, username):
        encrypted_message = input(Fore.YELLOW + "Enter the encrypted message: ").strip()
        try:
            decrypted_message = self.xor_decrypt(encrypted_message)
            slow_print(Fore.GREEN + f"Decrypted Message: {decrypted_message}")
            self.log_operation(username, "Decryption", len(encrypted_message))
        except Exception as e:
            slow_print(Fore.RED + f"ERROR: Decryption failed - {str(e)}")

    def edit_notes(self, username):
        slow_print(Fore.GREEN + f"Editing notes for {username}.")
        glitch_line("Notes opened for modification.")

    def access_logs(self):
        slow_print(Fore.GREEN + "Accessing logs.")
        glitch_line("Logs accessed.")

    def arm_rocket(self):
        slow_print(Fore.RED + "Arming rocket!")
        glitch_line("Rocket armed. Awaiting further commands.")

    def check_inactivity(self):
        if time.time() - self.last_activity_time > 300:  # 5 minutes in seconds
            slow_print(Fore.YELLOW + "You have been inactive for 5 minutes. Press any key to continue...")
            msvcrt.getch()  # Wait for key press to continue
            self.last_activity_time = time.time()  # Reset activity timer
            self.boot_sequence()

    def handle_exit(self):
        slow_print(Fore.YELLOW + "Press any key to continue...")
        msvcrt.getch()  # Wait for key press to continue
        self.last_activity_time = time.time()  # Reset activity timer
        self.boot_sequence()

    def boot_sequence(self):
        # This method can represent the boot sequence or any intro animation
        slow_print(Fore.GREEN + "Booting up...")
        time.sleep(1)
        slow_print(Fore.YELLOW + "Loading system...")
        time.sleep(1)
        glitch_line("SYSTEM READY.")
