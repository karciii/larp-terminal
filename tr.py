import random
import time
import threading
import keyboard
from time import sleep
from colorama import Fore, Style, init
from data.ascii_art import EVIL_CORP_ASCII, FOOTER_TEMPLATE
from animations import slow_print, glitch_line, loading_animation, data_wave_effect, generate_footer, flickering_status_line, matrix_rain, frame_effect
from encyclopedia import Encyclopedia
from journal import Journal
from login import Login

init(autoreset=True)  # Automatically reset colors after each print.

class BootSequence:
    inactivity_timer = None
    inactivity_timeout = 300  # 5 minutes in seconds.
    inactive_flag = False

    @staticmethod
    def start_inactivity_timer():
        # Start a timer for inactivity detection.
        def inactivity_countdown():
            time.sleep(BootSequence.inactivity_timeout)
            BootSequence.inactive_flag = True
            slow_print(Fore.RED + "\n[INACTIVE] System detected inactivity. Press any key to restart.")

        BootSequence.inactive_flag = False
        BootSequence.inactivity_timer = threading.Thread(target=inactivity_countdown)
        BootSequence.inactivity_timer.daemon = True  # The thread will terminate when the main thread exits.
        BootSequence.inactivity_timer.start()

    @staticmethod
    def reset_inactivity_timer():
        # Reset the inactivity timer.
        BootSequence.inactive_flag = False
        if BootSequence.inactivity_timer:
            BootSequence.inactivity_timer = None
        BootSequence.start_inactivity_timer()

    @staticmethod
    def monitor_activity():
        # Monitor for keyboard activity to reset the timer or restart the boot sequence.
        while True:
            if BootSequence.inactive_flag:
                keyboard.read_event()  # Wait for any key press.
                BootSequence.inactive_flag = False
                BootSequence.run()
            sleep(0.1)

    @staticmethod
    def display_logo():
        # Display the logo with animations.
        for line in EVIL_CORP_ASCII.splitlines():
            print(Fore.RED, end="")
            slow_print(Fore.RED + line, min_delay=0.001, max_delay=0.02)
        slow_print(Fore.YELLOW + " Welcome to the EVIL CORP Terminal System")

    @staticmethod
    def load_core_modules():
        # Simulate loading core modules with an animation.
        slow_print(Fore.YELLOW + "\n[ LOADING CORE MODULES... ]\n")
        loading_animation("Loading Core Modules", duration=5, total_steps=100)
        slow_print(Fore.GREEN + "\n[ CORE MODULES LOADED ]\n")
        matrix_rain(duration=3)

    @staticmethod
    def initialize_security_protocols():
        # Simulate the initialization of security protocols.
        slow_print(Fore.GREEN + "[ Initializing Security Protocols... ]")
        flickering_status_line(" Authentication System ")
        sleep(0.5)
        slow_print(Fore.GREEN + "[ Security Protocols Initialized ]")

    @staticmethod
    def run_diagnostics():
        # Simulate running diagnostics with animations.
        slow_print(Fore.CYAN + "[ Running System Diagnostics... ]")
        data_wave_effect(duration=5)
        slow_print(Fore.CYAN + "[ Diagnostics Complete ]")

    @staticmethod
    def run():
        # Main boot sequence logic.
        BootSequence.reset_inactivity_timer()
        BootSequence.load_core_modules()
        BootSequence.display_logo
        BootSequence.initialize_security_protocols()
        BootSequence.run_diagnostics()

        slow_print(Fore.GREEN + "[ ALL SYSTEMS OPERATIONAL ]\n")
        slow_print(generate_footer())

    @staticmethod
    def shutdown_animation():
        # Shutdown animation with a glitch effect.
        slow_print(Fore.RED + "[ Shutting down system... ]")
        time.sleep(1)
        slow_print(Fore.GREEN + "[ SYSTEM SHUTDOWN COMPLETE ]")
        time.sleep(1)
        slow_print(Fore.WHITE + "[ GOODBYE ]")
        time.sleep(1)
        BootSequence.display_logo()
        frame_effect(Fore.BLUE + "[ THANK YOU FOR USING THE EVIL CORP TERMINAL SYSTEM ]")
        frame_effect(Fore.WHITE + "[ COPYRIGHT © 2137 EVIL CORP. ALL RIGHTS RESERVED. ]")
        time.sleep(5)
        BootSequence.prompt_for_restart()

    @staticmethod
    def prompt_for_restart():
        # Display a prompt for restarting the system.
        slow_print(Fore.YELLOW + " Press any key to boot... ")
        while True:
            if keyboard.read_event():
                break
            time.sleep(0.1)
        slow_print(Fore.YELLOW + " Booting...\n")
        BootSequence.run()


