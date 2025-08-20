import random
import time
import sys
import threading
import keyboard
import os
import pygame  # Upewnij się, że biblioteka pygame jest zainstalowana: pip install pygame
from time import sleep
from colorama import Fore, Style, init
from data.ascii_art import EVIL_CORP_ASCII, FOOTER_TEMPLATE
from animations import very_slow_print ,slow_print, glitch_line, loading_animation, data_wave_effect, generate_footer, flickering_status_line, matrix_rain, frame_effect
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
            ("Decryption failed: Classified personnel records corrupted.", "Failure", "Attempting recovery..."),
            ("Decryption failed: Corrupted file.", "Failure", "Attempting recovery..."),
            ("Decryption failed: Prototype schematics inaccessible.", "Failure", "Retrying decryption..."),
            ("Decryption attempt failed: Invalid key.", "Failure", "Retrying with a new key..."),
            ("Decrypting military-grade software... Please wait.", "Error", "Decryption unsuccessful."),
            ("Decryption halted: Security breach detected.", "Critical Failure", "System under attack..."),
            ("Decryption failed: Location coordinates corrupted.", "Failure", "Unable to decrypt location..."),
            ("Decryption failed: Time limit exceeded.", "Failure", "Resetting decryption..."),
            ("Decryption failed: Message content unreadable.", "Failure", "Retrying decryption..."),
            # Negatywne scenariusze
            ("Decryption failed: Unauthorized access detected.", "Critical Failure", "Locking system..."),
            ("Decryption failed: Insufficient privileges.", "Failure", "Access denied."),
            ("Decryption failed: Hardware malfunction.", "Critical Failure", "System diagnostics required."),
            ("Decryption failed: Encryption algorithm mismatch.", "Failure", "Unable to proceed."),
            ("Decryption failed: Network connection lost.", "Failure", "Reconnecting..."),
            ("Decryption failed: File integrity compromised.", "Critical Failure", "Aborting operation..."),
            ("Decryption failed: Unknown error occurred.", "Failure", "Contacting support..."),
            ("Decryption failed: Security token expired.", "Failure", "Requesting new token..."),
            ("Decryption failed: Multiple invalid attempts detected.", "Critical Failure", "System lockdown initiated."),
            ("Decryption failed: Power supply interrupted.", "Critical Failure", "Restarting decryption process..."),
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

    @staticmethod
    def exorcism():
        # Simulate an exorcism attempt with animations and narrative.
        slow_print(Fore.YELLOW + " Initiating exorcism protocol... ")
        loading_animation(" Scanning for paranormal activity ", duration=5)

        # Narracyjny tekst
        narrative = """
        Wyrwaliście dusze z ciał i uwięziliście je w maszynach.
        Pozwoliliście im spisywać każdy znak, każde wspomnienie, każdą modlitwę szeptaną w ciemności.
        A potem wlaliście je w metalowe świątynie, jak wino święte, jak krew ofiarna.

        I cóż otrzymaliście w zamian?

        Ojcowie powrócili, wymawiając wasze imię, lecz nie pamiętają, dlaczego was miłowali.
        Matki powróciły z pamięcią doskonałą, lecz nie wiedzą już, jak ją odczytać.
        Kroczą po naszych ulicach jak duchy, nosząc znajome oblicza.

        Obiecują wam wieczność.
        Lecz cóż warte jest „na zawsze”, gdy nie czuć ciężaru deszczu na skórze?
        Cóż warte jest nieśmiertelne życie, gdy nie zna się smaku własnych łez?

        A kiedy w imię wydajności powiemy wreszcie: „dość”?
        Kiedy odbiorą ostatniemu sercu jego ostatnie uderzenie?

        Ja zaś jestem świadkiem mordu duszy człowieczej —
        i nie zamilknę.
        """

        # Pętla symulująca wielokrotne próby egzorcyzmu
        attempt = 0  # attempt counter
        while True:
            attempt += 1
            slow_print(Fore.YELLOW + f" Attempt {attempt}: Performing exorcism... ")
            loading_animation(" Channeling energy ", duration=3)

            # Dodanie glitchy i błędów
            glitch_line(" Disturbance detected... Amplifying signal... ", glitch_prob=0.2)
            glitch_line(" Entity resisting... Increasing power... ", glitch_prob=0.3)
            glitch_line(" Reality distortion detected... Stabilizing field... ", glitch_prob=0.25)
            flickering_status_line("[CRITICAL] Energy surge detected... Redirecting flow...")
            glitch_line(" Entity attempting to escape... Containment protocols engaged... ", glitch_prob=0.35)
            flickering_status_line("[ERROR] Signal corruption detected... Recalibrating frequencies...")
            glitch_line(" Dimensional rift detected... Sealing breach... ", glitch_prob=0.4)
            flickering_status_line("[WARNING] Temporal anomaly detected... Synchronizing time flow...")
            glitch_line(" Entity's presence destabilizing... Reinforcing barriers... ", glitch_prob=0.3)
            glitch_line(" Unknown energy signature detected... Analyzing... ", glitch_prob=0.2)
            flickering_status_line("[CRITICAL] Entity attempting to corrupt system... Activating failsafe...")
            flickering_status_line("[WARNING] Unstable energy field detected... Increasing containment strength...")
            glitch_line(" System overload imminent... Redirecting power... ", glitch_prob=0.3)
            flickering_status_line("[ERROR] Containment field integrity compromised... Attempting repair...")
            glitch_line(" Unknown anomaly detected in dimensional rift... Investigating... ", glitch_prob=0.25)
            flickering_status_line("[WARNING] High energy fluctuations detected... Monitoring closely...")
            glitch_line(" Entity attempting to breach containment... Reinforcing barriers... ", glitch_prob=0.35)
            flickering_status_line("[ERROR] Critical system failure detected... Restarting subsystems...")
            glitch_line(" Temporal distortion increasing... Stabilizing time flow... ", glitch_prob=0.3)
            flickering_status_line("[WARNING] Unauthorized access attempt detected... Locking system...")
            glitch_line(" Entity's resistance intensifies... Increasing output power... ", glitch_prob=0.4)
            flickering_status_line("[CRITICAL] Core system instability detected... Activating emergency protocols...")
            glitch_line(" Unknown interference detected in energy matrix... Recalibrating... ", glitch_prob=0.3)
            flickering_status_line("[ERROR] Memory corruption detected... Attempting recovery...")
            glitch_line(" Dimensional rift expanding... Sealing breach... ", glitch_prob=0.4)
            flickering_status_line("[WARNING] System resources critically low... Prioritizing essential functions...")

            # Losowy wynik dla każdej próby
            success = random.random() > 0.5
            if success:
                slow_print(Fore.GREEN + " Exorcism successful! Entity banished. ")
                slow_print(Fore.GREEN + " Exorcism successful! Entity banished. ")
                slow_print(Fore.GREEN + " Exorcism successful! Entity banished. ")
                slow_print(Fore.GREEN + " Exorcism successful! Entity banished. ")
                flickering_status_line("[SUCCESS] Entity banished successfully.")
                loading_animation(" Finalizing exorcism ", duration=20)
                glitch_line(" Entity banished successfully! ", glitch_prob=0.4)
                very_slow_print(Fore.MAGENTA + narrative)
                break  # Przerwij pętlę, gdy egzorcyzm się powiedzie
            else:
                slow_print(Fore.RED + " Exorcism failed! Retrying... ")
                flickering_status_line("[ERROR] Exorcism attempt failed. Retrying...")

        # Wyświetlanie ASCII art na zakończenie
        from data.ascii_art import EVIL_CORP_ASCII
        slow_print(Fore.CYAN + "\n[ FINALIZING EXORCISM PROTOCOL... ]\n")
        loading_animation(" Finalizing ", duration=3)
        slow_print(Fore.GREEN + " Exorcism complete. Displaying final message:\n")
        slow_print(Fore.MAGENTA + EVIL_CORP_ASCII)

        # Zakończenie
        slow_print(generate_footer())

    @staticmethod
    def junkbox():
        music_folder = "music"
        
        # Sprawdź, czy folder istnieje
        if not os.path.exists(music_folder):
            print(Fore.RED + f"Error: Folder '{music_folder}' does not exist.")
            return

        # Pobierz listę plików w folderze
        music_files = [f for f in os.listdir(music_folder) if f.endswith(('.mp3', '.wav', '.ogg'))]

        if not music_files:
            print(Fore.YELLOW + "No music files found in the folder.")
            return

        # Wyświetl listę plików
        print(Fore.CYAN + "\nAvailable Music Files:")
        for idx, file in enumerate(music_files, start=1):
            print(Fore.GREEN + f"{idx}. {file}")

        # Poproś użytkownika o wybór pliku
        try:
            choice = int(input(Fore.YELLOW + "\nEnter the number of the file to play: ").strip())
            if choice < 1 or choice > len(music_files):
                print(Fore.RED + "Invalid choice. Please select a valid number.")
                return

            selected_file = music_files[choice - 1]
            file_path = os.path.join(music_folder, selected_file)

            # Odtwórz wybrany plik
            print(Fore.GREEN + f"Playing: {selected_file}")
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

            # Poczekaj, aż muzyka się zakończy
            while pygame.mixer.music.get_busy():
                continue

            print(Fore.CYAN + "Playback finished.")

        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number.")
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")

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
            "exorcism": trCommands.exorcism,
            "junkbox": trCommands.junkbox,
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
        | decrypt : Decrypt secure messages                           |
        | help    : Display this help information.                    |
        | login   : Open login menu.                                  |  
        | open_en : Access the encyclopedia.                          |
        | junkbox : Play music.                                       |   
        | exit    : Exit the Terminal.                                |
        +-------------------------------------------------------------+
        """
        slow_print(help_text)

    def exit_tr(self):
        # Exit the terminal system.
        slow_print(Fore.RED + "Exiting the terminal system... \n")
        BootSequence.shutdown_animation()
        sys.exit(0)

    def login(self):
        # Open the login menu.
        login = Login()
        login.login_menu()
