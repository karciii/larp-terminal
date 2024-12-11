import json
import os
from colorama import Fore
from animations import slow_print, frame_effect, glitch_line

class Encyclopedia:
    """Handles the in-game encyclopedia."""

    ENCYCLOPEDIA_FILE = "data/encyclopedia.json"
    USERS_FILE = "data/users.json"

    def __init__(self):
        self.data = self.load_encyclopedia()
        self.users = self.load_users()
        self.current_user = None

    def load_encyclopedia(self):
        """Loads encyclopedia data from a file."""
        if not os.path.exists(self.ENCYCLOPEDIA_FILE):
            slow_print(Fore.RED + "[ERROR] Encyclopedia file not found. Creating a new one...")
            return {}
        with open(self.ENCYCLOPEDIA_FILE, "r") as file:
            return json.load(file)

    def load_users(self):
        """Loads user data from a file."""
        if not os.path.exists(self.USERS_FILE):
            slow_print(Fore.RED + "[ERROR] Users file not found. Creating a new one...")
            return {}
        with open(self.USERS_FILE, "r") as file:
            return json.load(file)

    def save_encyclopedia(self):
        """Saves the encyclopedia data to a file."""
        with open(self.ENCYCLOPEDIA_FILE, "w") as file:
            json.dump(self.data, file, indent=4)

    def menu(self):
        """Displays the encyclopedia menu."""
        while True:
            frame_effect(" Encyclopedia Menu ", width=60)
            slow_print(" 1. Search for an entry")
            slow_print(" 2. View all entries")
            if self.current_user and self.current_user['access_level'] == 7:
                slow_print(" 3. Add/Edit an entry (Admin only)")
                slow_print(" 4. Add a new category (Admin only)")
            slow_print(" 5. Exit to main menu")
            choice = input(Fore.GREEN + "> ").strip()

            if choice == "1":
                self.search_entry()
            elif choice == "2":
                self.view_all_entries()
            elif choice == "3" and self.current_user and self.current_user['access_level'] == 7:
                self.add_or_edit_entry()
            elif choice == "4" and self.current_user and self.current_user['access_level'] == 7:
                self.add_category()
            elif choice == "5":
                slow_print(Fore.YELLOW + "Returning to main menu...")
                break
            else:
                slow_print(Fore.RED + "Invalid choice. Please try again.")

    def authenticate_user(self):
        """Authenticates a user and sets the current user."""
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        user = self.users.get(username)
        if user and user["password"] == password:
            self.current_user = user
            slow_print(Fore.GREEN + "[SUCCESS] User authenticated.")
            return True
        slow_print(Fore.RED + "[ERROR] Authentication failed.")
        return False

    def add_category(self):
        """Adds a new category to the encyclopedia. Admin only."""
        if not self.authenticate_user() or self.current_user['access_level'] != 7:
            return

        category_name = input("Enter new category name: ").strip()
        if category_name in self.data:
            slow_print(Fore.RED + f"Category '{category_name}' already exists.")
        else:
            self.data[category_name] = {}
            self.save_encyclopedia()
            slow_print(Fore.GREEN + f"Category '{category_name}' has been added.")

    def add_or_edit_entry(self):
        """Adds or edits an entry in the encyclopedia. Admin only."""
        if not self.authenticate_user() or self.current_user['access_level'] != 7:
            return

        category_name = input("Enter category name: ").strip()
        if category_name not in self.data:
            slow_print(Fore.RED + f"Category '{category_name}' does not exist.")
            return

        entry_name = input("Enter entry name: ").strip()
        if entry_name in self.data[category_name]:
            slow_print(Fore.YELLOW + f"Editing existing entry '{entry_name}' in category '{category_name}'.")
        else:
            slow_print(Fore.YELLOW + f"Adding new entry '{entry_name}' to category '{category_name}'.")

        entry_details = {}
        while True:
            key = input("Enter detail key (or leave blank to finish): ").strip()
            if not key:
                break
            value = input(f"Enter value for '{key}': ").strip()
            entry_details[key] = value

        self.data[category_name][entry_name] = entry_details
        self.save_encyclopedia()
        slow_print(Fore.GREEN + f"Entry '{entry_name}' has been saved in category '{category_name}'.")

    def search_entry(self):
        """Searches for an entry by keyword."""
        keyword = input("Enter search keyword: ").strip().lower()
        results = []

        for category, entries in self.data.items():
            for entry_name, details in entries.items():
                if keyword in entry_name.lower() or any(keyword in str(value).lower() for value in details.values()):
                    results.append((category, entry_name, details))

        if results:
            slow_print(Fore.YELLOW + f"Found {len(results)} matching entries:\n")
            for category, entry_name, details in results:
                frame_effect(f" {entry_name.capitalize()} ({category.capitalize()}) ", width=60)
                self.display_entry(details)
        else:
            slow_print(Fore.RED + f"No entries found containing '{keyword}'.")

    def view_all_entries(self):
        """Displays all entries in all categories."""
        if not self.data:
            slow_print(Fore.RED + "No entries available.")
            return

        for category, entries in self.data.items():
            frame_effect(f" {category.capitalize()} ", width=60)
            for entry_name, details in entries.items():
                self.display_entry(details)

    def display_entry(self, entry_details):
        """Displays entry details in a table format."""
        frame_effect(" Entry Details ", width=60)
        for key, value in entry_details.items():
            if isinstance(value, list):
                value = ", ".join(value)
            slow_print(f"{key.capitalize():<15}: {value}")
        slow_print(Fore.YELLOW + "-" * 60)
