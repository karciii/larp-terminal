import json
import pyttsx3
import time
from colorama import Fore
from animations import slow_print, glitch_line
from utilities import frame_effect


class Journal:
    """Handles the player's journal system with histories."""

    JOURNAL_FILE = "data/journal.json"

    def __init__(self):
        self.entries = self.load_entries()
        self.tts_engine = pyttsx3.init()
        self.configure_tts()

    def configure_tts(self):
        """Configures the TTS engine with a more robotic voice."""
        voices = self.tts_engine.getProperty('voices')
        
        # Try to select a robotic or male voice
        for voice in voices:
            if 'robot' in voice.name.lower() or 'male' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        else:
            self.tts_engine.setProperty('voice', voices[0].id)  # Fallback to first available voice

        # Setting a lower rate (slower speech) for a more mechanical tone
        self.tts_engine.setProperty('rate', 80)  # Slower speed for a robotic feel
        
        # Setting pitch to lower values for a deeper, more metallic sound
        self.tts_engine.setProperty('pitch', 11)  # Decrease pitch for a more robotic tone
        
        # Adjust volume to maintain a consistent robotic feel
        self.tts_engine.setProperty('volume', 0.9)  # Volume at 90%

    def speak_text(self, text):
        """Reads the text aloud using TTS."""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def journal_menu(self):
        """Displays the journal menu."""
        while True:
            frame_effect(" Journal Menu ", width=60)
            slow_print(" 1. View Entries ")
            slow_print(" 2. Add Entry ")
            slow_print(" 3. Return to Main Menu ")
            choice = input(Fore.GREEN + "> ").strip()
            if choice == "1":
                self.view_entries()
            elif choice == "2":
                self.add_entry()
            elif choice == "3":
                break
            else:
                self.speak_text("Invalid choice. Please try again.")
                slow_print(Fore.RED + "Invalid choice. Please try again.")

    def load_entries(self):
        """Loads journal entries from the JSON file."""
        try:
            with open(self.JOURNAL_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"histories": []}
        except json.JSONDecodeError:
            self.speak_text("Failed to load the journal file.")
            slow_print(Fore.RED + "[ERROR] Failed to load the journal file.")
            return {"histories": []}

    def save_entries(self):
        """Saves journal entries to the JSON file."""
        try:
            with open(self.JOURNAL_FILE, "w", encoding="utf-8") as file:
                json.dump(self.entries, file, indent=4)
        except Exception as e:
            self.speak_text("Could not save the journal.")
            slow_print(Fore.RED + f"[ERROR] Could not save the journal: {e}")

    def add_entry(self):
        """Adds a new entry to the journal."""
        title = input("Entry title: ").strip()
        summary = input("Entry summary: ").strip()
        date = input("Entry date (YYYY-MM-DD): ").strip()
        location = input("Entry location: ").strip()
        persons = input("Persons involved (comma separated): ").split(",")
        category = input("Category of entry: ").strip()

        entry = {
            "title": title,
            "summary": summary,
            "date": date,
            "location": location,
            "persons": [person.strip() for person in persons],
            "category": category
        }

        self.entries["histories"].append(entry)
        self.save_entries()
        self.speak_text(f"Entry '{title}' has been added to the journal.")
        slow_print(Fore.GREEN + f"Entry '{title}' added to the journal.")

    def view_entries(self):
        """Displays all entries in the journal."""
        if not self.entries["histories"]:
            self.speak_text("Dziennik jest pusty")
            slow_print(Fore.YELLOW + "The journal is empty.")
            return

        self.speak_text("Wyświetlanie wpisów")
        slow_print("Journal Entries (Titles):")
        for idx, entry in enumerate(self.entries["histories"], 1):
            self.speak_text(entry['title'])
            slow_print(Fore.CYAN + f"{idx}. {entry['title']}")

        try:
            entry_number = int(input("\nEnter the number of the entry to view or 0 to return: ").strip())
            if entry_number == 0:
                return
            if 1 <= entry_number <= len(self.entries["histories"]):
                entry = self.entries["histories"][entry_number - 1]
                self.speak_text(f"Title: {entry['title']}, Date: {entry['date']}, Location: {entry['location']}, Summary: {entry['summary']}.")
                slow_print(Fore.CYAN + f"\nTitle: {entry['title']}\n" +
                           f"Date: {entry['date']}\nLocation: {entry['location']}\n" +
                           f"Category: {entry['category']}\n" +
                           Fore.WHITE + f"Summary: {entry['summary']}\n")
            else:
                self.speak_text("Niewłaściwy numer wpisu.")
                slow_print(Fore.RED + "Invalid entry number.")
        except ValueError:
            self.speak_text("Niewłaściwy parametr wejścia. Wpisz poprawny numer.")
            slow_print(Fore.RED + "Invalid input. Please enter a valid number.")