class trCommands:
    @staticmethod
    def gadget_scan():
        # Simulate a gadget scan with animations.
        slow_print("\n\n\n Activating Scanner... \n\n\n")
        loading_animation(" Scanning Area ")
        data_wave_effect(duration=2)
        results = [
            " No threats detected. ",
            " Signal interference detected nearby. ",
            " Unidentified object located in the area. ",
            " Radiation levels within safe limits. "
        ]
        slow_print(f"SCAN RESULT: {random.choice(results)} ")
        slow_print(generate_footer())

    @staticmethod
    def gadget_hack():
        # Simulate a hacking attempt with animations.
        slow_print(" Connecting to target system... ")
        glitch_line(" Establishing secure connection... ")
        loading_animation(" Decrypting Firewall ")
        success = random.random() > 0.4
        if success:
            for _ in range(3):
                data_wave_effect(duration=1)
                glitch_line("\n         HACK SUCCESSFUL! Access Granted!    HACK SUCCESSFUL! Access Granted!    HACK SUCCESSFUL! Access Granted \n")
        else:
            for _ in range(random.randint(5, 15)):
                glitch_line("           HACK FAILED! Intrusion detected!        ")
                sleep(0.2)
            slow_print(Fore.RED + "\n[ALERT] Connection Terminated!")
            flickering_status_line(" Alerting Security... ")

        slow_print(generate_footer())

    @staticmethod
    def gadget_decrypt():
        # Simulate a decryption process with animations.
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
        # Initialize command mappings.
        self.commands = {
            "scan": trCommands.gadget_scan,
            "hack": trCommands.gadget_hack,
            "decrypt": trCommands.gadget_decrypt,
            "help": self.show_help,
            "exit": self.exit_tr,
            "open_en": Encyclopedia().menu,
            "login": self.login,
        }

    def start(self):
        # Start the main terminal system.
        threading.Thread(target=BootSequence.monitor_activity, daemon=True).start()
        BootSequence.display_logo()
        BootSequence.run()  # Start the boot sequence.
        frame_effect(" Type 'help' to see the list of commands. ")
        slow_print(Fore.RED + generate_footer())  # Add footer after boot.
        while True:
            user_input = input(Fore.GREEN + "> ").strip().lower()
            BootSequence.reset_inactivity_timer()
            if user_input in self.commands:
                self.commands[user_input]()
            else:
                slow_print(Fore.RED + "Unknown command. Type 'help' for available commands.")
                slow_print(generate_footer())


    def show_help(self):
        # Display the help menu with commands.
        help_text = """
        +-------------------------------------------------------------+
        |                       Available Commands                    |
        +-------------------------------------------------------------+
        | scan    : Perform a scan of the surrounding area.           |
        | hack    : Attempt to hack into a system.                    |
        | decrypt : Decrypt secure messages                           |
        | help    : Display this help information.                    |
        | login   : Open login menu.                                  |  
        | open_en : Access the encyclopedia.                          |
        | exit    : Exit the Terminal.                                |                                         |
        +-------------------------------------------------------------+
        """
        slow_print(help_text)

    def exit_tr(self):
        # Exit the terminal system.
        slow_print(Fore.RED + "Exiting the terminal system... \n")
        BootSequence.shutdown_animation()
        # exit(0)

    def login(self):
        # Open the login menu.
        login = Login()
        login.login_menu()
