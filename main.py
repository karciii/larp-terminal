import time
import random
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Constants
EVIL_CORP_ASCII = r"""
  ______     _   _   _   _    ____   ____  _____  
 |  ____|   | | | | | \ | |  / __ \ / __ \|  __ \ 
 | |__ _   _| |_| |_|  \| | | |  | | |  | | |__) |
 |  __| | | | __| __| . ` | | |  | | |  | |  ___/ 
 | |  | |_| | |_| |_| |\  | | |__| | |__| | |     
 |_|   \__, |\__|\__|_| \_|  \____/ \____/|_|     
        __/ |                                     
       |___/                                      
"""

FOOTER_TEMPLATE = "Software by EVIL CORP, {year}"

# Utility Functions
def slow_print(text, min_delay=0.02, max_delay=0.1, newline=True):
    """Prints text character by character with random delay."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(random.uniform(min_delay, max_delay))
    if newline:
        print()

def loading_animation(text="Loading", duration=5):
    """Displays a loading animation with moving dots."""
    end_time = time.time() + duration
    while time.time() < end_time:
        for dots in range(1, 4):
            print(f"\r{text}{'.' * dots}   ", end='', flush=True)
            time.sleep(0.5)
    print("\r" + " " * 50, end='')  # Clear line after animation

def matrix_rain(duration=5, width=40):
    """Simulates a Matrix-style text rain effect."""
    end_time = time.time() + duration
    while time.time() < end_time:
        line = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(width))
        print(Fore.GREEN + line)
        time.sleep(0.05)

def glitch_line(text, glitch_prob=0.2):
    """Simulates a glitchy text line with random distortions."""
    glitched_text = ""
    for char in text:
        if random.random() < glitch_prob:
            glitched_text += random.choice("!@#$%^&*()_+-=[]{}|;':,.<>?")
        else:
            glitched_text += char
    print(Fore.YELLOW + glitched_text)

def data_wave_effect(duration=5):
    """Simulates a wave of processing data with scrolling numbers."""
    end_time = time.time() + duration
    while time.time() < end_time:
        line = ''.join(random.choice("0123456789") for _ in range(80))
        print(Fore.CYAN + line)
        time.sleep(0.05)

def flickering_status_line(text, flicker_count=10):
    """Creates a flickering effect for a status line."""
    for _ in range(flicker_count):
        if random.random() > 0.5:
            print(Fore.RED + "[ERROR] " + text)
        else:
            print(Fore.GREEN + "[OK] " + text)
        time.sleep(0.1)

def generate_footer():
    """Generate dynamic footer with changing year."""
    year = random.randint(1980, 2024)
    return FOOTER_TEMPLATE.format(year=year)

# Classes
class Terminal:
    """Main terminal class to organize features."""
    def __init__(self):
        self.commands = {
            "scan": self.gadget_scan,
            "hack": self.gadget_hack,
            "decrypt": self.gadget_decrypt,
            "help": self.show_help,
            "exit": self.exit_terminal
        }
    
    def start(self):
        """Starts the terminal with animations and boot sequence."""
        self.display_logo()
        self.boot_sequence()
        slow_print("Type 'help' to see the list of commands.")
        while True:
            user_input = input(Fore.GREEN + "> ").strip().lower()
            if user_input in self.commands:
                self.commands[user_input]()
            else:
                slow_print(Fore.RED + "Unknown command. Type 'help' for available commands.")
    
    def display_logo(self):
        """Displays the EVIL CORP logo."""
        for line in EVIL_CORP_ASCII.splitlines():
            slow_print(Fore.RED + line, min_delay=0.02, max_delay=0.05)
        print("\n")
        slow_print(Fore.YELLOW + "Welcome to the EVIL CORP Terminal System")
        time.sleep(1)

    def boot_sequence(self):
        """Simulates a boot-up sequence for the system."""
        slow_print("[SYSTEM BOOT INITIATED...]")
        loading_animation("Loading Core Modules")
        slow_print("[CORE MODULES LOADED]")
        matrix_rain(duration=3)
        slow_print("[Initializing Security Protocols...]")
        flickering_status_line("Authentication System")
        slow_print("[ALL SYSTEMS OPERATIONAL]")
        slow_print("-" * 40)
        slow_print(generate_footer())

    def gadget_scan(self):
        """Simulates a scanning gadget."""
        slow_print("Activating Scanner...")
        loading_animation("Scanning Area")
        data_wave_effect(duration=2)
        results = [
            "No threats detected.",
            "Signal interference detected nearby.",
            "Unidentified object located in the area.",
            "Radiation levels within safe limits."
        ]
        slow_print(f"SCAN RESULT: {random.choice(results)}")
        slow_print(generate_footer())

    def gadget_hack(self):
        """Simulates a hacking attempt."""
        slow_print("Connecting to target system...")
        glitch_line("Establishing secure connection...")
        loading_animation("Decrypting Firewall")
        success = random.random() > 0.4  # 60% success chance
        if success:
            glitch_line("HACK SUCCESSFUL! Access Granted!")
            data_wave_effect(duration=3)
        else:
            glitch_line("HACK FAILED! Intrusion detected!")
        slow_print(generate_footer())

    def gadget_decrypt(self):
        """Simulates a decryption process."""
        slow_print("Decrypting secure files...")
        loading_animation("Decrypting")
        decrypted = random.choice([
            "File decrypted: Classified personnel records.",
            "Decryption failed: Corrupted file.",
            "File decrypted: Top secret prototype schematics."
        ])
        slow_print(Fore.CYAN + decrypted)
        slow_print(generate_footer())

    def show_help(self):
        """Displays a list of available commands."""
        slow_print("Available commands:")
        for cmd in self.commands.keys():
            slow_print(f"- {cmd}: {self.commands[cmd].__doc__}")
        slow_print(generate_footer())

    def exit_terminal(self):
        """Exits the terminal program."""
        slow_print(Fore.YELLOW + "Shutting down the EVIL CORP Terminal...")
        slow_print(generate_footer())
        exit(0)

# Main Execution
if __name__ == "__main__":
    terminal = Terminal()
    try:
        terminal.start()
    except KeyboardInterrupt:
        slow_print("\nSession terminated.")
