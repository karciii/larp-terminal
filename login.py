import json
import time
from random import randint
from utilities import slow_print, glitch_line, loading_animation
from colorama import Fore


class Login:
    def __init__(self):
        # Załaduj dane użytkowników
        self.users = self.load_users()
        self.failed_attempts = {}
        self.locked_users = {}
    
    def load_users(self):
        try:
            with open('users.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("DEBUG: users.json not found!")
            slow_print(Fore.RED + "ERROR: users.json not found!")
            return {}
        except json.JSONDecodeError:
            print("DEBUG: Error parsing users.json!")
            slow_print(Fore.RED + "ERROR: Error parsing users.json!")
            return {}
        except Exception as e:
            print(f"DEBUG: Unexpected error: {e}")
            slow_print(Fore.RED + f"ERROR: {str(e)}")
            return {}

    def save_users(self):
        # Zapisz zmiany w danych użytkowników
        try:
            with open('users.json', 'w') as f:
                json.dump(self.users, f)
        except Exception as e:
            slow_print(Fore.RED + f"ERROR: Failed to save users data - {str(e)}")

    def login_menu(self):
        # Logowanie użytkownika
        username = input(Fore.YELLOW + "Username: ").strip()

        # Sprawdź, czy konto jest zablokowane
        if username in self.locked_users:
            if time.time() < self.locked_users[username]:
                slow_print(Fore.RED + "Account is locked. Try again later.")
                glitch_line("LOCKED: Unauthorized access detected.")
                return
            else:
                del self.locked_users[username]  # Odblokowanie użytkownika po 1 minucie

        # Jeśli użytkownik nie istnieje
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

        # lock the account after 3 wrong tries
        slow_print(Fore.RED + "Too many failed attempts. Locking account for 1 minute.")
        self.locked_users[username] = time.time() + 60  # lock for 1 minute
        glitch_line("Account temporarily locked.")
        glitch_line("Try again in some time.")


    def check_credentials(self, username, password):
        if username in self.users and self.users[username]['password'] == password:
            return True
        return False

    def show_user_menu(self, username):
        user_level = self.users[username]['access_level']
        slow_print(Fore.GREEN + f"Welcome {username}, Access Level: {user_level}")

        menu_options = self.get_menu_options(user_level)
        while True:
            slow_print(Fore.YELLOW + "Available options:")
            for idx, option in enumerate(menu_options, 1):
                slow_print(Fore.GREEN + f"{idx}. {option}")
            choice = input(Fore.YELLOW + "Choose an option (or type 'exit' to logout): ").strip().lower()
            if choice == 'exit':
                slow_print(Fore.GREEN + "Logging out...")
                glitch_line("User logged out. Goodbye.")
                break
            if choice.isdigit() and 1 <= int(choice) <= len(menu_options):
                self.handle_option(int(choice), username)
            else:
                slow_print(Fore.RED + "Invalid choice. Please try again.")
                glitch_line("ERROR: Invalid menu option.")

    def get_menu_options(self, access_level):
        # Opcje dostępne w menu na podstawie poziomu dostępu
        all_options = [
            "Gołe baby",
            "Notatki",
            "Otwórz logi",
            "Odszyfruj wiadomość",
            "Uzbrój rakiete"
        ]
        # Zwraca tylko dostępne opcje na podstawie poziomu dostępu użytkownika
        return all_options[:access_level]

    def handle_option(self, option, username):
        # Obsługuje wybraną opcję z menu
        if option == 1:
            slow_print(f"Viewing profile of {username}")
            glitch_line("Profile data retrieved.")
        elif option == 2:
            slow_print(f"Editing notes for {username}")
            glitch_line("Notes opened for modification.")
        elif option == 3:
            slow_print("Accessing logs")
            glitch_line("Logs accessed.")
        else:
            slow_print(Fore.RED + "Unknown option selected.")
            glitch_line("ERROR: Invalid option.")
