import json
import random
# import pyttsx3
from colorama import Fore
from animations import slow_print, frame_effect
import shutil
import subprocess
import sys

class Journal:
    """Handles the player's journal system with histories."""

    JOURNAL_FILE = "data/journal.json"

    def __init__(self):
        self.entries = self.load_entries()
        self._tts_backend = None
        # wybierz backend TTS
        if sys.platform.startswith("linux") and shutil.which("espeak"):
            self._tts_backend = "espeak"
        elif sys.platform.startswith("win") and shutil.which("powershell"):
            self._tts_backend = "powershell"
        else:
            self._tts_backend = None  # brak TTS, fallback -> print

    def configure_tts(self):
        """Configures the TTS engine with a more robotic voice."""
        # voices = self.tts_engine.getProperty('voices')
        
        # Try to select a robotic or male voice
        # for voice in voices:
        #     if 'robot' in voice.name.lower() or 'male' in voice.name.lower():
        #         self.tts_engine.setProperty('voice', voice.id)
        #         break
        # else:
        #     self.tts_engine.setProperty('voice', voices[0].id)  # Fallback to first available voice

        # Setting a lower rate (slower speech) for a more mechanical tone
        # self.tts_engine.setProperty('rate', 90)  # Slower speed for a robotic feel
        
        # # Setting pitch to lower values for a deeper, more metallic sound
        # self.tts_engine.setProperty('pitch', 8)  # Decrease pitch for a more robotic tone
        
        # # Adjust volume to maintain a consistent robotic feel
        # self.tts_engine.setProperty('volume', 0.9)  # Volume at 90%
        pass

    def speak_text(self, text):
        """Cross-platform minimal TTS: espeak on Linux, PowerShell on Windows, else print."""
        if self._tts_backend == "espeak":
            try:
                subprocess.run(["espeak", "--stdin"], input=text.encode("utf-8"), check=False)
            except Exception:
                slow_print(Fore.CYAN + text)
        elif self._tts_backend == "powershell":
            # prosty PowerShell TTS (Windows) — optional
            try:
                # escape single quotes for PowerShell single-quoted string by doubling them
                ps_text = text.replace("'", "''")
                ps_cmd = (
                    "Add-Type -AssemblyName System.speech; "
                    f"(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{ps_text}')"
                )
                subprocess.run(["powershell", "-Command", ps_cmd], check=False)
            except Exception:
                slow_print(Fore.CYAN + text)
        else:
            # fallback: nie ma TTS — tylko wypisz
            slow_print(Fore.CYAN + text)

    def journal_menu(self, username):
        while True:
            journal_menu = '''
            +----------------------------------------------------------+
            |                       Journal Menu                       |
            +----------------------------------------------------------+
            | open: Przeglądaj istniejące wpisy w dzienniku.           |
            | enter: Dodaj nowy wpis do dziennika (tylko admin).       |
            | exit: Powrót do menu głównego.                          |
            +----------------------------------------------------------+    
            '''
            slow_print(Fore.CYAN + journal_menu)

            choice = input(Fore.GREEN + "Wybierz opcję: ").strip().lower()

            if choice == "open":
                self.view_entries()
            elif choice == "enter":
                self.add_entry(username)
            elif choice == "exit":
                break
            else:
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

    def add_entry(self, username):
        """Adds a new entry to the journal."""
        # Sprawdź, czy użytkownik ma uprawnienia administratora
        if username != "admin":
            slow_print(Fore.RED + "Only the admin can add new journal entries.")
            return

        title = input("Entry title: ").strip()
        summary = input("Entry summary: ").strip()
        date = input("Entry date (YYYY-MM-DD): ").strip()
        location = input("Entry location: ").strip()
        persons = input("Persons involved (comma separated): ").split(",")
        category = input("Category of entry: ").strip()

        # Generowanie unikalnego entry_id
        existing_ids = {entry["entry_id"] for entry in self.entries["histories"]}
        while True:
            entry_id = f"{random.randint(100000, 999999)}"  # Losowy 6-cyfrowy numer
            if entry_id not in existing_ids:
                break

        entry = {
            "entry_id": entry_id,
            "title": title,
            "summary": summary,
            "date": date,
            "location": location,
            "persons": [person.strip() for person in persons],
            "category": category
        }

        self.entries["histories"].append(entry)
        self.save_entries()
        self.speak_text(f"Entry '{title}' has been added to the journal with ID {entry_id}.")
        slow_print(Fore.GREEN + f"Entry '{title}' added to the journal with ID {entry_id}.")

    def view_entries(self):
        """Displays a journal entry based on a 6-digit entry ID."""
        if not self.entries["histories"]:
            slow_print(Fore.YELLOW + "The journal is empty.")
            return

        try:
            entry_id = input(Fore.GREEN + "Enter a 6-digit entry ID: ").strip()
            if len(entry_id) != 6 or not entry_id.isdigit():
                slow_print(Fore.RED + "Invalid entry ID. Please enter a 6-digit number.")
                return

            # Search for the entry with the given entry_id
            entry = next((entry for entry in self.entries["histories"] if entry["entry_id"] == entry_id), None)

            if entry:
                self.speak_text(f"Title: {entry['title']}, Date: {entry['date']}, Location: {entry['location']}, Summary: {entry['summary']}.")
                slow_print(Fore.CYAN + f"\nTitle: {entry['title']}\n" +
                           f"Date: {entry['date']}\nLocation: {entry['location']}\n" +
                           f"Category: {entry['category']}\n" +
                           Fore.WHITE + f"Summary: {entry['summary']}\n")
            else:
                slow_print(Fore.RED + f"No entry found with ID {entry_id}.")
        except Exception as e:
            slow_print(Fore.RED + f"An error occurred: {e}")
