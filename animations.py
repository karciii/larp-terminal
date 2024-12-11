import time
import random
from colorama import Fore, Back, Style
from tqdm import tqdm  # Biblioteka do paskow postepu
from data.ascii_art import FOOTER_TEMPLATE
import threading
import keyboard  # Make sure to install this package

IS_ENABLED = True

def slow_print(text, min_delay=0.05, max_delay=0.1, end='\n'):
    """
    Funkcja do powolnego drukowania tekstu, z opcjonalnym określeniem opóźnienia i sposobu zakończenia.
    
    :param text: Tekst do wydrukowania
    :param min_delay: Minimalne opóźnienie pomiędzy znakami
    :param max_delay: Maksymalne opóźnienie pomiędzy znakami
    :param end: Jak zakończyć wydruk (domyślnie nowa linia)
    """

    if IS_ENABLED:
        for char in text:
            print(char, end='', flush=True)  # Zmieniono end na ''
            time.sleep(random.uniform(min_delay, max_delay))  # Losowe opóźnienie
        print(end, end='\n')  # Dodajemy końcowy argument end (np. '', '\n' lub coś innego)
    else:
        print(text)


stop_animation = False

def check_for_user_input():
    global stop_animation
    while not stop_animation:
        if keyboard.is_pressed('u'):
            stop_animation = True
            print(Fore.RED + "\n[ANIMATION INTERRUPTED]")
            break
        time.sleep(0.1)

def loading_animation(text="Loading", duration=random.randint(3, 60), total_steps=random.randint(1, 5000)):
    if IS_ENABLED:
        global stop_animation
        stop_animation = False
        listener_thread = threading.Thread(target=check_for_user_input)
        listener_thread.daemon = True
        listener_thread.start()

        with tqdm(total=total_steps, desc=text, ncols=80, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]") as pbar:
            step_duration = duration / total_steps
            for _ in range(total_steps):
                if stop_animation:
                    break
                time.sleep(step_duration)
                pbar.update(1)
    else: 
        print("Loading animation disabled, to enable set IS_ENABLED to True in animations.py")

def matrix_rain(duration=5, width=100):
    """
    Matrix-like rain effect with larger width.
    Introduces random red-colored characters to simulate irregular errors.
    """
    if IS_ENABLED:
        end_time = time.time() + duration
        while time.time() < end_time:
            line = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!$&()_-{}|?") for _ in range(width))
            if random.random() < 0.05:  # 5% chance to add red-colored characters to simulate error
                error_position = random.randint(0, width - 1)
                line = line[:error_position] + Fore.RED + line[error_position] + Fore.GREEN + line[error_position + 1:]
            print(Fore.GREEN + line)
            time.sleep(0.05)


def glitch_line(text, glitch_prob=0.05):
    """
    Introduces glitches in the line, replacing some characters with random symbols.
    Occasionally, a character might turn red to represent an error.
    """
    glitched_text = ""
    for char in text:
        if random.random() < glitch_prob:
            glitched_text += random.choice("!@#$%^&*()_+-=[]{}|;':,.<>?")  # Glitch characters
        else:
            glitched_text += char
    # Introduce some random red errors in the middle of the text
    if random.random() < 0.2:  # 20% chance to add a red-colored error
        error_pos = random.randint(0, len(glitched_text) - 1)
        glitched_text = glitched_text[:error_pos] + Fore.RED + glitched_text[error_pos] + Fore.YELLOW + glitched_text[error_pos + 1:]
    print(Fore.YELLOW + glitched_text)


def data_wave_effect(duration=5):
    """
    Data wave effect with random numeric values.
    Occasionally introduce errors in the wave by turning some numbers red.
    """
    if IS_ENABLED:
        end_time = time.time() + duration
        while time.time() < end_time:
            line = ''.join(random.choice("0123456789") for _ in range(80))
            if random.random() < 0.1:  # 10% chance to have red error in data wave
                error_position = random.randint(0, 79)
                line = line[:error_position] + Fore.RED + line[error_position] + Fore.CYAN + line[error_position + 1:]
            print(Fore.CYAN + line)
            time.sleep(0.05)


def flickering_status_line(text, flicker_count=10):
    """
    Flickering effect for status line with various types of error messages.
    Random errors to simulate more unpredictable system failures.
    """
    error_types = [
        "[ERROR] Connection lost",
        "[WARNING] Unauthorized access attempt",
        "[INFO] System operating normally",
        "[CRITICAL] Kernel panic, system failure imminent",
        "[INFO] Data corrupted, repair required",
        "[WARNING] Unusual activity detected in the network",
        "[ERROR] Failed to authenticate user credentials",
        "[INFO] System updated successfully",
        "[CRITICAL] Power supply unstable, shutting down non-essential systems",
        "[WARNING] Disk space critically low",
        "[ERROR] Unable to access secure partition",
        "[INFO] Backup completed at 03:45 AM",
        "[CRITICAL] Memory overflow, restarting processes",
        "[WARNING] Suspicious file detected: quarantine initiated",
        "[ERROR] Database connection timeout",
        "[INFO] Diagnostic check completed, no errors found",
        "[CRITICAL] Firewall breach detected, emergency protocols engaged",
        "[WARNING] Software update delayed due to connectivity issues",
        "[ERROR] Peripheral device malfunction",
        "[INFO] System clock synchronized with atomic time"
    ]
    
    for _ in range(flicker_count):
        error_type = random.choice(error_types)
        if random.random() < 0.5:
            print(Fore.RED + error_type)
        else:
            print(Fore.GREEN + "[OK] " + text)
        time.sleep(0.1)


def generate_footer():
    year = random.randint(2024, 2137)
    return FOOTER_TEMPLATE.format(year=year)


def frame_effect(text, width=60):
    """
    Add frame effect around text. The frame dynamically adjusts to fit the longest line of text.
    """
    # Split the text into lines
    lines = text.split('\n')
    
    # Find the maximum length of a line
    max_line_length = max(len(line) for line in lines)
    
    # Adjust width to the longest line, but keep it at least the given width
    width = max(width, max_line_length + 2)  # +2 to leave space for the border on both sides
    
    # Create the border based on the dynamic width
    border = "+" + "-" * width + "+"
    
    # Print the top border
    slow_print(border)
    
    # Print each line within the frame
    for line in lines:
        slow_print(f"| {line:<{width - 2}} |")  # Subtract 2 for the borders on both sides
    
    # Print the bottom border
    slow_print(border)


def boot_sequence():
    """
    Boot sequence for the system with initial loading effects.
    """
    if IS_ENABLED:
        slow_print("[ SYSTEM BOOT INITIATED... ]\n")
        loading_animation("Loading Core Modules")
        slow_print("\n[ CORE MODULES LOADED ]\n")
        matrix_rain(duration=3, width=100)
        slow_print("\n[ Initializing Security Protocols... ]\n")
        flickering_status_line("Authentication System")
        slow_print("[ ALL SYSTEMS OPERATIONAL ]\n")
        slow_print("-" * 60)
        slow_print(generate_footer())
        pass
    else: print("Boot sequence disabled, to enable set IS_ENABLED to True in animations.py")


# Example usage for the boot sequence
boot_sequence()
