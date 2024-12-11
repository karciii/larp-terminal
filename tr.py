import random
import time
import threading
import keyboard  # Do obsługi klawiszy
from time import sleep
from colorama import Fore
from ascii_art import EVIL_CORP_ASCII, FOOTER_TEMPLATE
from utilities import (
    slow_print, loading_animation, matrix_rain, glitch_line,
    data_wave_effect, flickering_status_line, generate_footer, frame_effect
)
from encyclopedia import Encyclopedia
from journal import Journal
from login import Login


class BootSequence:
    stop_boot = False  # Flaga kontrolująca przerwanie bootowania
    inactivity_timer = None  # Zmienna do monitorowania nieaktywności
    inactivity_timeout = 300  # 5 minut w sekundach

    @staticmethod
    def check_for_user_input():
        """Monitorowanie klawisza 'u' w tle i ustawienie flagi do zatrzymania animacji."""
        while not BootSequence.stop_boot:
            if keyboard.is_pressed('u'):  # Jeśli naciśnięto 'u'
                BootSequence.stop_boot = True
                print(Fore.RED + "\n[BOOT SEQUENCE INTERRUPTED]")
                break
            sleep(0.1)  # Sprawdzaj co 100ms

    @staticmethod
    def start_inactivity_timer():
        """Uruchomienie timera do monitorowania nieaktywności (5 minut)."""
        def inactivity_countdown():
            time.sleep(BootSequence.inactivity_timeout)
            if not BootSequence.stop_boot:
                slow_print(Fore.YELLOW + "\nNo activity detected. Press any key to continue...")
                input()  # Użytkownik musi nacisnąć klawisz, aby kontynuować
                BootSequence.run()  # Ponownie uruchamiamy proces bootowania

        BootSequence.inactivity_timer = threading.Thread(target=inactivity_countdown)
        BootSequence.inactivity_timer.daemon = True  # Wątek zakończy się, gdy główny wątek się zakończy
        BootSequence.inactivity_timer.start()

    @staticmethod
    def stop_inactivity_timer():
        """Zatrzymanie timera nieaktywności."""
        if BootSequence.inactivity_timer:
            BootSequence.inactivity_timer = None

    @staticmethod
    def run():
        slow_print("[ SYSTEM BOOT INITIATED... ]\n")
        
        # Uruchomienie wątku monitorującego klawisze
        listener_thread = threading.Thread(target=BootSequence.check_for_user_input)
        listener_thread.daemon = True  # Wątek zakończy się, gdy główny wątek się zakończy
        listener_thread.start()

        BootSequence.start_inactivity_timer()  # Uruchamiamy timer nieaktywności
        
        loading_animation(" Loading Core Modules ")

        # Jeśli animacja bootowania nie została przerwana, kontynuuj
        while not BootSequence.stop_boot:
            slow_print("\n[ CORE MODULES LOADED ]\n")
            matrix_rain(duration=3)
            slow_print("\n[ Initializing Security Protocols... ]\n")
            flickering_status_line(" Authentication System ")
            sleep(0.5)

            # Jeśli animacja została przerwana, zakończ
            if BootSequence.stop_boot:
                break

        slow_print("[ ALL SYSTEMS OPERATIONAL ]\n")
        slow_print("-" * 60)
        slow_print(generate_footer())

    @staticmethod
    def boot_animation():
        """Animacja początkowa, przerwana po naciśnięciu 'u'."""
        for _ in range(20):  # Animacja trwa przez 20 iteracji
            if keyboard.is_pressed('u'):
                slow_print(Fore.GREEN + " Skipping boot sequence and entering menu... \n")
                return
            glitch_line(Fore.CYAN + "[ SYSTEM BOOTING... ]")
            time.sleep(0.1)

        # Po zakończeniu animacji, przerwa i przejście do końca
        BootSequence.shutdown_animation()

    @staticmethod
    def shutdown_animation():
        """Animacja zamykania systemu oraz glitchowe 'press any key to boot'"""
        slow_print(Fore.RED + " [ Shutting down system... ]")
        time.sleep(1)
        for _ in range(10):
            glitch_line(Fore.MAGENTA + " [ Press any key to boot ] ")
            time.sleep(0.1)

        slow_print(Fore.GREEN + "[ SYSTEM SHUTDOWN COMPLETE ]")
        slow_print(Fore.YELLOW + "[ PRESS ANY KEY TO BOOT ]")
        while True:
            if keyboard.is_pressed('enter'):  # Naciśnięcie 'Enter' by ponownie uruchomić system
                break
            time.sleep(0.1)
        slow_print(Fore.YELLOW + " Booting...\n")
        BootSequence.run()


