from ascii_art import EVIL_CORP_ASCII, FOOTER_TEMPLATE
from utilities import (
    slow_print, loading_animation, matrix_rain, glitch_line,
    data_wave_effect, flickering_status_line, generate_footer, frame_effect
)
from colorama import Fore
from encyclopedia import Encyclopedia
import random
from utilities import frame_effect, slow_print, glitch_line
from journal import Journal
from time import sleep 

class BootSequence:
    @staticmethod
    def run():
        slow_print("[ SYSTEM BOOT INITIATED... ]\n")
        loading_animation(" Loading Core Modules ")
        slow_print("\n[ CORE MODULES LOADED ]\n")
        matrix_rain(duration=3)
        slow_print("\n[ Initializing Security Protocols... ]\n")
        flickering_status_line(" Authentication System ")
        slow_print("[ ALL SYSTEMS OPERATIONAL ]\n")
        slow_print("-" * 60)
        slow_print(generate_footer())
        pass


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
            for i in range(random.randint(1,13)):
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
            ("Encrypted message decrypted: 'The key is hidden under the third rock.'", "Success", "Decrypting message...")
        ]

        # Choose a random scenario
        result, status, process_message = random.choice(scenarios)

        # Show process message
        slow_print(Fore.YELLOW + f" {process_message} ")

        # Different types of progress bars based on the scenario
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
        elif status == "Success" and "map" in result.lower():
            # Display an ASCII map when location data is decrypted
            slow_print(Fore.GREEN + " Decryption successful. Displaying map...")
            ascii_map = """
                                _,__        .:
                        Darwin <*  /        | \
                            .-./     |.     :  :,
                        /           '-._/     \_
                        /                '       \
                        .'                         *: Brisbane
                    .-'                             ;
                    |                               |
                    \                              /
                    |                            /
                Perth  \*        __.--._          /
                        \     _.'       \:.       |
                        >__,-'             \_/*_.-'
                                            Melbourne
                                            :--,
                                            '/
                    """
            slow_print(Fore.CYAN + ascii_map)
            slow_print(Fore.GREEN + f" {result} ")

        # Display footer after decryption
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
            "open_jr": self.journal_menu
        }

    def start(self):
        self.display_logo()
        BootSequence.run()
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
        +-------------------------------------------------------------+
        """
        slow_print(Fore.CYAN + help_text)

    def exit_tr(self):
        frame_effect(" Shutting down the EVIL CORP tr... ", width=60)
        slow_print(generate_footer())
        exit(0)

    def journal_menu(self):
        journal = Journal()
        journal.journal_menu()
