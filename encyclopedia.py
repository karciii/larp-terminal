import json
from colorama import Fore
from animations import slow_print, frame_effect

class Encyclopedia:
    """Handles the in-game encyclopedia."""

    ENCYCLOPEDIA_FILE = "encyclopedia.json"

    def __init__(self):
        self.data = self.load_encyclopedia()

    def load_encyclopedia(self):
        """Loads encyclopedia data from a file."""
        try:
            with open(self.ENCYCLOPEDIA_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            slow_print(Fore.RED + "[ERROR] Encyclopedia file not found.")
            return {}

    def menu(self):
        """Displays the encyclopedia menu."""
        while True:
            frame_effect(" Encyclopedia Menu ", width=60)
            slow_print(" 1. Search for an entry ")
            slow_print(" 2. View all entries ")
            slow_print(" 3. Exit to main menu ")
            choice = input(Fore.GREEN + "> ").strip()
            if choice == "1":
                self.search_entry()
            elif choice == "2":
                self.view_all_entries()
            elif choice == "3":
                slow_print(Fore.YELLOW + "Returning to main menu...")
                break
            else:
                slow_print(Fore.RED + "Invalid choice. Please try again.")

    def search_entry(self):
        """Searches and displays a specific entry."""
        slow_print(Fore.YELLOW + "Categories: locations, factions, events")
        category = input("Enter category: ").strip().lower()
        if category not in self.data:
            slow_print(Fore.RED + "Invalid category. Please choose from: locations, factions, or events.")
            return

        entry = input("Enter entry name: ").strip()
        entry = entry.lower()  # Ensure the search is case-insensitive

        if category not in self.data:
            slow_print(Fore.RED + "Category not found.")
            return

        try:
            details = self.data[category][entry]
            slow_print(Fore.YELLOW + f"\n{entry.capitalize()}:")
            for key, value in details.items():
                slow_print(Fore.CYAN + f"{key.capitalize()}: {value}")
        except KeyError:
            slow_print(Fore.RED + f"Entry '{entry}' not found in the '{category}' category.")

    def view_all_entries(self):
        """Displays all entries in all categories."""
        slow_print(Fore.YELLOW + "Viewing all entries...\n")
        if not self.data:
            slow_print(Fore.RED + "No entries available.")
            return
        
        for category, entries in self.data.items():
            slow_print(Fore.MAGENTA + f"\n{category.capitalize()}:")
            for entry_name, entry_details in entries.items():
                slow_print(Fore.CYAN + f"- {entry_name.capitalize()}: {entry_details['opis'][:50]}...")  # Show first 50 chars of description
            slow_print(Fore.YELLOW + f"--- End of {category.capitalize()} ---")
