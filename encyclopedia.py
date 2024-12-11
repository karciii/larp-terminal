import json
import os
import textwrap
from colorama import Fore
from animations import slow_print, frame_effect

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
        with open(self.ENCYCLOPEDIA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    def load_users(self):
        """Loads user data from a file."""
        if not os.path.exists(self.USERS_FILE):
            slow_print(Fore.RED + "[ERROR] Users file not found. Creating a new one...")
            return {}
        with open(self.USERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    def validate_name(self, name):
        """Validates a name for categories or entries."""
        if not name or len(name) > 50 or any(char in name for char in "!@#$%^&*()[]{}<>?/\\|`~"):
            slow_print(Fore.RED + "[ERROR] Invalid name. Avoid special characters and limit to 50 characters.")
            return False
        return True

    def menu(self):
        """Displays the encyclopedia menu."""
        while True:
            frame_effect(" Encyclopedia Menu ", width=60)
            slow_print(" 1. Search for an entry")
            slow_print(" 2. View all entries")
            slow_print(" 3. View category summary")
            if self.current_user and self.current_user['access_level'] == 7:
                slow_print(" 4. Add/Edit an entry (Admin only)")
                slow_print(" 5. Add a new category (Admin only)")
            slow_print(" 6. Exit to main menu")
            choice = input(Fore.GREEN + "> ").strip()

            if choice == "1":
                self.search_entry()
            elif choice == "2":
                self.view_all_entries()
            elif choice == "3":
                self.view_categories_summary()
            elif choice == "4" and self.current_user and self.current_user['access_level'] == 7:
                self.add_or_edit_entry()
            elif choice == "5" and self.current_user and self.current_user['access_level'] == 7:
                self.add_category()
            elif choice == "6":
                slow_print(Fore.YELLOW + "Returning to main menu...")
                break
            else:
                slow_print(Fore.RED + "Invalid choice. Please try again.")

    def display_entry(self, entry_details):
        """Displays entry details in a table format with improved aesthetics."""
        table_header = Fore.CYAN + "+" + "-" * 20 + "+" + "-" * 50 + "+"
        table_row_format = "| {key:<18} | {value:<48} |"

        slow_print(table_header)
        slow_print(Fore.GREEN + "| Key                | Value                                              |")
        slow_print(table_header)

        for key, value in entry_details.items():
            if isinstance(value, list):
                value = ", ".join(value)

            wrapped_value = textwrap.fill(value, width=48)
            for idx, line in enumerate(wrapped_value.split("\n")):
                if idx == 0:
                    slow_print(Fore.WHITE + table_row_format.format(key=key.capitalize(), value=line))
                else:
                    slow_print(Fore.WHITE + table_row_format.format(key="", value=line))

        slow_print(table_header)

    def highlight_text(self, text, keyword):
        """Highlights the keyword in the given text."""
        return text.replace(keyword, Fore.RED + keyword + Fore.RESET)

    def search_entry(self):
        """Searches for an entry by keyword with highlighted results."""
        keyword = input("Enter search keyword: ").strip().lower()
        results = []

        for category, entries in self.data.items():
            for entry_name, details in entries.items():
                if keyword in entry_name.lower() or any(keyword in str(value).lower() for value in details.values()):
                    results.append((category, entry_name, details))

        if results:
            slow_print(Fore.YELLOW + f"Found {len(results)} matching entries:\n")
            for category, entry_name, details in results:
                frame_effect(f" {self.highlight_text(entry_name.capitalize(), keyword)} ({category.capitalize()}) ", width=60)
                self.display_entry(details)
        else:
            slow_print(Fore.RED + f"No entries found containing '{keyword}'.")

    def view_categories_summary(self):
        """Displays a summary of all categories and their entry counts."""
        if not self.data:
            slow_print(Fore.RED + "No categories available.")
            return

        frame_effect(" Encyclopedia Categories Summary ", width=60)
        for category, entries in sorted(self.data.items()):
            slow_print(Fore.YELLOW + f"Category: {category.capitalize()} - {len(entries)} entries")