class trCommands:
    @staticmethod
    def gadget_scan():
        slow_print("\n\n\n Activating Scanner... \n\n\n")
        loading_animation(" Scanning Area ")
        data_wave_effect(duration=2)
        results = [
            " No threats detected. ",
            " Signal interference detected nearby. ",
            " Unidentified object located in the area. ",
            " Radiation levels within safe limits. "
        ]
        slow_print(f" SCAN RESULT: {random.choice(results)} ")
        slow_print(generate_footer())

    @staticmethod
    def gadget_hack():
        slow_print(" Connecting to target system... ")
        glitch_line(" Establishing secure connection... ")
        loading_animation(" Decrypting Firewall ")
        success = random.random() > 0.4
        if success:
            data_wave_effect(duration=2)
            glitch_line("\n HACK SUCCESSFUL! Access Granted! \n")
            glitch_line("\n HACK SUCCESSFUL! Access Granted! \n")
        else:
            for i in range(random.randint(1, 13)):
                glitch_line(" HACK FAILED! Intrusion detected! ")
                sleep(1)
        slow_print(generate_footer())

    @staticmethod
    def gadget_decrypt():
        slow_print(" Initiating decryption sequence... \n\n")
        loading_animation(" Decrypting secure files... ")
        scenarios = [
            ("File decrypted: Classified personnel records.", "Success", "Decrypting personnel data..."),
            ("Decryption failed: Corrupted file.", "Failure", "Attempting recovery..."),
            ("File decrypted: Top secret prototype schematics.", "Success", "Decrypting schematics..."),
            ("Decryption attempt failed: Invalid key.", "Failure", "Retrying with a new key..."),
            ("Decrypting military-grade software... Please wait.", "Success", "Decryption successful."),
            ("Decryption halted: Security breach detected.", "Critical Failure", "System under attack..."),
            ("Map decrypted: Location coordinates of the hidden base.", "Success", "Decrypting location..."),
            ("Decryption failed: Time limit exceeded.", "Failure", "Resetting decryption..."),
            ("Encrypted message decrypted: 'The key is hidden under the third rock.'", "Success", "Decrypting message..."),
        ]

        result, status, process_message = random.choice(scenarios)
        slow_print(Fore.YELLOW + f" {process_message} ")

        if status == "Success":
            slow_print(Fore.GREEN + "[STATUS] Decryption Successful!")
            loading_animation(" Saving Data ")
            slow_print(Fore.GREEN + f" {result} ")
        elif status == "Failure":
            slow_print(Fore.RED + "[STATUS] Decryption Failed!")
            loading_animation(" Retrying... ")
            slow_print(Fore.RED + f" {result} ")
        elif status == "Critical Failure":
            slow_print(Fore.RED + "[STATUS] Critical Error!")
            slow_print(Fore.RED + "[ALERT] Security breach detected.")
            loading_animation(" Activating Countermeasures ")
            slow_print(Fore.RED + f" {result} ")

        slow_print(generate_footer())


class tr:
    def __init__(self):
        self.commands = {
            "scan": trCommands.gadget_scan,
            "hack": trCommands.gadget_hack,
            "decrypt": trCommands.gadget_decrypt,
            "help": self.show_help,
            "exit": self.exit_tr,
            "open_en": Encyclopedia().menu,
            "open_jr": self.journal_menu,
            "login": self.login,
        }

    def start(self):
        self.display_logo()
        BootSequence.run()  # Uruchamiamy proces bootowania
        frame_effect(" Type 'help' to see the list of commands. ")
        while True:
            user_input = input(Fore.GREEN + "> ").strip().lower()
            if user_input in self.commands:
                self.commands[user_input]()
            else:
                slow_print(Fore.RED + " Unknown command. Type 'help' for available commands. \n")

    def display_logo(self):
        for line in EVIL_CORP_ASCII.splitlines():
            slow_print(Fore.RED + line, min_delay=0.001, max_delay=0.02)
        slow_print(Fore.YELLOW + " Welcome to the EVIL CORP Terminal System \n")

    def show_help(self):
        """
        Wyświetlanie pomocy z użyciem animacji i glitchów.
        """
        help_text = """
        +-------------------------------------------------------------+
        |                       Available Commands                    |
        +-------------------------------------------------------------+
        | scan    : Perform a scan of the surrounding area.           |
        | hack    : Attempt to hack into a system.                    |
        | decrypt : Decrypt secure files.                             |
        | help    : Display this help information.                    |
        | exit    : Exit the Terminal.                                |
        | open_en : Access the encyclopedia.                          |
        | open_jr : Access and manage your journal entries.           |
        | login   : Open login menu.                                  |
        +-------------------------------------------------------------+
        """
        
        # Animacja wczytywania
        slow_print(Fore.CYAN + " Loading Help Information... ", end="\n")
        # loading_animation("Fetching Commands")
        
        # Glitchowy efekt wyświetlania pomocy
        slow_print(Fore.GREEN + "[HELP MENU]")
        slow_print(help_text)  # Glitchowy efekt wyświetlania pomocy
        
        # Powtarzający się glitch
        slow_print(Fore.WHITE + " Returning to menu... ")
        # loading_animation("Completing Help Sequence")
        slow_print(Fore.RED + " [ Command menu completed ] ")
        slow_print(generate_footer())  # Wyświetlenie stopki

    def exit_tr(self):
        frame_effect(" Shutting down the EVIL CORP tr... ", width=60)
        slow_print(generate_footer())
        exit(0)

    def journal_menu(self):
        journal = Journal()
        journal.journal_menu()

    def login(self):
        login = Login()
        login.login_menu()

