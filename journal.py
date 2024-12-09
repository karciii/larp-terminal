import json
import pyttsx3
from colorama import Fore
from animations import slow_print
from utilities import frame_effect  # Ensure it's imported

class Journal:
    """Handles the player's journal system."""

    JOURNAL_FILE = "journal_entries.json"

    def __init__(self):
        self.entries = self.load_entries()
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Set speech speed
        self.tts_engine.setProperty('voice', 'pl')  # Set voice to Polish

    def journal_menu(self):
        """Displays the journal menu."""
        while True:
            frame_effect(" Journal Menu ", width=60)
            slow_print(" 1. View Entries ")
            slow_print(" 2. Add Entry ")
            slow_print(" 3. Read Entry Aloud ")
            slow_print(" 4. Return to Main Menu ")
            choice = input(Fore.GREEN + "> ").strip()
            if choice == "1":
                self.view_entries()
            elif choice == "2":
                self.add_entry()
            elif choice == "3":
                self.read_entry_aloud()
            elif choice == "4":
                break
            else:
                slow_print(Fore.RED + "Invalid choice. Please try again.")

    def load_entries(self):
        """Loads journal entries from a file."""
        try:
            with open(self.JOURNAL_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}  # No entries yet
        except json.JSONDecodeError:
            slow_print(Fore.RED + "[ERROR] Failed to load journal file.")
            return {}

    def save_entries(self):
        """Saves journal entries to a file."""
        try:
            with open(self.JOURNAL_FILE, "w") as file:
                json.dump(self.entries, file, indent=4)
        except Exception as e:
            slow_print(Fore.RED + f"[ERROR] Could not save journal: {e}")

    def add_entry(self):
        """Adds a new entry to the journal."""
        title = input("Entry title: ").strip()
        content = input("Entry content: ").strip()
        self.entries[title] = content
        self.save_entries()
        slow_print(Fore.GREEN + f"Entry '{title}' added to the journal.")

    def view_entries(self):
        """Displays all entries in the journal."""
        if not self.entries:
            slow_print(Fore.YELLOW + "The journal is empty.")
            return
        slow_print("Journal Entries:")
        for title, content in self.entries.items():
            slow_print(Fore.CYAN + f"\nTitle: {title}\n" + Fore.WHITE + content)

    def read_entry_aloud(self):
        """Reads journal entries aloud using TTS."""
        if not self.entries:
            slow_print(Fore.YELLOW + "The journal is empty.")
            return
        self.view_entries()
        title = input("Enter the title of the entry to read aloud: ").strip()
        if title in self.entries:
            self.tts_engine.say(self.entries[title])
            self.tts_engine.runAndWait()
        else:
            slow_print(Fore.RED + f"No entry found with title '{title}'.")
